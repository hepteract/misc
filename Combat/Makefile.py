import json
import sys
import os

def generate_attack():
    code = ""
    with open("modules.conf") as conf:
        modules = conf.read().split("\n")
        try:
            modules.remove("")
        except:
            pass

    modules.insert(0, "include")
    
    for module in modules:
        code += "\n"
        with open(module + ".py") as f:
            code += f.read()
    return code

def make():
    if len(sys.argv) >= 2:
        cmd = " ".join(["./make"] + sys.argv[1:])
        os.system(cmd)
    else:
        with open("attack.py", "w") as f:
            f.write( generate_attack() )
            
        data = {}
        with open("material.json") as f:
            data["material"] = json.load(f)
        with open("character.json") as f:
            data["character"] = json.load(f)
        with open("weapon.json") as f:
            data["weapon"] = json.load(f)
        with open("magic.json") as f:
            data["magic"] = json.load(f)
            
        link(["basic_combat.py", "attack.py"], data, "combat")
        os.remove("attack.py")
