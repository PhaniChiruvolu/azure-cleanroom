# *Data Protection with a Clean Room*
<!--
This section provides an overview of the progression of mechanisms for protecting customers’ private data from exfiltration in a public cloud infrastructure and presents the Clean Room as the next stage in this evolutionary process.
-->
<!--TODO: Add links to all the offerings/technologies mentioned in this file.-->
Data is the core asset that customers seek to protect.

In an on-premises model, data is typically protected by controlling access to the data by operators (identity) and computers (isolated networks). To provide greater protection, data is often encrypted at rest (physical theft) and any remote access is additionally protected through a network firewall (network theft).

## PROTECTING PRIVATE DATA IN A PUBLIC CLOUD

Traditional data protection mechanisms are not readily applicable in a public cloud system. Here, data resides outside the customer premises in a shared environment data center, and customers cannot exercise control either on the physical access to the data center servers and network infrastructure, or on network access within the data center. This is a deterrent for customers to move to the public cloud and take advantage of all its other benefits.

Microsoft as a trusted cloud provider already offers a wide range of mechanisms for customers to protect their data in our public cloud infrastructure. Microsoft cloud infrastructure isolates customers from each other by design and ensures one customer cannot access other customers’ resources. Data is encrypted at rest by the storage servers with a key that is supplied by the customer. Customers can further lock down resources to only be accessed within a virtual network, enabling a “private” network within the public cloud. Robust access control mechanisms further ensure only authorized operators can access these resources.

However, all these mechanisms require a high degree of trust in the Microsoft cloud infrastructure – hardware, software, and operators. Any customer requiring a zero-trust model in the public cloud needs to necessarily adopt Confidential Computing.

Confidential Computing realizes remotely attestable trusted execution environments (TEE), using secrets embedded in the AMD/Intel CPUs to protect code and data within the environment from being tampered or exfiltrated. These secrets are not accessible to any code or person outside the hardware, enabling mechanisms in the public cloud to start with zero-trust and build a trust chain using these embedded secrets as the root of trust.

This enables an ecosystem where customer data can be encrypted with a key that is never shared with the cloud provider. The key can instead be stored in a trusted key management service that securely releases it to an endpoint after verifying that it is executing within a TEE that meets the attestation requirements.

## CREATING A TRUSTED EXECUTION ENVIRONMENT

However, there is a significant entry barrier to natively adopting confidential computing in line of business applications, and this is a deterrent for customers to leverage it as part of moving their data and the associated applications to the public cloud.

Microsoft, through the Azure Confidential Computing (ACC) ecosystem, offers multiple mechanisms to lower this entry barrier and enable the adoption of confidential computing.
Virtual Machines hosted on Azure hosts with AMD SEV-SNP/Intel TDX CPUs allow applications within to run largely unmodified as the virtual machine itself is completely protected. This significantly reduces the complexity from the deep awareness mandated by the Intel SGX paradigm to create a trusted execution environment.

The Confidential Virtual Machine (C-VM) offering builds on top of this and enables an out of the box trusted execution environment, where the public cloud infrastructure is kept out of the trust boundary and only a minimal footprint of infrastructure specific code is hosted within the VM as part of the trusted code base (TCB).

Container computation through AKS/ACI further reduces the burden by hosting customer applications as containers within a Microsoft maintained open-source OS and container runtime, allowing the application developers to focus on their business logic.

A collection of Microsoft published open-source sidecars reduces the burden further by abstracting the ACC ecosystem and underlying details such as secure key release from the container(s) executing the business logic.

## MAINTAINING A TRUSTED CODE BASE

Generating a robust measurement of the trusted execution environment (TEE) is a challenge. An attestation report containing this measurement and signed by the CPU needs to be consumed as part of the policies governing release of secrets from the secure key management services. Any change in the trusted code base (TCB) to be executed within the TEE would update the binaries that are executed within the TEE, changing the measurement of the TEE. This in turn causes the key release policy checks to fail and break the application, making the system very fragile.

