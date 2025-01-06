# User Flow
<!--
    This section provides an overview of end-to-end customer flows leveraging a clean room for processing sensitive data in the public cloud.
    Audience: Engineering & PM
    Prerequisites: Architectural Overview
-->

## Canonical Workflow

The workflow for storing sensitive data in the public cloud and consuming it from an application executing within a Clean Room involves multiple phases.

```mermaid
flowchart LR
%%   A@{ shape: manual-file, label: "File Handling"}
%%   B@{ shape: manual-input, label: "User Input"}
%%   C@{ shape: docs, label: "Multiple Documents"}
%%   D@{ shape: procs, label: "Process Automation"}
%%   E@{ shape: paper-tape, label: "Paper Records"}

    subgraph DataPrep [Prepare Data]
        _1@{ shape: notch-rect, label: "Publish (secured) data to be processed inside the clean room." }
        %% direction TB
        %% _1@{ shape: braces, label: "Secure data to processed inside the clean room." }
        %% B --> C --> B1Z@{shape: cyl, label: "Database"}
    end
    subgraph CodePrep [Application Preparation]
        _2@{ shape: notch-rect, label: "Publish application to be executed inside the clean room." }
        %% direction TB
        %% D --> E
    end
    subgraph GenerateSpec [Specification Generation]
        _3@{ shape: notch-rect, label: "Author clean room specification." }
    end
    subgraph PreProvision [Pre Provisioning]
        _4@{ shape: notch-rect, label: "Provision artefacts for deploying a clean room." }
    end
    subgraph ResourceProvision [Resource Provisioning]
        _5@{ shape: notch-rect, label: "Configure secure access from clean room to data." }
    end
    subgraph ComputeProvision [Compute Provisioning]
        _6@{ shape: notch-rect, label: "Deploy clean room." }
    end
    subgraph Execution [Application Execution]
        _7@{ shape: notch-rect, label: "Launch application inside clean room." }
    end

%%   subgraph Workflow
%%     direction TB
%%   end
%%   AA@{ shape: circle, label: "Start" } -->|run| Workflow
%%   AIO@{ shape: lean-r, label: "Input/Output" } --o|test| Workflow
%%   Workflow ==> Z@{ shape: stadium, label: "Terminal point" }
  Start@{shape: circle, label: "Start"}
  Start -.-> DataPrep & CodePrep-.-> GenerateSpec
%%   CodePrep -.-> GenerateSpec
  GenerateSpec -.-> PreProvision
  PreProvision -.-> ResourceProvision
  ResourceProvision -.-> ComputeProvision
  ComputeProvision -.-> Execution
  Finish@{shape: stadium, label: "Application" }
  Execution -.-> Finish
```

```mermaid
stateDiagram-v2
    direction TB
    DataPrep: Data Preparation
    CodePrep: Code Preparation
    GenerateSpec: Specification Generation
    PreProvision: Pre Provisioning
    ResourceProvision: Resource Provisioning

    [*] --> DataPrep
    state DataPrep {
        [*] --> [*]
    }
    note right of DataPrep
        Secure data to processed inside the clean room.
    end note

    state CodePrep {
        [*] --> [*]
    }
    note left of CodePrep
        Secure code to processed inside the clean room.
    end note

    state GenerateSpec {
        [*] --> [*]
    }
    note right of GenerateSpec
        Author clean room specification.
    end note

    state PreProvision {
        [*] --> [*]
    }
    note left of PreProvision
        Provision artefacts for deploying a clean room.
    end note

    state ResourceProvision {
        [*] --> [*]
    }
    note left of ResourceProvision
        Configure secure access from the computation environment to data.
    end note

    DataPrep --> CodePrep
    CodePrep --> GenerateSpec
    GenerateSpec --> PreProvision
    PreProvision --> ResourceProvision
    ResourceProvision --> [*]
```

### Preparation Stage

#### DATA PREPARATION PHASE

In this phase, customers secure the data to be processed inside the clean room. Typical considerations for this phase include evaluation of storage requirements for the encrypted data, mechanisms for protection of the data through encryption, and mechanisms for secure storage of the encryption key.

```mermaid
sequenceDiagram
title Data Preparation Phase

box green Customer Premises
    actor Customer
    participant Tooling
end

box brown Public Cloud
    participant Blob as Cloud Storage
end

Customer->>+Tooling: Generate DEK
Tooling--)-Customer: DEK
Customer->>+Tooling: Upload(data, DEK)
Tooling--)Tooling: Encrypt data using DEK
Tooling->>+Blob: Encrypted data
Blob--)-Tooling: <br>
Tooling--)-Customer: <br>
```

#### CODE PREPARATION PHASE

In this phase, code providers secure the code for collaboration, and it is executed concurrently/independently by each collaborator. Typical considerations for this phase include evaluation of storage requirements for the encrypted code, mechanisms for protection of the code through encryption, and mechanisms for secure storage of the encryption key.

