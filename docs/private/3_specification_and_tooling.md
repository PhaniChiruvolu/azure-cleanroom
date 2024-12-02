# Specification & Tooling

As discussed earlier, the Clean Room application architecture allows customers to operate with a simplified grammar that captures the desired data protection intent as a Clean Room specification.

## Specification

This content has been moved [here](../public/specification.md).

## Tooling

This content has been moved [here](../public/tooling.md).

## Frequently Asked Questions
<!-- TODO: Scrub this section. -->

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