Code Transparency Service seeks to address this challenge by abstracting away the exact measurement of the binaries being executed within the TEE. Instead, a bootstrap mechanism within the TEE can ensure that the binaries come from a trusted and governed customer-specified code repository. The attestation report can now contain a measurement of just this bootstrap mechanism and its configuration parameters like repository details, enabling robust key release policies if CTS satisfies the trust requirements.

One can also make a case for similar bootstrap mechanisms enforcing digital signature with a customer specified key for application binaries. If this enforcement suffices for the customer’s trust requirements, it enables customers to continue generating their applications using existing dev-ops workflows producing “signed” binaries and consume those within a TEE without any (significant) additional burden on the application developer.

## TRANSLATING INTENT TO A HARDENED CONFIGURATION

The ACC ecosystem lowers the entry barrier for customers to protect data in the Microsoft public cloud using confidential computing significantly. However, customers are still required to develop a deep understanding of the confidential computation infrastructure, as they need to translate their data protection intent into a reliable TCB, a secure TEE configuration measured in a robust attestation report and a strict key release policy enforcing the desired protection. Any misconfiguration of this system completely nullifies data protection guarantees, making it necessary for the customer to acquire expertise in an area that has a steep learning curve and is unlikely to be relevant for their core business on a regular basis.

A “Clean Room”, an application architecture that hosts customer applications requiring data protection within a standardized privacy preserving infrastructure, can address these concerns. It allows customers to operate with a simplified specification/grammar that captures the desired data protection intent while abstracting away details of confidential computation. The open-source infrastructure and associated tooling take over the burden of translating this intent into a hardened confidential computation configuration enforcing the desired zero-trust protection.

In a “Clean Room”, the responsibility of ensuring that customer data is not accessible outside the confidential TEE moves from the application code to the infrastructure. This includes the responsibility of protecting customers against any faulty code executing within the TEE accidentally exfiltrating their data. Given these requirements, the infrastructure effectively treats the customers’ application as opaque/untrusted code and executes the same within a sandbox enforcing the desired protection.

## COLLABORATION

Multi-party data collaboration (collaboration) consists of a computation environment where data originating from one or more parties (data providers) is presented to code originating from another party (code provider). This code processes the presented data and generates insights or transformed data that are subsequently consumed by some of the parties involved.

Data is a protected asset for almost all collaboration scenarios, and every data provider requires assurance that their data will only be used within this computation environment and only for the agreed purpose. The code provider, other data providers and the party hosting the computation environment (solution provider) should not be able to copy, access or misuse this protected data outside the agreed upon collaboration.

Confidential computing enables computation environments providing this assurance, as the data provider assets can be protected by an encryption key that is only released to a trusted execution environment. Trust can be established through measurement of the TEE, ensuring that the code provider is only injecting code agreed upon beforehand, and the solution provider is not able to view/exfiltrate sensitive data.

However, agreeing upon the injected code is not possible in many collaboration scenarios, especially if the code itself is a protected asset and constitutes the code providers’ Intellectual Property, presenting an additional challenge to the confidential computing adoption challenges that have already been discussed so far.

A computation environment leveraging the “Clean Room” architecture would largely address this challenge as well and enable a zero trust multi-party collaboration workflow. The inherent ability of the “Clean Room” to execute opaque code within a trusted infrastructure enforcing data protection policies allows for the creation of safe computation environments where multiple customers can inject opaque code and secret data, while still assuring the data provider that “their data will only be used within this computation environment”.

Extensions to the “Clean Room” infrastructure strictly enforce a pre-agreed collaboration contract, assuring the data provider that their data is used “only for the agreed purpose”. Corresponding extensions to tooling capture this collaboration intent and translate into “Clean Room” specification/grammar and eventually a hardened confidential computation configuration enforcing the desired zero-trust protection.
