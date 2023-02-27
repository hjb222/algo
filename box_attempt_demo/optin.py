from beaker.client import ApplicationClient
from demo import Demo
from beaker import sandbox
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk import transaction
from beaker import consts


# Get sandbox `algod` client
sandbox_client = sandbox.get_algod_client()

# Retrieve sandbox accounts
wallet_name = "unencrypted-default-wallet"  # <-- put wallet's name here
wallet_password = ""  # <-- put wallet's password here
sandbox_accounts = sandbox.get_accounts(
    wallet_name=wallet_name,
    wallet_password=wallet_password,
)
print(f"Found {len(sandbox_accounts)} accounts into the wallet")

# Pop accounts from sandbox
manager_acct = sandbox_accounts.pop()
print(f"Manager account: {manager_acct.address}")

oracle_acct = sandbox_accounts.pop()
print(f"Oracle account: {oracle_acct.address}")

participant_1_acct = sandbox_accounts.pop()
print(f"Participant 1 account: {participant_1_acct.address}")

# participant_2_acct = sandbox_accounts.pop()
# print(f"Participant 2 account: {participant_2_acct.address}")

# Create an Application client signed by Participant 1
app_client_participant_1 = ApplicationClient(
    # Use the `algod` client connected to sandbox
    client=sandbox_client,
    # Provide an AlgoBet instance to the client
    app=Demo(),
    # Provide a deployed AlgoBet dApp ID
    app_id=9,
    # Select the Participant 1 account as transaction signer
    signer=participant_1_acct.signer
)

# Opt-in into the dApp
app_client_participant_1.opt_in()

# APP_ADDR = "BAXQDLV55Y24TA35PSFOOQU6KCZT7AP3SMKW54GTDSN3DUQAFW7BYKKVRQ"
# # Place a bet as Participant 1 forecasting a home team win
# result = app_client_participant_1.call(
#     # Transaction to be requested
#     Demo.opt_in,
#     # Bet deposit transaction
#     bet_deposit_tx=TransactionWithSigner(
#         # Transaction of type PaymentTxn
#         txn=transaction.PaymentTxn(
#             # Address of the account requesting the transfer
#             participant_1_acct.address,
#             # Transaction parameters (use suggested)
#             app_client_participant_1.client.suggested_params(),
#             # Receiver account address
#             APP_ADDR,
#             # Transfer amount
#             140 * consts.milli_algo),
#         # Payment transaction signer
#         signer=participant_1_acct.signer
#     ),
#     # Option to bet on: home team win
#     opt=0
# )