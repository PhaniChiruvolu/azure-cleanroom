# Tooling
<!--
    This section describes the tooling for translating a Clean Room specification into a deployment template.
-->

Full document [here](/src/tools/azure-cli-extension/cleanroom/README.md)

Tooling is required to translate the Clean Room specification into an ARM template that can be used to deploy a Clean Room enforcing the data protection intent within a confidential computation environment. The ARM template and the associated secure key release policy ensure that the TEE measurement and attestation include the Clean Room infrastructure binary components required for data protection, as well as their configuration applying customer specified rules to enforce the data protection intent.

The mechanism for generating this ARM template and key release policy needs to be transparent, so that customers can ensure that all elements of the generated template are accounted for and relate to their specification. Publishing and sustaining this tooling in a Microsoft maintained open-sourced repository enables customers to develop an auditable and verifiable trust in this mechanism without any opaque/closed components requiring implicit trust.

<!-- TODO: Add more details about the tooling. -->
