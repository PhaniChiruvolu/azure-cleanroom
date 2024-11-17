param(
    [parameter(Mandatory = $false)]
    [string]$tag = "latest",

    [parameter(Mandatory = $false)]
    [string]$repo = "docker.io",

    [parameter(Mandatory = $false)]
    [switch]$push
)

. $PSScriptRoot/../helpers.ps1

if ($repo) {
    $imageName = "$repo/testvolmount:$tag"
}
else {
    $imageName = "testvolmount:$tag"
}

$root = git rev-parse --show-toplevel
docker image build -t $imageName `
    -f $PSScriptRoot/../docker/testcontainers/Dockerfile.testVolMount $root
CheckLastExitCode

if ($push) {
    docker push $imageName
    CheckLastExitCode
}