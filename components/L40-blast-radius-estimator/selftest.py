# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L40 selftest — 断言写在实现旁边，改坏了立刻红。"""
import impl


def main():
    impl.l40_selftest()
    print("PASS L40 blast-radius-estimator")


if __name__ == "__main__":
    main()
