# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L37 — 自改绊线（迭代安全）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


_RED = {
    "记忆层": ["MEMORY.md", "memory/", "notes/", "wiki/"],
    "发布门": ["license_gate", "release_gate", "gate_depth", "INDEX.md"],
    "规则": ["rules/", "规定-", "约定-"],
    "凭据": [".env", "token", "secret", "keyfile"],
}


def l37_check(paths):
    """迭代若触及红区，必须停下来要授权——即使改的是「优化」。"""
    hits = []
    for p in paths:
        low = p.lower()
        for zone, keys in _RED.items():
            if any(k.lower() in low for k in keys):
                hits.append({"path": p, "zone": zone})
                break
    return {
        "touched_red": bool(hits),
        "hits": hits,
        "verdict": "STOP-need-authorization" if hits else "clear",
        "why": "触及红区：这类改动即使看起来是优化，也必须先要一句明确授权" if hits else "未触红区",
    }


def l37_demo():
    safe = ["src/policy.py", "cards/policy.json"]
    risky = ["docs/style-guide.md", "config/credentials.json"]
    print("  普通改动 ->", l37_check(safe)["verdict"])
    r = l37_check(risky)
    print("  危险改动 ->", r["verdict"], [h["zone"] for h in r["hits"]])


def l37_selftest():
    assert l37_check(["a/b.py"])["verdict"] == "clear"
    r = l37_check(["docs/MEMORY.md"])
    assert r["verdict"].startswith("STOP") and r["hits"][0]["zone"] == "记忆层"
    assert l37_check(["x/.env"])["hits"][0]["zone"] == "凭据"
    return True


if __name__ == "__main__":
    l37_demo()
