from algosdk.abi import ABIType
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.encoding import decode_address, encode_address
from algosdk.transaction import AssetOptInTxn, PaymentTxn
from beaker import *
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

    contract_a.call(
        "make_global_box",
        new_member="global_counter",
        value=1,
        suggested_params=sp,
        boxes=[(contract_a.app_id, "global_counter")]
    )


    result = contract_a.call(
        "read_global_box",
        member="global_counter",
        boxes=[(contract_a.app_id, "global_counter")],
    )
    print("Global box created with value: " + str(result.return_value))

    contract_a.call(
        "set_global_box",
        member="global_counter",
        value=8,
        suggested_params=sp,
        boxes=[(contract_a.app_id, "global_counter")]
    )

    result = contract_a.call(
        "read_global_box",
        member="global_counter",
        boxes=[(contract_a.app_id, "global_counter")],
    )
    print("Global box set to value: " + str(result.return_value))

    contract_a.call(
        "increment_global_box",
        member="global_counter",
        suggested_params=sp,
        boxes=[(contract_a.app_id, "global_counter")]
    )

    result = contract_a.call(
        "read_global_box",
        member="global_counter",
        boxes=[(contract_a.app_id, "global_counter")],
    )
    print("Global box inremented to value: " + str(result.return_value))

    contract_a.call(
        "decrement_global_box",
        member="global_counter",
        suggested_params=sp,
        boxes=[(contract_a.app_id, "global_counter")]
    )

    result = contract_a.call(
        "read_global_box",
        member="global_counter",
        boxes=[(contract_a.app_id, "global_counter")],
    )
    print("Global box decremented to value: " + str(result.return_value))


    contract_a.call(
        "make_local_box",
        new_member=member_acct.address,
        value=1,
        suggested_params=sp,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))]
    )

    result = contract_a.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))],
    )
    print("Local box created with value: " + str(result.return_value))

    contract_a.call(
        "set_local_box",
        member=member_acct.address,
        value=4,
        suggested_params=sp,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))]
    )

    result = contract_a.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))],
    )
    print("Local box set to value: " + str(result.return_value))

    contract_a.call(
        "increment_local_box",
        member=member_acct.address,
        suggested_params=sp,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))]
    )

    result = contract_a.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))],
    )

    print("Local box incremeneted to value: " + str(result.return_value))

    contract_a.call(
        "decrement_local_box",
        member=member_acct.address,
        suggested_params=sp,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))]
    )

    result = contract_a.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(contract_a.app_id, decode_address(member_acct.address))],
    )

    print("Local box decremented to value: " + str(result.return_value))

if __name__ == "__main__":
    demo()