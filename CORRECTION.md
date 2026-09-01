# Correction and release record

Repository: permitpath

Contract: PermitDecisionTree

Corrected release verified: 2026-09-01T09:16:26.694646Z

## Findings applied

This repository was checked against both steward findings from the rejected Boxcomplete and Baggate submissions:

1. A leader-provided digest is not proof of its attached substantive payload. Every result that affects state must be canonicalized, independently compared, and rebound after consensus.
2. A shared permissionless registry with fixed global capacity can be captured or exhausted. Operational catalogs must be explicitly owner-scoped, bounded per catalog, or safely reclaimable.
3. Corrected repository source is insufficient when the submitted Studio/Explorer address still runs an earlier build. The active address, deployed source, ABI, transaction, and evidence URLs must identify one release.

## Contract-specific correction

Each model answer is canonicalized against the exact answer set of the active frozen node both inside the validator and after consensus, so a shape-valid but node-invalid answer cannot advance the tree.

## Verified release lock

Current StudioNet address: 0x76b24914523dBfF377d1558958613A90Cd2ae4A2

Deployment transaction: 0xed026a900f672883e30805aa8bf83ae478f8ce54c74ade145d88200e562b9ec9

Source SHA-256: ff07deae57b782c8e6a986c799897bc007b13c0ab550d60913c9607a69b461e2

Superseded address: 0x587D01515DF8c4A07424700871829Df12E50457F

The deployment manifest records exact byte-for-byte source readback, exact full ABI/schema equality, successful finalized execution for all 4 release transactions, role-separated external wallets, and the final state observed from StudioNet. The superseded address is historical only and must not be used in a new submission.

## Regression evidence

GenVM lint and strict typecheck: pass

Direct tests: 11 pass

Five-validator integration tests: 1 pass

Leader-payload or post-consensus injection regression tests: pass

Registry isolation and reclaim tests: not applicable

## Review boundary

No live collection. Guidance trees, project descriptions, and source references are public caller-supplied snapshots and are not authenticated.

It is an informational router, not a permit, code-compliance finding, government decision, or professional advice.

This record documents the implemented controls and verified release. It does not promise a particular human review outcome.
