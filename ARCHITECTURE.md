# Architecture

Project: PermitDecisionTree

Reusable primitive: validated acyclic binary tree -> evidence-bounded one-node consensus -> deterministic traversal -> authority uncertainty lane.

The contract separates caller-attested public inputs, validator-agreed semantic fields, deterministic state transitions, and role-bound final actions. It stores canonical JSON strings in GenVM maps, validates every identifier and bound before consensus, and keeps source references explicitly unverified.

The mechanism is not a renamed assessment record. Its state transitions, role topology, storage layout, deterministic algorithm, and public ABI are specific to this project.

<!-- correction-release-start -->
## Consensus and storage safety boundary

Each model answer is canonicalized against the exact answer set of the active frozen node both inside the validator and after consensus, so a shape-valid but node-invalid answer cannot advance the tree.

The on-chain state transition consumes only the canonical value returned by the post-consensus binding boundary. This contract does not expose a shared permissionless fixed-cap operational registry.
<!-- correction-release-end -->
