# Specification & Tooling

As discussed earlier, the Clean Room application architecture allows customers to operate with a simplified grammar that captures the desired data protection intent as a Clean Room specification.

## Specification
<!--
    This section describes the schema used for a Clean Room specification.
    Update this section with any changes to the schema.
-->

The Clean Room specification describes the set of data sources and data sinks that need to be made available within the clean room, the set of applications to be deployed within the clean room consuming this data as well any endpoints that need to be enabled for communication with these applications. Additional configuration includes the code sandbox configuration details and details of the endpoints to be used for governance.

```yaml
Specification:
  DataSources:
    - DataSource
  DataSinks:
    - DataSink
  Applications:
    - Application
  Sandbox: SandboxSettings
  Governance: GovernanceSettings
```

### DATA

The Clean Room specification includes details about the data source(s) and data sink(s) to be surfaced - the type of the data source/sink, resource providing the backing data store, identity to be used for accessing the resource and privacy protection configuration.

```yaml
# Data related.
DataSource:
  Name: string
  Type: string # Type of the data source.
  Path: string
  Store: Resource # Backing data store.
  Identity: Identity # Identity to be used for accessing the resource.
  Protection: PrivacyProxySettings

DataSink:
  Name: string
  Type: string # Type of the data sink.
  Path: string
  Store: Resource # Backing data store.
  Identity: Identity # Identity to be used for accessing the resource.
  Protection: PrivacyProxySettings
```

### RESOURCE

```yaml
# Resource
Resource:
  Name: string # Name of the resource.
  Type: string # Type of the resource.
  Id: string # ID of the resource.
  Provider: ServiceEndpoint
ServiceEndpoint:
  Protocol: string # Service communication protocol.
  URL: string # Service endpoint.
  Configuration: string # Service specific details required for communication.
```

### IDENTITY

The Clean Room specification includes details about the identity to be used for accessing a given resource. These identities can be based on attestation of the compute instance (AttestationBasedTokenIssuer), presentation of a secret (SecretBasedTokenIssuer) or identity federation (FederatedIdentityBasedTokenIssuer).

```yaml
# Identity
Identity:
  Name: string
  ClientId: string # User.
  TenantId: string # Directory.
  TokenIssuer: AttestationBasedTokenIssuer | SecretBasedTokenIssuer | FederatedIdentityBasedTokenIssuer # Token issuer service.
AttestationBasedTokenIssuer:
  Issuer: ServiceEndpoint # Token issuer service.
SecretBasedTokenIssuer:
  Issuer: ServiceEndpoint # Token issuer service.
  Secret: CleanRoomSecret
  SecretAccessIdentity: Identity # Token issuer service - AttestationBasedTokenIssuer.
FederatedIdentityBasedTokenIssuer:
  Issuer: ServiceEndpoint # Token issuer service.
  FederatedIdentity: Identity # Identity to be used for federating with the token issuer.
CleanRoomSecret:
  SecretType: string # Key | Certificate | Secret
  BackingResource: Resource
```

### PRIVACY PROTECTION

The Clean Room specification includes details about the privacy proxy to be used, the protection mode – Secure/Trusted/Open, policy specifying any rules to be enforced and the secret to be used for decryption and encryption of sensitive data.

```yaml
# Protection
PrivacyProxySettings:
  ProxyType: string # Type of privacy proxy.
  ProxyMode: string # Proxy privacy mode - Secure | Trusted | Open.
  PrivacyPolicy: Policy # Proxy specific privacy policy.
  Configuration: string # Proxy specific configuration details.
  EncryptionSecret:
    # If both DEK and KEK are provided, then the DEK is assumed to be wrapped by KEK.
    # If only DEK is provided, then the DEK is assumed to be unwrapped.
    # If both DEK and KEK are not provided, then data is not protected and is in clear text.
    DEK: CleanRoomSecret # Data Encryption Key.
    KEK: CleanRoomSecret # Key Encryption Key.
  EncryptionSecretAccessIdentity: Identity

# Policy
Policy: InlinePolicy | ExternalPolicy
InlinePolicy: string # Inline policy.
ExternalPolicy: Document # Downloadable policy.
Document: # Self contained reference to document
  DocumentType: string # File | OCI
  BackingResource: Resource
  Identity: Identity # Identity to be used for accessing the resource.
  AuthenticityReceipt: string
```

### APPLICATION

