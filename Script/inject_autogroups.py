#!/usr/bin/env python3
"""
每当 Surge 从订阅链接更新 WestData.conf 后，
自动往 [Proxy Group] 里补回各地区的 url-test 自动延迟组。
"""

import re
import time

CONFIG_FILE = "/Users/weko/Library/Mobile Documents/com~apple~CloudDocs/surge/WestData.conf"

# 等待 Surge 完成文件写入
time.sleep(2)

def inject_auto_groups(text):
    if "HK-Auto" in text:
        print("Auto groups already present, skipping.")
        return text

    lines = text.split("\n")
    result = []

    for line in lines:
        injected = False
        for region in ["HK", "JP", "SG", "TW", "US"]:
            # 匹配形如 "HK = select,🇭🇰 Hong Kong | 01,..." 的行
            m = re.match(rf"^{region} = select,(.+)$", line)
            if m:
                nodes_str = m.group(1)
                nodes = [n.strip() for n in nodes_str.split(",")]
                nodes_csv = ",".join(nodes)
                result.append(f"{region} = select,{region}-Auto,{nodes_csv}")
                result.append(
                    f"{region}-Auto = url-test,{nodes_csv},"
                    f"url=http://www.gstatic.com/generate_204,interval=600,tolerance=100"
                )
                injected = True
                break
        if not injected:
            result.append(line)

    return "\n".join(result)


with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    content = f.read()

new_content = inject_auto_groups(content)

if new_content != content:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Auto groups injected successfully.")
