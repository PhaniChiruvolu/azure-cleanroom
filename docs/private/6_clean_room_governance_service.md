# Clean Room Governance Service
<!-- Audience: Engineering
Prerequisites: Architectural Overview, User Flow -->

Azure Clean Rooms lend themselves well to zero-trust multi-party collaboration on Azure. The Clean Room specification can be used to capture the mutually agreed upon data protection requirements for the collaboration, and the Clean Room tooling can be used to translate this intent into a hardened confidential computation specification.

However, from an end-to-end workflow perspective, there is no ready mechanism for the collaborators to come together in Azure and co-author the clean room specification before
deployment or co-govern the clean room instance after deployment in a tamper proof and auditable manner that meets the zero-trust bar. Nor can such mechanisms be built in a straightforward manner.

Neither the clean room specification as a shared “contract”, nor the governance service as a shared “service” are natural candidates for modelling as traditional Azure Resources. Each collaborator is in a separate AAD tenant by definition, and hence cannot access the other tenant’s resources. While a multi-tenant “Contract RP” or “Governance RP” can in principle project a single resource in AME tenant across multiple customer AAD tenants, this breaks the zero-trust bar as RPs don’t lend themselves well to zero-trust computing given the ARM control plane and RP service code can’t be verified or attested in a confidential manner.

This content has been moved [here](../public/clean_room_governance_service.md).
