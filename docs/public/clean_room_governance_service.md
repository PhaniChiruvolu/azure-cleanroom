# Clean Room Governance Service
<!-- Audience: Engineering
Prerequisites: Architectural Overview, User Flow -->

Azure Clean Rooms lend themselves well to zero-trust multi-party collaboration on Azure. The Clean Room specification can be used to capture the mutually agreed upon data protection requirements for the collaboration, and the Clean Room tooling can be used to translate this intent into a hardened confidential computation specification. However, from an end-to-end workflow perspective, a mechanism is needed for the collaborators to come together in Azure and co-author the clean room specification before deployment or co-govern the clean room instance after deployment in a tamper proof and auditable manner that meets the zero-trust bar.

Clean Room Governance Service (CGS), a per-collaboration open-sourced application deployed by one of the collaborators in a zero-trust confidential computing environment serves as a confidentially attestable source of truth, exposing secure API for contract management as well as governance.

Modelling this Clean Room Governance Service (CGS) as a Confidential Consortium Framework (CCF) application meets the requirements particularly well. CCF is an open-source framework for building stateful services providing decentralized trust. It enables multiple parties to execute auditable code over confidential data without trusting each other or a privileged operator. CCF provides robust guarantees on transparent governance (consortium), application integrity (hardware-backed integrity for application logic and data) and confidentiality (all transactions are confidential by default). All CCF transactions are reflected in a tamper-proof ledger that can be used to audit governance as well as obtain transaction receipts to verify the consistency of the service and prove the execution of transaction.

## Initialization

```mermaid
sequenceDiagram
title Clean Room Governance Service - Initialization

actor ISV
actor CP
actor DP
participant CCF
participant Constitution
participant CGS
participant KVS

rect Purple
note over ISV,KVS: Initialization

rect Teal
note over ISV,KVS: Consortium - Creation
    %% create participant CCF
    ISV->CCF:Create CCF
    %% create participant KVS
    CCF->KVS: `
    CCF-->ISV:CCF created
    ISV->+CCF:Set constitution
    %% create participant Constitution
    CCF->Constitution: `
    Constitution-->CCF: `
    CCF-->-ISV:Constitution configured
    ISV->+CCF:Deploy Clean Room Governance Service (CGS)
    %% create participant CGS
    CCF->CGS:Deploy App
    CGS-->CCF: `
    CCF-->-ISV: App Configured
end

rect Teal
note over ISV,KVS: Consortium - Establishing quorum
    ISV->+CCF: Add collaborators to consortium
    CCF-->-ISV: Invitations
    ISV->+DP: Share invitation
    note over DP: Validate Constitution
    note over DP: Validate App
    DP->+CCF: Accept invitation
    CCF-->-DP: `
    DP-->-ISV: Accepted
    ISV->+CP: Share invitation
    note over CP: Validate Constitution
    note over CP: Validate App
    CP->+CCF: Accept invitation
    CCF-->-CP: `
    CP-->-ISV: Accepted
end

end
```

Figure *Initializing the Clean Room Governance Service*

The solution provider deploys CGS as a CCF application, where the constitution of the CCF will restrict modifications to the CGS application and the constitution itself. The solution provider subsequently invites all the collaborators to join the consortium.

## Contract Management & Specification Generation Flow

The per-collaboration (Clean Room Governance Service) can readily serve as a secure & attested source of truth for the current state of a shared “contract”, by exposing Contract API for the collaborators to propose, amend and accept contracts and any related assets. This offers a robust mechanism for the generation and acceptance of a collaboration contract represented as a Clean Room specification (Specification Generation Phase).

```mermaid
sequenceDiagram
title Collaboration - Specification Generation Phase
actor ISV
participant Contract
actor CP
actor DP

rect Teal
note over ISV,DP: Specification Generation Phase
    %% create participant Contract
    ISV->+Contract: Propose
    CP->Contract: Amend
    DP->Contract: Amend
    CP->Contract: Approve
    DP->Contract: Approve
    Contract-->ISV: Specification
    destroy Contract
end

```

Figure *Specification generation flow*

