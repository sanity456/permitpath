# Audit record

Status: PASS for the corrected source, local verification, and current StudioNet release.

Contract: PermitDecisionTree

Mechanism: validated acyclic binary tree -> evidence-bounded one-node consensus -> deterministic traversal -> authority uncertainty lane.

## Review-blocker results

- GenVM lint and strict typecheck: PASS
- Direct security and state tests: 11 PASS
- Five-validator GLSim integration tests: 1 PASS
- Leader substantive payload or closed-domain result binding: PASS
- Deterministic post-consensus revalidation before state writes: PASS
- Registry ownership, bounded capacity, and safe reclaim: not applicable; no permissionless fixed-cap operational registry
- Concrete GenVM runner hash on source line 1: PASS
- ABI regenerated from the corrected source: PASS
- Source collection and provenance boundary: PASS
- StudioNet workflow: PASS, 4 finalized successful transactions
- Exact deployed-source byte readback: PASS
- Exact full on-chain schema equality with abi.json: PASS
- Mechanism-specific terminal-state readback: PASS
- Fresh external wallets, no workspace wallet, no other-owner wallet, no cross-repository reuse: PASS
- Submission evidence lock: current address `0x76b24914523dBfF377d1558958613A90Cd2ae4A2`; superseded address `0x587D01515DF8c4A07424700871829Df12E50457F` is historical only

## Residual boundary

No live collection. Guidance trees, project descriptions, and source references are public caller-supplied snapshots and are not authenticated.

It is an informational router, not a permit, code-compliance finding, government decision, or professional advice.
