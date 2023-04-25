import C2CContract
import SecondaryContract
import beaker
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.transaction import PaymentTxn


def demo() -> None:
    algod_client = beaker.sandbox.get_algod_client()
    account = beaker.sandbox.get_accounts().pop()

    # create a couple of clients for the same underlying application
    # definition
    first_app_client = beaker.client.ApplicationClient(
        algod_client,
        C2CContract.app,
        signer=account.signer,
    )

    second_app_client = beaker.client.ApplicationClient(
        algod_client,
        SecondaryContract.app,
        signer=account.signer,
    )

    # Deploy the apps on-chain
    first_app_client.create()
    second_app_client.create()

    # fund the first app client

    print("Bootstrapping app")
    sp = first_app_client.get_suggested_params()
    sp.flat_fee = True
    sp.fee = 2000
    ptxn = PaymentTxn(
        account.address,
        sp,
        first_app_client.app_addr,
        99999999
    )
    first_app_client.call(
        "bootstrap",
        seed=TransactionWithSigner(ptxn, account.signer),
        token_name="fight club",
        boxes=[(first_app_client.app_id, "affirmations")] * 8,
    )
    first_app_client.call(
        "make_global_box",
        new_member="global_counter",
        value=1,
        suggested_params=sp,
        boxes=[(first_app_client.app_id, "global_counter")]
    )


    result = first_app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(first_app_client.app_id, "global_counter")],
    )
    print("Global box created with value: " + str(result.return_value))

    first_app_client.call(
        "set_global_box",
        member="global_counter",
        value=8,
        suggested_params=sp,
        boxes=[(first_app_client.app_id, "global_counter")]
    )

    result = first_app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(first_app_client.app_id, "global_counter")],
    )
    print("Global box set to value: " + str(result.return_value))

    first_app_client.call(
        "increment_global_box",
        member="global_counter",
        suggested_params=sp,
        boxes=[(first_app_client.app_id, "global_counter")]
    )

    result = first_app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(first_app_client.app_id, "global_counter")],
    )
    print("Global box inremented to value: " + str(result.return_value))

    first_app_client.call(
        "decrement_global_box",
        member="global_counter",
        suggested_params=sp,
        boxes=[(first_app_client.app_id, "global_counter")]
    )

    result = first_app_client.call(
        "read_global_box",
        member="global_counter",
        boxes=[(first_app_client.app_id, "global_counter")],
    )
    print("Global box decremented to value: " + str(result.return_value))

    result = first_app_client.call(
        C2CContract.call_calc_method,
        fn_selector=SecondaryContract.perform_add.method_spec().get_selector(),
        num1=3,
        num2=2,
        other_app=second_app_client.app_id, 
        suggested_params=sp,
    )
    print(result.return_value)

    result = first_app_client.call(
        C2CContract.call_calc_method,
        fn_selector=SecondaryContract.perform_sub.method_spec().get_selector(),
        num1=5,
        num2=2,
        other_app=second_app_client.app_id, 
        suggested_params=sp,
    )
    print(result.return_value)

    result = first_app_client.call(
        C2CContract.call_calc_method,
        fn_selector=SecondaryContract.perform_mul.method_spec().get_selector(),
        num1=2,
        num2=3,
        other_app=second_app_client.app_id, 
        suggested_params=sp,
    )
    print(result.return_value)

    result = first_app_client.call(
        C2CContract.call_calc_method,
        fn_selector=SecondaryContract.perform_div.method_spec().get_selector(),
        num1=4,
        num2=2,
        other_app=second_app_client.app_id, 
        suggested_params=sp,
    )
    print(result.return_value)

if __name__ == "__main__":
    demo()