### Co-authoring the collaboration contract

```mermaid
sequenceDiagram
title Contract - Generation

actor ISV
actor CP
actor DP
participant CMS
participant KVS

rect Teal
note over ISV,KVS: Specification - Initialize
    note over ISV: Create draft specification
    ISV->+CMS: Contract/Initialize(id, spec)
    CMS->+KVS: kvs["draft"].Set(id, spec)
    KVS-->-CMS:x-ms-ccf-transaction-id
    CMS-->-ISV:x-ms-ccf-transaction-id
end

rect Teal
note over ISV,KVS: Specification - Update
    DP->+CMS: Contract/Fetch(id)
    CMS->+KVS: kvs["draft"].Get(id)
    KVS-->-CMS: spec
    CMS-->-DP: spec, state:"draft"
    note over DP: Update spec
    DP->+CMS: Contract/Amend(id, spec)
    CMS->+KVS: kvs["draft"].Set(id, spec)
    KVS-->-CMS:x-ms-ccf-transaction-id
    CMS-->-DP:x-ms-ccf-transaction-id

    CP->+CMS: Contract/Fetch(id)
    CMS->+KVS: kvs["draft"].Get(id)
    KVS-->-CMS: spec
    CMS-->-CP: spec, state:"draft"
    note over CP: Update spec
    CP->+CMS: Contract/Amend(id, spec)
    CMS->+KVS: kvs["draft"].Set(id, spec)
    KVS-->-CMS:x-ms-ccf-transaction-id
    CMS-->-CP:x-ms-ccf-transaction-id
end

```

Figure *Contract management using Clean Room Governance Service (co-authoring the contract)*

The solution provider initializes a draft clean room specification using the Contract API of CGS. Thereafter, the collaborators iterate over the draft specification and make changes to the data sources and applications to be executed within the Clean Room.

### Finalizing the collaboration contract

```mermaid
sequenceDiagram
title Contract - Finalization

actor ISV
actor CP
actor DP
participant CCF
participant CMS
participant Constitution
participant KVS

rect Purple
note over ISV,KVS: Finalize

rect Teal
note over ISV,KVS: Specification - Finalize
    ISV->+CMS: Contract/Fetch(id)
    CMS->+KVS: kvs["draft"].Get(id)
    KVS-->-CMS: spec
    CMS-->-ISV: spec, state:"draft"

    ISV->+CCF: Propose(id, spec)
    CCF-->+Constitution: CreateProposal(id, spec)
    Constitution->+KVS: kvs["proposed"].Set(id, [spec, proposal_id])
    KVS-->-Constitution: `
    Constitution-->-CCF: `
    CCF-->-ISV: proposal_id

    ISV->+DP: Vote(id)
    ISV->+CP: Vote(id)

    DP->+CMS: Contract/Fetch(id)
    CMS->+KVS: kvs["proposed"].Get(id)
    KVS-->-CMS: [spec, proposal_id]
    CMS-->-DP: spec, state:"proposed", proposal_id

    CP->+CMS: Contract/Fetch(id)
    CMS->+KVS: kvs["proposed"].Get(id)
    KVS-->-CMS: [spec, proposal_id]
    CMS-->-CP: spec, state:"proposed", proposal_id

    note over CP: Verify spec
    note over DP: Verify spec

    CP->+CCF: Accept(proposal_id)
    CCF-->+Constitution: Resolve(proposal_id, votes[])
    Constitution-->-CCF: Pending
    CCF-->-CP: `
    CP-->-ISV: `

    DP->+CCF: Accept(proposal_id)
    CCF-->+Constitution: Resolve(proposal_id, votes[])
    Constitution->+KVS: kvs["accepted"].Set(id, [spec, proposal_id])
    KVS-->-Constitution: `
    Constitution-->-CCF: Accepted
    CCF-->-DP: `
    DP-->-ISV: `
end

rect Teal
note over ISV,KVS: Specification - Consume
    ISV->+CMS: Contract/Fetch(id)
    CMS->+KVS: kvs["accepted"].Get(id)
    KVS-->-CMS: [spec, proposal_id]
    CMS-->-ISV: spec, state:"accepted", proposal_id
