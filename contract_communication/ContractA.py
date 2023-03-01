from pyteal import *
from beaker import *
import os
import json
from typing import Final
 
APP_CREATOR = Seq(creator := AppParam.creator(Int(0)), creator.value())
 
class DemoA(Application):
 
    global_counter: Final[ApplicationStateValue] = ApplicationStateValue(stack_type=TealType.uint64, default=Int(0))
    winning_call_number: Final[ApplicationStateValue] = ApplicationStateValue(stack_type=TealType.uint64, default=Int(5))

    @create
    def create(self):
        return self.initialize_application_state()
    
    # @internal
    # def is_odd(self,val:abi.Uint64):
    
    @internal 
    def winner(self, acct: abi.Address):
        return self.global_counter.set(self.global_counter.get()+Int(5))
    
    @internal
    def increaseCounter(self, acct: abi.Address):
        return If(self.global_counter.get()==self.winning_call_number.get(),
                  self.winner(acct),
                  self.global_counter.set(self.global_counter.get()+Int(1)))
    
    @external
    def getGlobalCounter(self,*,output:abi.Uint64):
        return output.set(self.global_counter.get())
    
    # https://forum.algorand.org/t/calling-function-of-another-contract-in-current-contract/7571
    @external
    def add(self, num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.application_id: Int(3),
                TxnField.on_completion: OnComplete.NoOp,
                TxnField.application_args: [Bytes("add"), Int(num1.get()), Int(num2.get())]
            }),
            InnerTxnBuilder.Submit()
        )

    @external
    def sub(self, num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.application_id: Int(3),
                TxnField.on_completion: OnComplete.NoOp,
                TxnField.application_args: [Bytes("sub"), Int(num1.get()), Int(num2.get())]
            }),
            InnerTxnBuilder.Submit()
        )

    
            

if __name__ == "__main__":
    app = DemoA(version=8)
    artifactPath = "artifactsA/"
    if os.path.exists("./"+artifactPath+"approval.teal"):
        os.remove("./"+artifactPath+"approval.teal")
 
    if os.path.exists("./"+artifactPath+"approval.teal"):
        os.remove("./"+artifactPath+"clear.teal")
 
    if os.path.exists("./"+artifactPath+"abi.json"):
        os.remove("./"+artifactPath+"abi.json")
 
    if os.path.exists("./"+artifactPath+"app_spec.json"):
        os.remove("./"+artifactPath+"app_spec.json")
 
    with open("./"+artifactPath+"approval.teal", "w") as f:
        f.write(app.approval_program)
 
    with open("./"+artifactPath+"clear.teal", "w") as f:
        f.write(app.clear_program)
 
    with open("./"+artifactPath+"abi.json", "w") as f:
        f.write(json.dumps(app.contract.dictify(), indent=4))
 
    with open("./"+artifactPath+"app_spec.json", "w") as f:
        f.write(json.dumps(app.application_spec(), indent=4))