from pyteal import *
from beaker import *
import os
import json
from typing import Final

APP_CREATOR = Seq(creator := AppParam.creator(Int(0)), creator.value())

class Demo(Application):
    global_increment: Final[ApplicationStateValue] = ApplicationStateValue(stack_type=TealType.uint64, default=Int(0))
    

    @create
    def create(self):
        return self.initialize_application_state()
    
    @external(read_only=True)
    def getGlobalInc(self, *, output: abi.Uint64):
        return output.set(self.global_increment.get())

    @external
    def setGlobalInc(self, val: abi.Uint64):
        return self.global_increment.set(val.get())

    @external
    def incrementGlobal(self):
        return self.global_increment.set(self.global_increment.get()+Int(1))

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def is_opted_in(self, *, output: abi.Uint64):
        return output.set(App.optedIn(Txn.sender(), Txn.application_id()))

    @external
    def local_init(self, *, output: abi.Uint64):
        scratchCount = ScratchVar(TealType.uint64)
        return Seq(
            App.localPut(Txn.sender(), Bytes("local_counter"), Int(1)),
            output.set(App.localGet(Txn.sender(), Bytes("local_counter")))
        )
    
if __name__ == "__main__":
    app = Demo(version=8)

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