end
end
```

Figure *Contract management using Clean Room Governance Service (finalizing the contract)*

Once the collaborators have completed iterating over the specification, the solution provider proposes a “contract” to the CCF containing the agreed upon Clean Room specification. Each collaborator reviews this proposal and verifies that the specification enforces their requirements before accepting the proposal. Once all the collaborators have accepted the proposal, the “contract” is moved to an accepted state and the specification is finalized.

## Deployment template and clean room policy management

Once the “contract” specification has been finalized the solution provider now generates a deployment template and the clean room policy as referred to in the  Pre-Provisioning Phase. The solution provider then proposes this deployment template and policy as the “deployment spec” and “clean room policy” proposals to the CCF that is containing the agreed upon Clean Room specification. Each collaborator reviews these proposals and verifies that the deployment spec and policy correspond to the agreed upon Clean Room specification before accepting the proposals. Once all the collaborators have accepted the proposals, the “deployment spec” and “policy” becomes final. Once finalized these can be used for both resource provisioning and compute provisioning as per the Resource Provisioning Phase and Compute Provisioning Phase.

## Cross tenant identity provisioning

One of the aspects mentioned in the Resource Provisioning Phase is providing a mechanism for enabling access to resources for a cross tenant clean room identity. The Clean Room Governance Service can act as an Identity provider (IdP)/OIDC issuer and one can leverage federated identity credential with external identity provider to create a trust relationship between a user-assigned managed identity in a tenant and CGS as the external identity provider. Thus, each collaborator sets up a user-assigned managed identity in their tenant and configures Federated Credential on that identity, with the issuer URL pointing to an endpoint that exposes the CGS OpenID configuration and token signing keys. Then as part of the Application Execution Phase the clean room instance requests an ID token from CGS. CGS first confirms that the clean room presents a valid attestation report with expected values (as per the agreed upon clean room policy proposal) and on success returns an ID Token. The clean room instance uses the ID token to get access tokens for each of the managed identities in respective tenants.

## Governance Flow

The per-collaboration (Clean Room Governance Service) can readily serve as a secure & attested endpoint satisfying the Governance Considerations discussed earlier. The endpoint is responsible for maintaining tamper proof consent and audit ledger for the Clean Room and is invoked by the Clean Room infrastructure during the application execution phase to meet various governance requirements.

```mermaid
sequenceDiagram
title Clean Room - Application Execution Phase

participant Client
participant Application
participant Clean Room
participant mHSM
participant AKV
participant Blob
participant Governance

rect Teal
note over Client,Governance: Application Execution Phase
    Client->+Clean Room: DoWork()

    Clean Room->+Governance: Consent/Check()
    Governance-->-Clean Room: 200 OK
    %% create participant Application
    Clean Room->+Application: `

    Clean Room->+Governance: Audit/RecordAccess(Wrapped DEK)
    Governance-->-Clean Room: `
    Clean Room->+AKV: Get(Wrapped DEK, identity token)
    AKV-->-Clean Room: Wrapped DEK

    Clean Room->+Governance: Audit/RecordAccess(KEK)
    Governance-->-Clean Room: `
    Clean Room->+mHSM: Get(KEK, attestation token)
    note over mHSM: Check Clean Room attestation
    mHSM-->-Clean Room: KEK

    note over Clean Room: Unwrap DEK

    Clean Room->+Governance: Audit/RecordAccess(Data)
    Governance-->-Clean Room: `
    Clean Room->+Blob: Download(encrypted data)
    Blob-->-Clean Room: `

    note over Clean Room: Decrypt data with DEK

    Clean Room->+Governance: Audit/RecordExecution(Application)
    Governance-->-Clean Room: `
    Clean Room->+Application: DoWork(clear data) 
    Application-->-Clean Room: `
    %% destroy Application

    Clean Room-->Client: Result
end
```

Figure 6 5 Governance flow in Application Execution Phase
<!-- TODO: Add high level flow for the CGS implementation of Consent API & Audit API using CCF infrastructure. -->