The Clean Room specification includes details about the application(s) to be executed within the code sandbox. These applications are locked down and can only access the configured data source/data sink or communicate with each other through a local port.

```yaml
# Application related.
Application:
  Name: string
  Image:
    Executable: Document
    Protection: PrivacyProxySettings
    EnforcementPolicy: Policy # Application specific enforcement policy.
  Command:
    - string
  EnvironmentVariables:
    - string:string
  RuntimeSettings:
    Parameters []: string:string
    Environment []: string:string
    Payload []: string:string | string:DataSource
  ApplicationEndpoint:
    Type: string
    Port: int
    Protection: PrivacyProxySettings
```

### SANDBOX

The Clean Room specification includes details about the type of sandbox to be created for hosting the application.

```yaml
# Sandbox related.
SandboxSettings:
  Type: int # Type of clean room – 0 | 1 | 2 | 3. Currently supported - 0.
  Configuration: Policy # Sandbox specific configuration.
```

### GOVERNANCE

The Clean Room specification includes details about the endpoints to be invoked for meeting any governance requirements, such as runtime validation of consent for executing the application or presenting data or generation of an audit trail for all privileged operations performed inside the clean room.

```yaml
# Governance related.
GovernanceSettings:
  Consent:
    # Endpoints to be invoked for runtime validation of consent for executing
    # the application or presenting data to the application.
    - GovernanceService
  Audit:
    # Endpoints to be invoked to record an auditable event.
    - GovernanceService
  Telemetry:
    Infrastructure:
      Consent: GovernanceService # Endpoint to check consent for exporting telemetry events.
      Metrics: DataSink
      Traces: DataSink
      Logs: DataSink
    Application:
      Consent: GovernanceService # Endpoint to check consent for exporting application logs.
      Logs: DataSink
GovernanceService:
  URL: string # Service endpoint to be invoked for governance.
  Method: string # Method to be invoked on the endpoint.
  ValidResponses: # Accepted response codes.
    - int # HTTP status code
  Identity: Identity # Identity to be used for accessing the endpoint.
```

## Tooling
<!--
    This section describes the tooling for translating a Clean Room specification into a deployment template.
-->

Tooling is required to translate the Clean Room specification into an ARM template that can be used to deploy a Clean Room enforcing the data protection intent within a confidential computation environment. The ARM template and the associated secure key release policy ensure that the TEE measurement and attestation include the Clean Room infrastructure binary components required for data protection, as well as their configuration applying customer specified rules to enforce the data protection intent.

The mechanism for generating this ARM template and key release policy needs to be transparent, so that customers can ensure that all elements of the generated template are accounted for and relate to their specification. Publishing and sustaining this tooling in a Microsoft maintained open-sourced repository enables customers to develop an auditable and verifiable trust in this mechanism without any opaque/closed components requiring implicit trust.

<!-- TODO: Add more details about the tooling. -->

## Frequently Asked Questions

### Is the tooling available in the form of a Microsoft Clean Room RP?

An Azure Clean Room is not a new type of Azure Compute “ARM Resource” – it is a configuration of existing Azure Compute constructs to enforce data protection.

A configuration is not a useful ARM resource by itself as it is not “doing” anything for the customer on its own. Customers derive value only when this configuration is consumed by the Resource Provider offering the underlying Azure Compute construct to instantiate a clean room instance.

A Clean Room Resource Provider (Clean Room RP) deploying the clean room configuration on behalf of the customers is of limited value as well:

- It is not feasible for the Clean Room RP to surface and wrap every single capability of the underlying Azure Compute offerings.
- Further, every Azure Compute offering provides mechanisms to manage, scale and orchestrate customer applications and their instances, and it is not feasible to put a Clean Room RP hat on this management functionality and experience.
- From a customer’s point of view, deploying a standalone instance of a limited capability Azure Compute construct is not very useful and is instead counterproductive.
- From a data protection perspective, an RP running opaque code behind a Microsoft AME tenant goes against the zero-trust requirement and we necessarily need to maintain live and updated tooling for customers to independently derive the deployment template from the clean room specification and verify that the RP has deployed an identical copy.

Given the need for open-sourced tooling independent of a Clean Room RP, and the limited customer value offered by a Clean Room RP either for specifications or deployments, building an RP is deferred and only open-sourced tooling is made available.

_Note that a case is made for a Clean Room RP providing customer value-add specifically in the context of multi-party collaboration workflows – this is explored later in the document as part of the Collaboration discussion._
