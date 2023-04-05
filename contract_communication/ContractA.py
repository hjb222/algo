from pyteal import *
from beaker import *
import os
import json
from typing import Final
from beaker.consts import ASSET_MIN_BALANCE, BOX_BYTE_MIN_BALANCE, BOX_FLAT_MIN_BALANCE
from beaker.lib.storage import BoxMapping

global_counter = GlobalStateValue(
        TealType.uint64,
        default=Int(1),
        descr="An int as a global counter",
)

class ContractA:
    def __init__(self, *, max_members: int):

        # A Mapping will create a new box for every unique key,
        # taking a data type for key and value
        # Only static types can provide information about the max
        # size (and thus min balance required) - dynamic types will fail at abi.size_of
        self.local_boxes = BoxMapping(abi.Address, abi.Uint64)
        self.global_boxes = BoxMapping(abi.String, abi.Uint64)
        # Math for determining min balance based on expected size of boxes
        self.max_members = Int(max_members)


contract_a = Application(
    "ContractA",
    state=ContractA(max_members=1000),
)

@contract_a.external()
def make_global_box(new_member: abi.String, value: abi.Uint64):
    return contract_a.state.global_boxes[new_member.get()].set(value)

@contract_a.external()
def make_local_box(new_member: abi.Account, value: abi.Uint64):
    return contract_a.state.local_boxes[new_member.address()].set(value)

@contract_a.external()
def read_global_box(member: abi.String, *,output:abi.Uint64):
    return contract_b.state.global_boxes[member.get()].store_into(output)

def read_global_box(member: abi.String, *,output:abi.Uint64):
    return contract_a.state.global_boxes[member.get()].store_into(output)

@contract_a.external()
def read_local_box(member: abi.Address, *, output:abi.Uint64):
    return contract_a.state.global_boxes[member.get()].store_into(output)

@contract_a.external()
def set_global_box(member: abi.String, value: abi.Uint64):
    return contract_a.state.global_boxes[member.get()].set(value)

@contract_a.external()
def set_local_box(member: abi.Address, value: abi.Uint64):
    return contract_a.state.global_boxes[member.get()].set(value)

@contract_a.external()
def increment_global_box(member: abi.String,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_a.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            contract_a.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@contract_a.external()
def decrement_global_box(member: abi.String,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_a.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() - Int(1)),
            contract_a.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@contract_a.external()
def increment_local_box(member: abi.Address,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_a.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            contract_a.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@contract_a.external()
def decrement_local_box(member: abi.Address,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            contract_a.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() - Int(1)),
            contract_a.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )


@contract_a.external(authorize=Authorize.only(Global.creator_address()))
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
                TxnField.config_asset_total: contract_a.state.max_members,
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

def is_odd(val:abi.Uint64):
    return If(val%2 != 0, abi.Bool(False), abi.Bool(True))

# https://forum.algorand.org/t/calling-function-of-another-contract-in-current-contract/7571
@contract_a.external()
def add(num1: abi.Uint64, num2: abi.Uint64, app_id: abi.Uint64, *, output: abi.Uint64):
    return Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: app_id,
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.application_args: [Bytes("add"), num1, num2]
        }),
        InnerTxnBuilder.Submit()
    ) # in order to return value back to user, A has to look at logs from call to B to get return value, then use that as its own return value
    
@contract_a.external()
def sub(num1: abi.Uint64, num2: abi.Uint64, app_id: abi.Uint64, *, output: abi.Uint64):
    return Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.application_id: app_id,
            TxnField.on_completion: OnComplete.NoOp,
            TxnField.application_args: [Bytes("sub"), num1, num2]
        }),
        InnerTxnBuilder.Submit()
    )
