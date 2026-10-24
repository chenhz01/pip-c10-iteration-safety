# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L38 — 不变量快照（迭代安全）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l38_snapshot(pairs):
    """pairs: [(不变量名, 当前值)]。返回快照（可存 JSON）。"""
    return dict(pairs)


def l38_compare(before, after):
    broken, changed, same = [], [], []
    for k, v in before.items():
        if k not in after:
            broken.append({"name": k, "why": "迭代后该不变量消失了"})
        elif after[k] == v:
            same.append(k)
        else:
            changed.append({"name": k, "before": v, "after": after[k]})
    added = [k for k in after if k not in before]
    return {
        "broken": broken,
        "changed": changed,
        "same": same,
        "added": added,
        "verdict": "violation" if broken else ("changed" if changed else "stable"),
        "advice": "先解释 broken，再解释 changed：消失比变形更严重" if broken else "无破坏性变化",
    }


def l38_demo():
    b = l38_snapshot([("组件数", 55), ("自检通过率", "8/8"), ("零依赖", True)])
    a = l38_snapshot([("组件数", 55), ("自检通过率", "8/8"), ("零依赖", False)])
    r = l38_compare(b, a)
    print("  结果:", r["verdict"], "| 变化:", r["changed"], "|", r["advice"])
    r2 = l38_compare(b, l38_snapshot([("组件数", 55)]))
    print("  丢项:", r2["broken"], "->", r2["verdict"])


def l38_selftest():
    b = {"a": 1, "b": 2}
    assert l38_compare(b, {"a": 1, "b": 2})["verdict"] == "stable"
    assert l38_compare(b, {"a": 1, "b": 3})["verdict"] == "changed"
    r = l38_compare(b, {"a": 1})
    assert r["verdict"] == "violation" and r["broken"][0]["name"] == "b"
    return True


if __name__ == "__main__":
    l38_demo()
