#!/usr/bin/env python3
"""实验protocol版本管理"""

# 实验protocol版本管理
import os
import json
from datetime import datetime

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


print("=" * 60)
print("  📖 实验Protocol版本管理器")
print("=" * 60)

protocol_dir = get_input("protocol目录路径", "protocols")
action = get_input("操作(list/create/update/diff)", "list")
output_file = get_input("版本报告路径", "protocol_versions.txt")

os.makedirs(protocol_dir, exist_ok=True)

version_file = os.path.join(protocol_dir, "version_log.json")

if os.path.exists(version_file):
    with open(version_file, "r", encoding="utf-8") as f:
        version_log = json.load(f)
else:
    version_log = {"protocols": {}, "history": []}

print("✅ Protocol目录: " + protocol_dir)

if action == "list":
    print("\n📋 Protocol列表:")
    for name, info in version_log["protocols"].items():
        print("  " + name + ": v" + info["version"] + " (" + info["last_updated"] + ")")

elif action == "create":
    name = get_input("Protocol名称", "new_protocol")
    description = get_input("Protocol描述", "")
    version = "1.0"
    
    version_log["protocols"][name] = {
        "version": version,
        "description": description,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "changes": ["Initial version"]
    }
    version_log["history"].append({
        "protocol": name, "action": "create",
        "version": version, "date": datetime.now().strftime("%Y-%m-%d")
    })
    
    proto_path = os.path.join(protocol_dir, name + "_v" + version + ".md")
    with open(proto_path, "w", encoding="utf-8") as f:
        f.write("# " + name + "\n\nVersion: " + version + "\n\n" + description + "\n\n## Steps\n\n1. [Step 1]\n")
    print("  ✅ 创建: " + name + " v" + version)

elif action == "update":
    name = get_input("Protocol名称(已有)", "existing_protocol")
    if name in version_log["protocols"]:
        changes = get_input("变更描述", "minor update")
        old_ver = version_log["protocols"][name]["version"]
        parts = old_ver.split(".")
        new_ver = parts[0] + "." + str(int(parts[1]) + 1)
        
        version_log["protocols"][name]["version"] = new_ver
        version_log["protocols"][name]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        version_log["protocols"][name]["changes"].append(changes)
        version_log["history"].append({
            "protocol": name, "action": "update",
            "version": new_ver, "date": datetime.now().strftime("%Y-%m-%d")
        })
        print("  ✅ 更新: " + name + " v" + old_ver + " -> v" + new_ver)

with open(version_file, "w", encoding="utf-8") as f:
    json.dump(version_log, f, indent=2, ensure_ascii=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("Protocol Version Report\n")
    f.write("Date: " + datetime.now().strftime("%Y-%m-%d") + "\n\n")
    for name, info in version_log["protocols"].items():
        f.write("  " + name + ": v" + info["version"] + "\n")
        for c in info["changes"]:
            f.write("    - " + c + "\n")

print("📄 版本报告: " + output_file)
