# Deploy clean rooms locally for development <!-- omit from toc -->

The intent of this guide is to setup a clean room environment where in the clean room infrastructure
and application containers all run locally on a Kind cluster instead of a Confidential ACI container
group in Azure.

This is geared towards local development and learning scenarios where deploying to C-ACI as part of
the development loop can become an overhead. The ability to test the changes locally with a full
setup would help in speeding up development and also increase familiarity with the underlying
architecture.

> [!WARNING]
> The virtual version of cleanroom runs on hardware that does not support SEV-SNP. Virtual mode
> does not provide any security guarantees and should be used for development purposes only.

## Prerequisites <!-- omit from toc -->

### Dev Container/GitHub Codespaces

You can [open this repo](../../README.md#quickstart) in a dev container or a GitHub Codespace. These
environments are pre-configured so the only other setup required is to add the CleanRoom Azure CLI
extension using:

```powershell
az extension add --source https://cleanroomazcli.blob.core.windows.net/azcli/cleanroom-0.0.7-py2.py3-none-any.whl -y --allow-preview true
```

### Local Setup

We recommend running the following steps in PowerShell on WSL using Ubuntu 22.04.

- Instructions for setting up WSL can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install).
- To install PowerShell on WSL, follow the instructions [here](https://learn.microsoft.com/en-us/powershell/scripting/install/install-ubuntu?view=powershell-7.3).

To set this infrastructure up, we will need the following tools to be installed prior to running the setup scripts.

1. An Azure subscription with adequate permissions to create resources and manage permissions on these resources.
2. Azure CLI version >= 2.57. Installation instructions [here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux).
3. You need Docker for Linux installed locally. Installation instructions [here](https://docs.docker.com/engine/installation/#supported-platforms).
4. Confidential containers Azure CLI extension, version >= 0.3.5. You can install this extension using ```az extension add --name confcom -y```. You can check the version of the extension using ```az extension show --name confcom```. Learn about it [here](https://learn.microsoft.com/en-us/cli/azure/confcom?view=azure-cli-latest).
5. azcopy versions >= 10.25.0. Installation instructions [here](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10).
6. openssl - Download instructions for Linux [here](https://www.openssl.org/source/).
7. jq - Download / install instructions for Linux [here](https://jqlang.github.io/jq/download/).
8. Add the CleanRoom Azure CLI extension using:

    ```powershell
    az extension add --source https://cleanroomazcli.blob.core.windows.net/azcli/cleanroom-0.0.7-py2.py3-none-any.whl -y --allow-preview true
    ```

- Kind: see steps [here](https://kind.sigs.k8s.io/docs/user/quick-start/) to install it.

## Differences compared to CACI deployment <!-- omit from toc -->

- Runs in non SEV-SNP environment.
- Uses an allow all cce policy enforcement for SKR.
- The SKR setup is not locked down and open to releasing keys to any clean room enviornment and
  meant for development purposes only.
- The setup creates and uses Azure Key Vault and Azure Storage accounts. The interactions with these
  services are not emulated/mocked.

## Setup instructions <!-- omit from toc -->

Follow the below steps to create a local setup.

## 1. Create Kind cluster and a local registry

Below creates a kind cluster named `kind-cleanroom` and also starts a local registry container named `kind-registry`. The cluster is configured so that it can reach the registry endpoint at `localhost:5001` from within the cluster.

```powershell
$root = git rev-parse --show-toplevel
bash $root/test/onebox/kind-up.sh
```

## 2. Build clean room containers and push to local registry

The below command will build the clean room infrastructure containers and push the images to the
local registry that was started above. These images get deployed on the kind cluster to create the
virtual clean room environment.

```powershell
pwsh $root/build/onebox/build-local-cleanroom-containers.ps1
```

Unless you are changing the code for the container images you can run the above command once and
keep re-using the pushed images when running the subsequent steps below.

## 3. Run the collab scenario locally
>
> [!NOTE]
> The steps below run with `scenario=encrypted-storage` but the same flow can be used with
> `db-access` or `ml-training` scenarios also.

With the kind cluster setup execute the below command to run the scenario:

```powershell
$scenario = "encrypted-storage"
pwsh $root/test/onebox/multi-party-collab/$scenario/run-collab.ps1
```

## 4. Delete the clean room from the local cluster

To remove the clean room instance run the following:

```powershell
pwsh $root/test/onebox/multi-party-collab/remove-virtual-cleanroom.ps1
```

## 5. Run scenarios in CACI

Follow the below steps to run the scenario in CACI instead of the Kind cluster. Note that below runs the scenarios in with the same insecure (allow all) CCE policy meant for dev/test:

```powershell
# Build and publish all the container images.
$root = git rev-parse --show-toplevel
$acrname = <youracrname>
$repo = "$acrname.azurecr.io"
$tag = "onebox"
$withCcePolicy = $false # change to true if CCE policy should be computed and enforced.

az acr login -n $acrname

pwsh $root/build/onebox/build-local-cleanroom-containers.ps1 `
  -repo $repo `
  -tag $tag `
  -withRegoPolicy:$withCcePolicy

pwsh $root/build/ccf/build-ccf-infra-containers.ps1 `
  -repo $repo `
  -tag $tag `
  -push `
  -pushPolicy:$withCcePolicy

# Launch the scenario.
$scenario = "nginx-hello"
pwsh $root/test/onebox/multi-party-collab/$scenario/run-collab-aci.ps1 `
  -registry acr `
  -registryUrl $repo `
  -tag $tag `
  -allowAll:(!$withCcePolicy)
```