```mermaid
sequenceDiagram
title Code Preparation Phase

box green Customer Premises
    actor Customer
    participant Tooling
end

box brown Public Cloud
    participant Blob as Cloud Storage
    participant ACR as Application<br>Registry
end

Customer->>+ACR: Publish application
ACR--)-Customer: Container details

Customer->>+Tooling: Generate DEK
Tooling--)-Customer: DEK
Customer->>+Tooling: Upload(secret sauce, DEK)
Tooling--)Tooling: Encrypt secret sauce using DEK
Tooling->>+Blob: Encrypted secret sauce
Blob--)-Tooling: <br>
Tooling--)-Customer: <br>

```

#### SPECIFICATION GENERATION PHASE

In this phase, customers author specification of clean room(s) that should have access to the secured data. Typical considerations for this phase include evaluation of the security requirements (type of the clean room), evaluation of the privacy protection requirements (proxy mode and configuration), and evaluation of the deployment model (monolithic vs distributed).

```mermaid
sequenceDiagram
title Specification Generation Phase

box green Customer Premises
    actor Customer
    participant Tooling
end

box brown Public Cloud
    participant AD as Azure<br>Active Directory
end

Customer-->>+Tooling: Initialize<br>Specification

Customer->>+AD: Provision clean room identity
AD--)-Customer: Identity details
Customer->>Tooling: Add identity details

Customer->>Tooling: Add application registry details
Customer->>Tooling: Add secret sauce details
Customer->>Tooling: Add endpoint details

loop 
Customer->>Tooling: Add data source details
Customer->>Tooling: Add data sink details
end

Tooling--)-Customer: Clean Room<br>Specification

```

#### PRE-PROVISIONING PHASE

In this phase, customers provision artefacts for deploying a clean room. Typical considerations for this phase include mechanisms for translating the clean room specification into a deployment template for the trusted computation environment, and mechanisms for associating an attestable identity with this environment to facilitate secure access to protected resources.

```mermaid
sequenceDiagram
title Pre-Provisioning Phase

box green Customer Premises
    actor Customer
    participant Tooling
end

box brown Public Cloud
    participant MCR as Clean Room<br>Registry
end

Customer->>+Tooling: Translate specification
Tooling->>+MCR: Get<br>infrastructure<br>details
MCR--)-Tooling: Infrastructure<br>details
note over Tooling: Generate<br>deployment template
note over Tooling: Generate<br>key release policy
Tooling--)-Customer: Deployment template,<br>key release policy
```

#### RESOURCE PROVISIONING PHASE

In this phase, customers configure secure access from the computation environment to their data. Typical considerations for this phase include mechanisms for enabling role-based access to resources from the clean room identity and verifying the clean room attestation before releasing encryption keys from secure storage.

```mermaid
sequenceDiagram
title Resource Provisioning Phase

box green Customer Premises
    actor Customer
    participant Tooling
end

box purple Confidential
    participant mHSM as Azure<br>mHSM
end

box brown Public Cloud
    participant Blob as Cloud Storage
    participant AKV as Azure<br>Key Vault
end


    Customer->>+Tooling: Generate KEK
    Tooling->>+mHSM: Store KEK<br>(key release policy,<br>clean room identity)
    mHSM--)-Tooling:<br>
    Tooling--)-Customer:<br>
    Customer->>+Tooling: Wrap DEK
    Tooling->>+AKV: Store Wrapped DEK<br>(clean room identity)
    AKV--)-Tooling: <br>
    Tooling--)-Customer: <br>
    Customer->>+Blob: Provision access<br>(clean room identity)
    Blob-->>-Customer: <br>
```

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

### Post Execution Stage

#### CONSOLIDATION PHASE

In this phase, the solution provider processes completion signal from the computation environment and informs the collaborators. Typical considerations for this phase include mechanisms for ensuring output can only be accessed by authorized parties.

#### TEARDOWN PHASE

In this phase, the computation environment is torn down by the solution provider.

### Sample Collaboration Workflow

```mermaid
sequenceDiagram
title Collaboration - Preparation

actor CP
actor DP
participant Tooling
participant Contract
actor ISV
participant AD
participant Blob
participant AKV
participant mHSM


rect Teal
note over CP,mHSM: Data Preparation Phase
    note over DP: Generate DataDEK
    note over DP: Encrypt data
    DP->>+Blob: Upload(encrypted data)
    Blob-->>-DP: `
end

