import typing
from typing import Final
from pyteal import *
from beaker import *
from beaker.consts import ASSET_MIN_BALANCE, BOX_BYTE_MIN_BALANCE, BOX_FLAT_MIN_BALANCE
from beaker.lib.storage import BoxMapping


class SecondaryContract:
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
    "SecondaryContract",
    state=SecondaryContract(max_members=1000),
)

@app.external()
def perform_add(num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
    return output.set(num1.get() + num2.get())

@app.external()
def perform_sub(num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
    return output.set(num1.get() - num2.get())

@app.external()
def perform_mul(num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
    return output.set(num1.get() * num2.get())

@app.external()
def perform_div(num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
    return output.set(num1.get() / num2.get())