from pyteal import *
from beaker import *
import os
import json
from typing import Final
 
APP_CREATOR = Seq(creator := AppParam.creator(Int(0)), creator.value())
 
class DemoB(Application):
 
    @create
    def create(self):
        return self.initialize_application_state()
    
    # @external
    # def add(self, num1: abi.Uint64, num2: abi.Uint64):
    

    # @external
    # def sub(self, num1: abi.Uint64, num2: abi.Uint64):

    # @external
    # def pay(self, acct:abi.Uint64):
        

if __name__ == "__main__":
    app = DemoB(version=8)
    artifactPath = "artifactsB/"
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