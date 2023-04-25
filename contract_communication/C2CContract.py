from pyteal import *
import pyteal as pt
from beaker import *
from typing import Literal
from typing import Final
from beaker.consts import ASSET_MIN_BALANCE, BOX_BYTE_MIN_BALANCE, BOX_FLAT_MIN_BALANCE
from beaker.lib.storage import BoxMapping

class C2CContract:
    def __init__(self, *, max_members: int):

        # A Mapping will create a new box for every unique key,
        # taking a data type for key and value
        # Only static types can provide information about the max
        # size (and thus min balance required) - dynamic types will fail at abi.size_of
        self.local_boxes = BoxMapping(abi.Address, abi.Uint64)
        self.global_boxes = BoxMapping(abi.String, abi.Uint64)
        # Math for determining min balance based on expected size of boxes
        self.max_members = Int(max_members)


app = Application(
    "C2CContract",
    state=C2CContract(max_members=1000),
)

@app.opt_in()
def opt_in():
    return app.initialize_global_state()


@app.external()
def make_global_box(new_member: abi.String, value: abi.Uint64):
    return app.state.global_boxes[new_member.get()].set(value)

@app.external()
def make_local_box(new_member: abi.Account, value: abi.Uint64):
    return app.state.local_boxes[new_member.address()].set(value)

@app.external()
def read_global_box(member: abi.String, *,output:abi.Uint64):
    return app.state.global_boxes[member.get()].store_into(output)

def read_global_box(member: abi.String, *,output:abi.Uint64):
    return app.state.global_boxes[member.get()].store_into(output)

@app.external()
def read_local_box(member: abi.Address, *, output:abi.Uint64):
    return app.state.global_boxes[member.get()].store_into(output)

@app.external()
def set_global_box(member: abi.String, value: abi.Uint64):
    return app.state.global_boxes[member.get()].set(value)

@app.external()
def set_local_box(member: abi.Address, value: abi.Uint64):
    return app.state.global_boxes[member.get()].set(value)

@app.external()
def increment_global_box(member: abi.String,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            app.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            app.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@app.external()
def decrement_global_box(member: abi.String,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            app.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() - Int(1)),
            app.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@app.external()
def increment_local_box(member: abi.Address,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            app.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            app.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )

@app.external()
def decrement_local_box(member: abi.Address,*,output:abi.Uint64):
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            app.state.global_boxes[member.get()].store_into(old_counter),
            new_counter.set(old_counter.get() - Int(1)),
            app.state.global_boxes[member.get()].set(new_counter),
            output.set(new_counter),
    )


@app.external(authorize=Authorize.only(Global.creator_address()))
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
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: token_name.get(),
                TxnField.config_asset_total: app.state.max_members,
                TxnField.config_asset_default_frozen: Int(1),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.fee: Int(0),
            }
        ),
    )


# https://forum.algorand.org/t/calling-function-of-another-contract-in-current-contract/7571

def increment_global():
    old_counter = abi.Uint64()
    new_counter = abi.Uint64()
    return Seq(
            app.state.global_boxes[Bytes("global_counter")].store_into(old_counter),
            new_counter.set(old_counter.get() + Int(1)),
            app.state.global_boxes[Bytes("global_counter")].set(new_counter),
    )

@app.external
def call_calc_method(
    fn_selector: pt.abi.StaticBytes[Literal[4]], # method selector 
    num1: pt.abi.Uint64,
    num2: pt.abi.Uint64,
    other_app: pt.abi.Application,
    *,
    output: pt.abi.Uint64,
) -> pt.Expr:
    return pt.Seq(
        # call other app method, specified by fn
        # pass args a and b

        pt.InnerTxnBuilder.Begin(),
        pt.InnerTxnBuilder.SetFields({
            pt.TxnField.type_enum: pt.TxnType.ApplicationCall,
            pt.TxnField.application_id: other_app.application_id(),
            pt.TxnField.application_args: [
                fn_selector.encode(),
                num1.encode(),
                num2.encode(),
            ],
            pt.TxnField.fee: pt.Int(0),
        }),
        pt.InnerTxnBuilder.Submit(),
        output.decode(pt.Suffix(pt.InnerTxn.last_log(), pt.Int(4))),
        increment_global()
    )
