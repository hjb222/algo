from pyteal import *
from beaker import *
import os
import json
from typing import Final
from beaker.consts import ASSET_MIN_BALANCE, BOX_BYTE_MIN_BALANCE, BOX_FLAT_MIN_BALANCE
from beaker.lib.storage import BoxMapping

class ContractB:
    def __init__(self, *, max_members: int):

        # A Mapping will create a new box for every unique key,
        # taking a data type for key and value
        # Only static types can provide information about the max
        # size (and thus min balance required) - dynamic types will fail at abi.size_of
        self.local_boxes = BoxMapping(abi.Address, abi.Uint64)
        self.global_boxes = BoxMapping(abi.String, abi.Uint64)
        # Math for determining min balance based on expected size of boxes
        self.max_members = Int(max_members)


contract_b = Application(
    "ContractB",
    state=ContractB(max_members=1000),
)

@contract_b.external()
def make_global_box(new_member: abi.String, value: abi.Uint64):
    return contract_b.state.global_boxes[new_member.get()].set(value)

@contract_b.external()
def make_local_box(new_member: abi.Account, value: abi.Uint64):
    return contract_b.state.local_boxes[new_member.address()].set(value)

@contract_b.external()
def read_global_box(member: abi.String, *,output:abi.Uint64):
    return contract_b.state.global_boxes[member.get()].store_into(output)

def read_global_box(member: abi.String, *,output:abi.Uint64):
    return contract_b.state.global_boxes[member.get()].store_into(output)

@contract_b.external()
def read_local_box(member: abi.Address, *, output:abi.Uint64):
    return contract_b.state.global_boxes[member.get()].store_into(output)

@contract_b.external()
def set_global_box(member: abi.String, value: abi.Uint64):
    return contract_b.state.global_boxes[member.get()].set(value)

@contract_b.external()
def set_local_box(member: abi.Address, value: abi.Uint64):
    return contract_b.state.global_boxes[member.get()].set(value)

@contract_b.external()
def increment_global_box(member: abi.String,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_b.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            contract_b.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@contract_b.external()
def decrement_global_box(member: abi.String,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_b.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() - Int(1)),
            contract_b.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@contract_b.external()
def increment_local_box(member: abi.Address,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_b.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            contract_b.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@contract_b.external()
def decrement_local_box(member: abi.Address,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_b.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() - Int(1)),
            contract_b.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )


@contract_b.external(authorize=Authorize.only(Global.creator_address()))
def bootstrap(
    seed: abi.PaymentTransaction,
    token_name: abi.String,
) -> Expr:
    """create membership token and receive initial seed payment"""
    return Seq(
        Assert(
            seed.get().receiver() == Global.current_application_address(),
            comment="payment must be to app address",
        ),
        #Pop(membership_club_app.state.affirmations.create()),
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: token_name.get(),
                TxnField.config_asset_total: contract_b.state.max_members,
                TxnField.config_asset_default_frozen: Int(1),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.fee: Int(0),
            }
        ),
        # membership_club_app.state.membership_token.set(InnerTxn.created_asset_id()),
        # output.set(membership_club_app.state.membership_token),
    )
    
@contract_b.external()
def add(num1: abi.Uint64, num2: abi.Uint64):
    return Seq(num1 + num2)


@contract_b.external
def sub(num1: abi.Uint64, num2: abi.Uint64):
    return Seq(num1 - num2)

# @external
# def pay(self, acct:abi.Uint64):

if __name__ == "__main__":
    app = ContractB(max_members=100)

    if os.path.exists("approval.teal"):
        os.remove("approval.teal")

    if os.path.exists("approval.teal"):
        os.remove("clear.teal")

    if os.path.exists("abi.json"):
        os.remove("abi.json")

    if os.path.exists("app_spec.json"):
        os.remove("app_spec.json")

    with open("approval.teal", "w") as f:
        f.write(app.approval_program)

    with open("clear.teal", "w") as f:
        f.write(app.clear_program)

    with open("abi.json", "w") as f:
        f.write(json.dumps(app.contract.dictify(), indent=4))

    with open("app_spec.json", "w") as f:
        f.write(json.dumps(app.application_spec(), indent=4))
        