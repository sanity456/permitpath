"""Direct tests for forward-only permit tree traversal."""

import json


TREE = json.dumps({"nodes": [
    {"id": "ROOT", "question": "Does the project explicitly add or enlarge a permanent enclosed structure?", "yes": "ROUTE:BUILDING", "no": "N2"},
    {"id": "N2", "question": "Does the project explicitly alter fixed electrical wiring or a service panel?", "yes": "ROUTE:ELECTRICAL", "no": "ROUTE:INFORMATION_ONLY"},
]})
DESCRIPTION = "The public project description says a new enclosed storage room will be added to the existing house."


def _tree(contract, vm, authority):
    vm.sender = authority
    return contract.publish_tree("HOME", "Illustrative local home-project guidance snapshot.", TREE, "municipal-guidance-copy")


def _project(contract, vm, applicant, tree_id):
    vm.sender = applicant
    return contract.open_project("P1", tree_id, DESCRIPTION)


def _answer(contract, vm, applicant, project_id, answer):
    vm.sender = applicant
    vm.mock_llm(r".*Answer one frozen permit-routing question.*", json.dumps({"answer": answer}))
    return contract.assess_next(project_id)


def test_publishes_forward_tree(contract, direct_vm, direct_alice):
    tree_id = _tree(contract, direct_vm, direct_alice)
    assert contract.get_tree(tree_id)["tree_sha256"].startswith("sha256:")


def test_rejects_backward_edge(contract, direct_vm, direct_alice):
    bad = json.dumps({"nodes": [{"id": "A", "question": "This question is intentionally long enough to be valid?", "yes": "B", "no": "ROUTE:NONE"}, {"id": "B", "question": "This second question is intentionally long enough to be valid?", "yes": "A", "no": "ROUTE:NONE"}]})
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("tree_must_be_forward_only"):
        contract.publish_tree("BAD", "Illustrative jurisdiction note.", bad, "source")


def test_current_question_view(contract, direct_vm, direct_alice, direct_bob):
    tree_id = _tree(contract, direct_vm, direct_alice)
    project_id = _project(contract, direct_vm, direct_bob, tree_id)
    assert "enclosed structure" in contract.get_current_question(project_id)


def test_only_applicant_assesses(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    tree_id = _tree(contract, direct_vm, direct_alice)
    project_id = _project(contract, direct_vm, direct_bob, tree_id)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_applicant"):
        contract.assess_next(project_id)


def test_yes_reaches_terminal_route(contract, direct_vm, direct_alice, direct_bob):
    tree_id = _tree(contract, direct_vm, direct_alice)
    project_id = _project(contract, direct_vm, direct_bob, tree_id)
    assert _answer(contract, direct_vm, direct_bob, project_id, "YES") == "YES"
    assert contract.get_project(project_id)["route"] == "BUILDING"


def test_unclear_requires_authority(contract, direct_vm, direct_alice, direct_bob):
    tree_id = _tree(contract, direct_vm, direct_alice)
    project_id = _project(contract, direct_vm, direct_bob, tree_id)
    _answer(contract, direct_vm, direct_bob, project_id, "UNCLEAR")
    direct_vm.sender = direct_alice
    contract.resolve_unclear(project_id, "YES", "Authority resolves the frozen root question from the submitted description.")
    assert contract.get_project(project_id)["route"] == "BUILDING"


def test_cancel_open_project(contract, direct_vm, direct_alice, direct_bob):
    tree_id = _tree(contract, direct_vm, direct_alice)
    project_id = _project(contract, direct_vm, direct_bob, tree_id)
    direct_vm.sender = direct_bob
    contract.cancel_project(project_id)
    assert contract.get_project(project_id)["state"] == "CANCELLED"


def test_invalid_answer_preserves_state(contract, direct_vm, direct_alice, direct_bob):
    tree_id = _tree(contract, direct_vm, direct_alice)
    project_id = _project(contract, direct_vm, direct_bob, tree_id)
    with direct_vm.expect_revert("[LLM_ERROR] invalid_answer"):
        _answer(contract, direct_vm, direct_bob, project_id, "MAYBE")
    assert contract.get_project(project_id)["state"] == "ASSESSING"
