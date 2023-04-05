from algosdk.abi import ABIType
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.encoding import decode_address, encode_address
from algosdk.transaction import AssetOptInTxn, PaymentTxn
from beaker import *
from algosdk import *
from algosdk.atomic_transaction_composer import *
from beaker import client, consts, sandbox
from ContractA import (
    contract_a
)
from ContractB import(
    contract_b
)

def demo() -> None:
    accts = sandbox.get_accounts()
    acct = accts.pop()
    member_acct = accts.pop()

    contract_a = client.ApplicationClient(
        sandbox.get_algod_client(), contract_a, signer=acct.signer
    )
    contract_b = client.ApplicationClient(
        sandbox.get_algod_client(), contract_b, signer=acct.signer
    )
    print("Creating app")
    contract_a.create()
    contract_b.create()
    sp = contract_a.get_suggested_params()
    sp_b = contract_b.get_suggested_params()

     ##
    # Bootstrap Club app
    ##
    print("Bootstrapping app")
    sp = contract_a.get_suggested_params()
    sp.flat_fee = True
    sp.fee = 2000
    ptxn = PaymentTxn(
        acct.address,
        sp,
        contract_a.app_addr,
        99999999
    )

    contract_a.call(
        "bootstrap",
        seed=TransactionWithSigner(ptxn, acct.signer),
        token_name="fight club",
        boxes=[(contract_a.app_id, "affirmations")] * 8,
    )

    atc = AtomicTransactionComposer() 

    with open("./ContractB.json") as f:
        js = f.read()
    contract = abi.Contract.from_json(js)
    atc.add_method_call(
        app_id=contract_b.app_id,
        # contract_b.get_method_by_name("add")
        sender=acct.address,
        sp=sp_b,
        #signer=contract_a.get_signer(),
        # how do we get signer?
        method_args=[1, 1]
    )
if __name__ == "__main__":
    demo()