rect Teal
note over CP,mHSM: Code Preparation Phase
    note over CP: Generate CodeDEK
    note over CP: Encrypt code
    CP->>+Blob: Upload(encrypted code)
    Blob-->>-CP: `
end

rect Teal
note over CP,mHSM: Specification Generation Phase
    %% create participant Contract
    ISV->>+Contract: Propose
    CP->>Contract: Amend
    DP->>Contract: Amend
    CP->>Contract: Approve
    DP->>Contract: Approve
    %% destroy Contract
    Contract-->>-ISV: Specification
end

rect Teal
note over CP,mHSM: Pre-Provisioning Phase
    %% create participant Tooling
    ISV->>+Tooling: Translate specification
    %% destroy Tooling
    Tooling-->>-ISV: Deployment template, key release policy
    ISV->>+AD: Provision identity
    AD-->>-ISV: clean room identity
end

rect Teal
note over CP,mHSM: Resource Provisioning Phase
    ISV->>+CP: Provision resources(key release policy, clean room identity)
    ISV->>+DP: Provision resources(key release policy, clean room identity)
    note over CP: Verify key release policy
    note over DP: Verify key release policy
    note over CP: Generate CodeKEK
    note over DP: Generate DataKEK
    CP->>+mHSM: Store(CodeKEK, key release policy, clean room identity)
    mHSM-->>-CP: `
    DP->>+mHSM: Store(DataKEK, key release policy, clean room identity)
    mHSM-->>-DP: `
    note over CP: Wrap CodeDEK
    CP->>+AKV: Store(Wrapped CodeDEK, clean room identity)
    AKV-->>-CP: `
    note over DP: Wrap DataDEK
    DP->>+AKV: Store(Wrapped DataDEK, clean room identity)
    AKV-->>-DP: `
    CP->>+Blob: Provision access to encrypted code (clean room identity)
    Blob-->>-CP: `
    CP-->>-ISV: `
    DP->>+Blob: Provision access to encrypted data (clean room identity)
    Blob-->>-DP: `
    DP-->>-ISV: `
end
```

Figure *Sample collaboration workflow using Azure Clean Room (preparation stage)*

```mermaid
sequenceDiagram
title Collaboration - Execution

actor ISV
participant Client
%% participant Application
participant ACI
participant Clean Room
participant AD
participant mHSM
participant AKV
participant Blob
participant Governance

rect Teal
note over ISV,Governance: Compute Provisioning Phase
    ISV->>+ACI: Deploy template
    ACI->>+Clean Room: `
    Clean Room->>+AD: Get identity token
    AD-->>-Clean Room: Identity token
    Clean Room-->>-ACI: `
    ACI-->>-ISV: `
end

rect Teal
note over ISV,Governance: Application Execution Phase
    Client->>+Clean Room: DoWork()
    
    Clean Room->>+Governance: Consent/Check()
    Governance-->>-Clean Room: 200 OK

    Clean Room->>+Governance: Audit/RecordAccess(Wrapped CodeDEK)
    Governance-->>-Clean Room: `
    Clean Room->>+AKV: Get(Wrapped CodeDEK, identity token)
    AKV-->>-Clean Room: Wrapped CodeDEK

    Clean Room->>+Governance: Audit/RecordAccess(Wrapped CodeKEK)
    Governance-->>-Clean Room: `
    Clean Room->>+mHSM: Get(CodeKEK, attestation token)
    note over mHSM: Check attestation
    mHSM-->>-Clean Room: CodeKEK

    note over Clean Room: Unwrap CodeDEK

    Clean Room->>+Governance: Audit/RecordAccess(Code)
    Governance-->>-Clean Room: `
    Clean Room->>+Blob: Download(encrypted code)
    Blob-->>-Clean Room: `
    
    note over Clean Room: Decrypt code

    create participant Application
    Clean Room->>+Application: `

    Clean Room->>+Governance: Audit/RecordAccess(Wrapped DataDEK)
    Governance-->>-Clean Room: `
    Clean Room->>+AKV: Get(Wrapped DataDEK, identity token)
    AKV-->>-Clean Room: Wrapped DataDEK

    Clean Room->>+Governance: Audit/RecordAccess(Wrapped DataKEK)
    Governance-->>-Clean Room: `
    Clean Room->>+mHSM: Get(DataKEK, attestation token)
    note over mHSM: Check Clean Room attestation
    mHSM-->>-Clean Room: DataKEK

    note over Clean Room: Unwrap DataDEK

    Clean Room->>+Governance: Audit/RecordAccess(Data)
    Governance-->>-Clean Room: `
    Clean Room->>+Blob: Download(encrypted data)
    Blob-->>-Clean Room: `

    note over Clean Room: Decrypt data

    Clean Room->>+Governance: Audit/RecordExecution(Application)
    Governance-->>-Clean Room: `
    Clean Room->>+Application: DoWork(clear data)
    Application-->>-Clean Room: Result
    destroy Application
    Clean Room--xApplication: `
    Clean Room-->>-Client: Result
end
```

Figure *Sample collaboration workflow using Azure Clean Room (execution stage)*

<!-- markdownlint-configure-file {
    "no-duplicate-heading": {
        "siblings_only": true
    }
} -->