# User Flow
<!--
    This section provides an overview of end-to-end customer flows leveraging a clean room for processing sensitive data in the public cloud.
    Audience: Engineering & PM
    Prerequisites: Architectural Overview
-->

## Canonical Workflow

The workflow for storing sensitive data in the public cloud and consuming it from an application executing within a Clean Room involves multiple phases.

### Preparation Stage

#### DATA PREPARATION PHASE
In this phase, customers secure the data to be processed inside the clean room. Typical considerations for this phase include evaluation of storage requirements for the encrypted data, mechanisms for protection of the data through encryption, and mechanisms for secure storage of the encryption key.
#### SPECIFICATION GENERATION PHASE
In this phase, customers author specification of clean room(s) that should have access to the secured data. Typical considerations for this phase include evaluation of the security requirements (type of the clean room), evaluation of the privacy protection requirements (proxy mode and configuration), and evaluation of the deployment model (monolithic vs distributed).
#### PRE-PROVISIONING PHASE
In this phase, customers provision artefacts for deploying a clean room. Typical considerations for this phase include mechanisms for translating the clean room specification into a deployment template for the trusted computation environment, and mechanisms for associating an attestable identity with this environment to facilitate secure access to protected resources.
#### RESOURCE PROVISIONING PHASE
In this phase, customers configure secure access from the computation environment to their data. Typical considerations for this phase include mechanisms for enabling role-based access to resources from the clean room identity and verifying the clean room attestation before releasing encryption keys from secure storage.

### Execution Stage
#### COMPUTE PROVISIONING PHASE
In this phase, customers deploy clean rooms by rolling out the deployment templates generated above. Typical considerations for this phase include configuration of compute (SKU, networking) and configuration of mechanisms to manage, scale and orchestrate the application/instances.
#### APPLICATION EXECUTION PHASE
In this phase, the customer triggers the application code. Typical considerations for this phase include mechanisms for protection against exfiltration.

### Sample Workflow

```mermaid
sequenceDiagram
title Clean Room - Preparation

actor Customer
participant Tooling
participant Blob
participant AD
participant mHSM
participant AKV

rect Teal
note over Customer,AKV: Data Preparation Phase
    Customer->>+Tooling: Generate DEK
    Tooling-->>-Customer: DEK
    Customer->>+Tooling: Encrypt data with DEK
    Tooling-->>-Customer: Encrypted data
    Customer->>+Blob: Upload (encrypted data)
    Blob-->>-Customer: `
end

rect Teal
note over Customer,AKV: Specification Generation Phase
    Customer->>+Tooling: Generate specification
    Tooling-->>-Customer: `
end

rect Teal
note over Customer,AKV: Pre-Provisioning Phase
    Customer->>+AD: Provision clean room identity
    AD-->>-Customer: Identity details
    Customer->>+Tooling: Translate specification
    Tooling-->-Customer: Deployment template, key release policy
end

rect Teal
note over Customer,AKV: Resource Provisioning Phase
    Customer->>+Tooling: Generate KEK
    Tooling->>+mHSM: Store(KEK, key release policy, clean room identity)
    mHSM-->>-Tooling: `
    Tooling-->>-Customer: `
    Customer->>+Tooling: Wrap DEK
    Tooling->>+AKV: Store(Wrapped DEK, clean room identity)
    AKV-->>-Tooling: `
    Tooling-->>-Customer: `
    Customer->>+Blob: Provision access to encrypted data (clean room identity)
    Blob-->>-Customer: `
end
```

Figure *Sample workflow using Azure Clean Room (preparation stage)*

```mermaid
sequenceDiagram
title Clean Room - Execution

actor Customer
participant Client
participant ACI
participant Clean Room
participant AD
participant mHSM
participant AKV
participant Blob
participant Governance

