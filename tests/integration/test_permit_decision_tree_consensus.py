import hashlib
import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context(fragment, response):
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {fragment: json.dumps(response)}},
    )
    return {
        "validators": [validator.to_dict() for validator in validators],
        "genvm_datetime": "2026-08-25T12:00:00Z",
    }


def _deploy(contract_file, owner_account):
    factory = get_contract_factory(
        contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / contract_file
    )
    receipt = factory.deploy_contract_tx(
        args=[],
        account=owner_account,
        wait_transaction_status=TransactionStatus.FINALIZED,
    )
    _ok(receipt)
    return factory, extract_contract_address(receipt)


def _send(method, args, context=None):
    if context is None:
        receipt = method(args=args).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    else:
        receipt = method(args=args).transact(
            transaction_context=context,
            wait_transaction_status=TransactionStatus.FINALIZED,
        )
    _ok(receipt)
    return receipt


def test_five_validator_forward_tree_route_flow():
    authority_account, applicant_account = create_accounts(2)
    factory, address = _deploy("permit_decision_tree.py", authority_account)
    authority = factory.build_contract(address, account=authority_account)
    applicant = factory.build_contract(address, account=applicant_account)
    tree_id = f"{str(authority_account.address).lower()}:HOME"
    project_id = f"{str(applicant_account.address).lower()}:P1"
    tree = json.dumps({"nodes": [
        {"id": "ROOT", "question": "Does the project explicitly add or enlarge a permanent enclosed structure?", "yes": "ROUTE:BUILDING", "no": "N2"},
        {"id": "N2", "question": "Does the project explicitly alter fixed electrical wiring or a service panel?", "yes": "ROUTE:ELECTRICAL", "no": "ROUTE:INFORMATION_ONLY"},
    ]})
    description = "The public project description says a new enclosed storage room will be added to the existing house."
    _send(authority.publish_tree, ["HOME", "Illustrative local home-project guidance snapshot.", tree, "municipal-guidance-copy"])
    _send(applicant.open_project, ["P1", tree_id, description])
    _send(applicant.assess_next, [project_id], _context("Answer one frozen permit-routing question", {"answer": "YES"}))
    project = applicant.get_project(args=[project_id]).call()
    assert project["state"] == "ROUTED"
    assert project["route"] == "BUILDING"
