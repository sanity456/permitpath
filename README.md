# PermitDecisionTree

A reusable forward-only authority tree where validators answer one frozen project question per step, code follows the branch, and only the publishing authority can resolve an unclear node.

The repository is standalone and the contract is reusable: one deployment can hold multiple independent records for unrelated callers. It has no frontend and moves no funds.

## Native mechanism

validated acyclic binary tree -> evidence-bounded one-node consensus -> deterministic traversal -> authority uncertainty lane.

## Actors

tree publisher, project applicant, GenLayer validators.

## Source boundary

No live collection. Guidance trees, project descriptions, and source references are public caller-supplied snapshots and are not authenticated.

## Safety boundary

It is an informational router, not a permit, code-compliance finding, government decision, or professional advice.

All inputs and results are public. Untrusted public data is delimited in prompts and cannot change the closed response schema. A malformed or non-consensus model result fails without committing the intended state transition.

## Verification

    genvm-lint check contracts/permit_decision_tree.py
    genvm-lint typecheck contracts/permit_decision_tree.py --strict
    python -m pytest tests/direct -q -p no:cacheprovider
    python tests/run_glsim.py --port 4000 --validators 5 --no-browser
    python -m pytest tests/integration -q -s -p no:cacheprovider

See ARCHITECTURE.md, SECURITY.md, SOURCE_PROVENANCE.md, AUDIT.md, SUBMISSION_CHECKLIST.md, and deployments/studionet.json.

MIT licensed.

<!-- correction-release-start -->
## Corrected release integrity

The full twelve-repository correction audit applied both steward findings to this contract. Each model answer is canonicalized against the exact answer set of the active frozen node both inside the validator and after consensus, so a shape-valid but node-invalid answer cannot advance the tree.

The current StudioNet release is `0x76b24914523dBfF377d1558958613A90Cd2ae4A2`. Its source bytes and full schema were read back from StudioNet and matched this repository exactly. Use `CORRECTION.md`, `REVIEW_RESPONSE.txt`, and the commit-pinned `deployments/studionet.json` for submission evidence; do not reuse the superseded address `0x587D01515DF8c4A07424700871829Df12E50457F`.
<!-- correction-release-end -->
