"""Strict branch-answer validator and state-boundary regressions."""

from tests.direct.test_permit_decision_tree import _answer, _project, _tree


def _prepared(contract, vm, authority, applicant):
    tree_id = _tree(contract, vm, authority)
    project_id = _project(contract, vm, applicant, tree_id)
    return project_id


def test_validator_rejects_out_of_domain_answer(contract, direct_vm, direct_alice, direct_bob):
    project_id = _prepared(contract, direct_vm, direct_alice, direct_bob)
    _answer(contract, direct_vm, direct_bob, project_id, "YES")
    assert direct_vm.run_validator(leader_result={"answer": "MAYBE"}) is False


def test_validator_accepts_honest_answer(contract, direct_vm, direct_alice, direct_bob):
    project_id = _prepared(contract, direct_vm, direct_alice, direct_bob)
    _answer(contract, direct_vm, direct_bob, project_id, "YES")
    assert direct_vm.run_validator() is True


def test_post_consensus_invalid_answer_preserves_project(contract, direct_vm, direct_alice, direct_bob, monkeypatch):
    from genlayer import gl

    project_id = _prepared(contract, direct_vm, direct_alice, direct_bob)
    before = contract.get_project(project_id)
    direct_vm.sender = direct_bob
    monkeypatch.setattr(gl.vm, "run_nondet_unsafe", lambda *args: {"answer": "MAYBE"})
    with direct_vm.expect_revert("invalid_answer"):
        contract.assess_next(project_id)
    assert contract.get_project(project_id) == before
