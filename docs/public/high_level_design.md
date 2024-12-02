# High Level Design
<!--
This section captures high-level design of Azure Clean Room Infrastructure.
Audience: Engineering
Prerequisites: Architectural Overview
-->
Azure Clean Room implements this architecture on top of Azure Confidential Container Instances (Confidential ACI).

![Type 0 Azure Clean Room using Confidential ACI](../assets/excalidraw/cleanroom_type0_custom_runtime.svg)
Figure *Type 0 Azure Clean Room using Confidential ACI (Production)*

- The clean room specification is translated into a Confidential ACI container group specification, consisting of a set of infrastructure containers (sidecars) executing audited/trusted code, and a set of user containers running unaudited/untrusted code.
- The container group is configured such that the infrastructure containers (sidecars) execute with system/root privileges and user containers executed with user/non-root privileges.
- The infrastructure containers (sidecars) leverage constructs from the underlying kernel and container runtime to set up firewall rules and mount points that ensure all IO from the user containers is intercepted by the infrastructure containers.

<!-- TODO: Add details about the options for customers to explicitly specify this external trust as part of the clean room specification.  -->

## Code Sandbox
<!-- TODO: Add high level design of the mechanisms used to realize a code sandbox. -->
- Infrastructure – privileged containers, launched using ACI.
- Application – non privileged containers, launched using podman.

## Data Protection Firewall
<!-- TODO: Add high level design of the mechanisms used to ensure interception of all traffic originating from within the sandbox. -->
- Storage – Only secure volumes mounted to application containers
- Network – Iptables firewall configured to drop all external packets

## Privacy Proxy

### Volume
<!-- TODO: Add high level design of the mechanism used to surface a “secure" mode hardened volume as a data source/sink for Azure Blob Storage. -->
- `blobfuse` mounted Azure Storage
- Individual encrypted blobs present to application as clear text files
- Secure key release for encryption key

### API
<!-- TODO: Add high level design of the mechanism used to surface a “open” mode hardened HTTP API endpoint. -->
- Envoy HTTP proxy
- Open Policy Agent engine inspects request-response

## Governance

### Consent
<!-- TODO: Add high level design of the mechanism used for runtime validation of consent for executing the application or presenting data. -->
- Infrastructure code invokes specified external service endpoint (trusted) to check for consent to execute the application and present data to it.
- Governance service responsible for maintaining tamper proof consent, infrastructure code only ensures that invoking the consent endpoint resulted in a valid response (based on specified success codes) before proceeding with the operation.
- Support for multiple consent endpoints.

### Audit
<!-- TODO: Add high level design of the mechanism used to log audit events and generate of an audit trail for all privileged operations performed inside the clean room. -->
- Infrastructure code invokes specified external service endpoint (trusted) to record audit events.
- Governance service responsible for maintaining tamper proof audit ledger, infrastructure code only ensures that invoking the audit endpoint resulted in a response confirming that the audit event has been recorded (based on specified success codes) before proceeding with the operation.
- Support for multiple audit endpoints.

### Telemetry

#### INFRASTRUCTURE
<!-- TODO: Add high level design of the mechanism used to govern and emit telemetry about the infrastructure. -->
- Collect Open Telemetry (OTel) metrics, traces and logs emitted by infrastructure code.
- Infrastructure code invokes specified external service endpoint (trusted) to check for consent to export telemetry events.
- Governance service responsible for maintaining tamper proof consent, infrastructure code only ensures that invoking the consent endpoint resulted in a valid response (based on specified success codes) before exporting the events to the data sink specified in the clean room specification.
- Low data egress risk expected as infrastructure code is audited and trusted, data sink proxy can operate in any mode - secure/trusted/open.
- E.g., encrypted blobs in Azure Storage container.

#### APPLICATION
<!-- TODO: Add high level design of the mechanism used to govern and emit application logs. -->
- Capture console logs emitted by application.
- Infrastructure code invokes specified external service endpoint (trusted) to check for consent to export application logs.
- Governance service responsible for maintaining tamper proof consent, infrastructure code only ensures that invoking the consent endpoint resulted in a valid response (based on specified success codes) before copying captured logs to the data sink specified in the clean room specification.
- High data egress risk as application code is unaudited and untrusted, data sink proxy can only operate in protected modes - secure/trusted.
- E.g., encrypted blobs in Azure Storage container.
