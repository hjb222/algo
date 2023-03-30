from algosdk.abi import ABIType
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.encoding import decode_address, encode_address
from algosdk.transaction import AssetOptInTxn, PaymentTxn
from beaker import *
from beaker import client, consts, sandbox
from application import (
     membership_club_app
)

def demo() -> None:
    accts = sandbox.get_accounts()
    acct = accts.pop()
    member_acct = accts.pop()

    app_client = client.ApplicationClient(
        sandbox.get_algod_client(), membership_club_app, signer=acct.signer
    )
    print("Creating app")
    app_client.create()

    sp = app_client.get_suggested_params()

     ##
    # Bootstrap Club app
    ##
    print("Bootstrapping app")
    sp = app_client.get_suggested_params()
    sp.flat_fee = True
    sp.fee = 2000
    ptxn = PaymentTxn(
        acct.address,
        sp,
        app_client.app_addr,
        99999999
    )
    app_client.call(
        "bootstrap",
        seed=TransactionWithSigner(ptxn, acct.signer),
        token_name="fight club",
        boxes=[(app_client.app_id, "affirmations")] * 8,
    )

    app_client.call(
        "make_global_box",
        new_member="global_counter",
        value=1,
        suggested_params=sp,
        boxes=[(app_client.app_id, "global_counter")]
    )


    result = app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(app_client.app_id, "global_counter")],
    )
    print("Global box created with value: " + str(result.return_value))

    app_client.call(
        "set_global_box",
        member="global_counter",
        value=8,
        suggested_params=sp,
        boxes=[(app_client.app_id, "global_counter")]
    )

    result = app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(app_client.app_id, "global_counter")],
    )
    print("Global box set to value: " + str(result.return_value))

    app_client.call(
        "increment_global_box",
        member="global_counter",
        suggested_params=sp,
        boxes=[(app_client.app_id, "global_counter")]
    )

    result = app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(app_client.app_id, "global_counter")],
    )
    print("Global box inremented to value: " + str(result.return_value))

    app_client.call(
        "decrement_global_box",
        member="global_counter",
        suggested_params=sp,
        boxes=[(app_client.app_id, "global_counter")]
    )

    result = app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(app_client.app_id, "global_counter")],
    )
    print("Global box decremented to value: " + str(result.return_value))


    app_client.call(
        "make_local_box",
        new_member=member_acct.address,
        value=1,
        suggested_params=sp,
        boxes=[(app_client.app_id, decode_address(member_acct.address))]
    )

    result = app_client.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(app_client.app_id, decode_address(member_acct.address))],
    )
    print("Local box created with value: " + str(result.return_value))

    app_client.call(
        "set_local_box",
        member=member_acct.address,
        value=4,
        suggested_params=sp,
        boxes=[(app_client.app_id, decode_address(member_acct.address))]
    )

    result = app_client.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(app_client.app_id, decode_address(member_acct.address))],
    )
    print("Local box set to value: " + str(result.return_value))

    app_client.call(
        "increment_local_box",
        member=member_acct.address,
        suggested_params=sp,
        boxes=[(app_client.app_id, decode_address(member_acct.address))]
    )

    result = app_client.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(app_client.app_id, decode_address(member_acct.address))],
    )

    print("Local box incremeneted to value: " + str(result.return_value))

    app_client.call(
        "decrement_local_box",
        member=member_acct.address,
        suggested_params=sp,
        boxes=[(app_client.app_id, decode_address(member_acct.address))]
    )

    result = app_client.call(
        "read_local_box",
        member=member_acct.address,
        boxes=[(app_client.app_id, decode_address(member_acct.address))],
    )

    print("Local box decremented to value: " + str(result.return_value))

if __name__ == "__main__":
    demo()