rect Teal
note over Customer,Governance: Compute Provisioning Phase
    Customer->>+ACI: Deploy template
    ACI->>+Clean Room: `
    Clean Room->>+AD: Get identity token
    AD-->>-Clean Room: Identity token
    Clean Room-->>-ACI: `
    ACI-->>-Customer: `
end

rect Teal
note over Customer, Governance: Application Execution Phase
    Client-)+Clean Room: DoWork()

    Clean Room->>+Governance: Consent/Check()
    Governance-->>-Clean Room: 200 OK

    create participant Application
    Clean Room--)+Application: `

    Clean Room->>+Governance: Audit/RecordAccess(Wrapped DEK)
    Governance-->>-Clean Room: `
    Clean Room->>+AKV: Get(Wrapped DEK, identity token)
    AKV-->>-Clean Room: Wrapped DEK

    Clean Room->>+Governance: Audit/RecordAccess(KEK)
    Governance-->>-Clean Room: `
    Clean Room->>+mHSM: Get(KEK, attestation token)
    note over mHSM: Check Clean Room<br>attestation
    mHSM-->>-Clean Room: KEK

    note over Clean Room: Unwrap DEK

    Clean Room->>+Governance: Audit/RecordAccess(Data)
    Governance-->>-Clean Room: `
    Clean Room->>+Blob: Download(encrypted data)
    Blob-->>-Clean Room: `

    note over Clean Room: Decrypt data with DEK

    Clean Room->>+Governance: Audit/RecordExecution(Application)
    Governance-->>-Clean Room: `
    Clean Room->>+Application: DoWork(clear data)
    Application-->>-Clean Room: `

    destroy Application
    Application--)Clean Room: `

    Clean Room--)-Client: Result
end
```

Figure *Sample workflow using Azure Clean Room (execution stage)*

## Collaboration Workflow

As discussed earlier (“Collaboration”), the Clean Room application architecture enables a zero trust multi-party collaboration workflow where secret data originating from one or more parties (data providers) is presented to opaque code originating from another party (code provider) in a safe computation environment hosted by a different party (solution provider), with the assurance that all the secret data will only be used within this computation and cannot be copied, accessed or misused outside this environment.
Collaboration workflows build upon the Canonical Workflow described earlier and involve similar phases, with additional coordination/agreement requirements across more than one party at every step.
### Preparation Stage
#### DATA PREPARATION PHASE
In this phase, data providers secure the data for collaboration, and it is executed concurrently/independently by each collaborator. Considerations for this phase are the same as those for the single party Data Preparation Phase.
#### CODE PREPARATION PHASE
In this phase, code providers secure the code for collaboration, and it is executed concurrently/independently by each collaborator. Typical considerations for this phase include evaluation of storage requirements for the encrypted code, mechanisms for protection of the code through encryption, and mechanisms for secure storage of the encryption key.
#### SPECIFICATION GENERATION PHASE
In this phase, a collaboration agreement is reached between all the collaborators. Typical considerations for this phase include mechanisms for generation and acceptance of a collaboration contract represented as a Clean Room specification that captures the security requirements (type of the clean room), privacy protection requirements (proxy mode and configuration) and deployment model (monolithic vs distributed) of the collaboration, and handshake mechanisms to facilitate the same.
#### PRE-PROVISIONING PHASE
In this phase, the solution provider provisions artefacts for deploying the clean room executing the collaboration. Considerations for this phase are the same as those for the single party Pre-Provisioning Phase.
#### RESOURCE PROVISIONING PHASE
In this phase, data & code providers configure secure access from the computation environment to their data/code. An additional consideration for this phase from those for the single party Resource Provisioning Phase includes mechanism for enabling access to resources for a cross tenant clean room identity.

### Execution Stage
#### COMPUTE PROVISIONING PHASE
In this phase, the solution provider deploys clean rooms by rolling out the deployment templates generated above. Considerations for this phase are the same as those for the single party Compute Provisioning Phase.
#### APPLICATION EXECUTION PHASE
In this phase, the solution provider or code provider triggers the collaboration code. Additional considerations for this phase from those for the single party Application Execution Phase include mechanisms for the computation environment to enforce the collaboration contract and secure storage of the output of the computation.
###	Post Execution Stage
#### CONSOLIDATION PHASE
In this phase, the solution provider processes completion signal from the computation environment and informs the collaborators. Typical considerations for this phase include mechanisms for ensuring output can only be accessed by authorized parties.
#### TEARDOWN PHASE
In this phase, the computation environment is torn down by the solution provider.
 
3.2.4.	Sample Workflow

Figure 4 3 Sample collaboration workflow using Azure Clean Room (preparation stage)

Figure 4 4 Sample collaboration workflow using Azure Clean Room (execution stage)
