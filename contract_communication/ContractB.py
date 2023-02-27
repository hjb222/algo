from pyteal import *
from beaker import *
import os
import json
from typing import Final
 
APP_CREATOR = Seq(creator := AppParam.creator(Int(0)), creator.value())
 
class Demo(Application):
 
    @create
    def create(self):
        return self.initialize_application_state()

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