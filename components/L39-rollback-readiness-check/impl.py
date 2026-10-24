# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L39 — 回滚就绪检查（迭代安全）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l39_check(backup_exists, backup_verified, steps_documented, owner_known):
    """四级就绪：缺任何一项都不是「可回滚」，只是「以为可回滚」。"""
    items = {
        "backup_exists": bool(backup_exists),
        "backup_verified": bool(backup_verified),
        "steps_documented": bool(steps_documented),
        "owner_known": bool(owner_known),
    }
    score = sum(items.values()) / len(items)
    if score == 1.0:
        lvl, verdict = "R3-ready", "可回滚（已演练）"
    elif items["backup_exists"]:
        lvl, verdict = "R1-unverified", "有备份但未验证：回滚时才知道坏没坏"
    else:
        lvl, verdict = "R0-blind", "无备份：任何改动都是单向门"
    return {"score": round(score, 3), "level": lvl, "verdict": verdict,
            "missing": [k for k, v in items.items() if not v]}


def l39_demo():
    cases = [
        (True, True, True, True),
        (True, False, True, True),
        (False, False, False, False),
    ]
    for c in cases:
        r = l39_check(*c)
        print("  %s -> %-12s %s 缺%s" % (c, r["level"], r["verdict"], r["missing"]))


def l39_selftest():
    assert l39_check(True, True, True, True)["level"] == "R3-ready"
    assert l39_check(True, False, True, True)["level"] == "R1-unverified"
    assert l39_check(False, False, False, False)["level"] == "R0-blind"
    assert l39_check(True, True, True, True)["missing"] == []
    return True


if __name__ == "__main__":
    l39_demo()
