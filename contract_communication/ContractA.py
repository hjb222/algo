from pyteal import *
from beaker import *
import os
import json
from typing import Final
 
APP_CREATOR = Seq(creator := AppParam.creator(Int(0)), creator.value())
 
class Demo(Application):
 
    global_counter: Final[ApplicationStateValue] = ApplicationStateValue(stack_type=TealType.uint64, default=Int(0))
    winning_call_number: Final[ApplicationStateValue] = ApplicationStateValue(stack_type=TealType.uint64, default=Int(5))

    @create
    def create(self):
        return self.initialize_application_state()
    
    @external
    def getGlobalCounter(self,*,output:abi.Uint64):
        return output.set(self.global_counter.get())
    
    @internal 
    def winner(self, acct: abi.Address):
            return self.global_counter.set(self.global_counter.get()+Int(5))
    
    @internal
    def increaseCounter(self, acct: abi.Address):
        return If(self.global_counter.get()==self.winning_call_number.get(),
                  self.winner(acct),
                  self.global_counter.set(self.global_counter.get()+Int(1)))
    
    @external
    def add(self, num1: abi.Uint64, num2: abi.Uint64, *, output: abi.Uint64):
        return Seq(
             self.increaseCounter(Txn.sender()),
             output.set(num1.get()+num2.get())
        )
            

if __name__ == "__main__":
    app = Demo(version=8)
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