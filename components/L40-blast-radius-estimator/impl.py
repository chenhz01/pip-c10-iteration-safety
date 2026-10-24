# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L40 — 爆炸半径估算（迭代安全）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l40_radius(files_changed, callers, user_facing, rollback_ready=True):
    """半径 = 改动面 × 调用方 × 用户可见；回滚不就绪直接乘 2。"""
    base = files_changed * 1.0 + callers * 2.0 + (user_facing * 10.0)
    if not rollback_ready:
        base *= 2
    if base >= 60:
        lvl, advice = "R3-wide", "必须分批发布 + 灰度 + 事前演练回滚"
    elif base >= 25:
        lvl, advice = "R2-medium", "分批发布，先内部验证再对外"
    elif base >= 8:
        lvl, advice = "R1-small", "单批可发，保留回滚点"
    else:
        lvl, advice = "R0-tiny", "直接做"
    return {"score": round(base, 2), "level": lvl, "advice": advice,
            "note": "回滚不就绪会直接让半径翻倍——这不是保守，是乘法的结果"}


def l40_demo():
    cases = [
        (1, 0, False, True),
        (3, 2, False, True),
        (5, 6, True, True),
        (5, 6, True, False),
    ]
    for c in cases:
        r = l40_radius(*c)
        print("  %-24s -> %-10s 分%.1f | %s" % (c, r["level"], r["score"], r["advice"]))


def l40_selftest():
    assert l40_radius(1, 0, False, True)["level"] == "R0-tiny"
    # 3 文件 + 2 调用方 = 7 分，仍在 R0；再加一个文件才进 R1（门槛 8）
    assert l40_radius(3, 2, False, True)["level"] == "R0-tiny"
    assert l40_radius(4, 2, False, True)["level"] == "R1-small"
    # 5 文件 + 6 调用方 + 对用户可见 = 27 分 → R2；要到 R3（60 分）得是真正的大改
    assert l40_radius(5, 6, True, True)["level"] == "R2-medium"
    assert l40_radius(20, 20, True, True)["level"] == "R3-wide"
    a = l40_radius(3, 2, False, True)["score"]
    b = l40_radius(3, 2, False, False)["score"]
    assert b == a * 2
    return True


if __name__ == "__main__":
    l40_demo()
