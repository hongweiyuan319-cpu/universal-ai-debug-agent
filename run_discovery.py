#!/usr/bin/env python3
"""Universal AI Debug Agent · 命令行入口（T007）。

本脚本只做一件事：**为一次发现任务创建独立的产物目录**。

它现在会做
----------
1. 校验 ``--task-id``：只允许字母、数字、短横线、下划线，且必须以字母或数字开头，
   防止任务 ID 被用来把文件写到 ``artifacts/`` 之外；
2. 校验 ``--profile``：确认指定路径**存在且是普通文件**；
3. 创建 ``artifacts/task_<task-id>/``；目录已存在时直接报错，绝不覆盖；
4. 用退出码表示成功或失败（成功 ``0``，失败非 ``0``）。

它现在不会做（这是本轮的刻意边界）
--------------------------------
- **不读取** ``project-profile.yaml`` 的内容，**不 import yaml**：YAML 解析属于 T012；
- **不扫描**任何仓库、不识别语言 / 框架 / 依赖：属于 T008；
- 不分析 Flask / React 代码：属于 T009 / T010；
- 不构建调用链：属于 T011；
- **不执行** profile 里的 ``startup`` 命令（见决定 D004）；
- 不生成 ``repository_summary.json`` / ``system_map.json``，也不写任何“占位版”假结果。

换句话说：**有命令行入口，不等于已经实现仓库扫描。**

退出码
------
====  ===========================================
0     成功：任务目录已创建
2     argparse 用法错误（缺少参数、未知参数等）
3     ``--profile`` 指定的文件不存在，或指向的不是普通文件
4     ``--task-id`` 不符合命名规则
5     ``artifacts/task_<task-id>/`` 已存在（不覆盖）
6     artifacts 路径异常或目录创建失败
====  ===========================================

用法示例
--------
.. code-block:: console

    .venv/bin/python run_discovery.py \
        --task-id demo001 \
        --profile templates/project-profile.yaml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

__all__ = ["main"]

EXIT_OK = 0
EXIT_PROFILE_ERROR = 3
EXIT_TASK_ID_ERROR = 4
EXIT_TASK_DIR_EXISTS = 5
EXIT_ARTIFACTS_ERROR = 6

# 项目根目录：以本文件所在位置为准，这样无论从哪个工作目录运行，
# artifacts/ 都稳定地落在项目根目录下。
PROJECT_ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。

    ``--help`` 由 argparse 自动生成。两个参数都是必填：
    没有任务 ID 不知道产物写到哪，没有档案文件则连“为哪个项目跑”都不确定。
    """
    parser = argparse.ArgumentParser(
        prog="run_discovery.py",
        description=(
            "为一次发现任务创建 artifacts/task_<task-id>/ 目录。"
            "当前版本只初始化任务目录，尚不扫描仓库。"
        ),
        epilog=(
            "示例：.venv/bin/python run_discovery.py "
            "--task-id demo001 --profile templates/project-profile.yaml"
        ),
    )
    parser.add_argument(
        "--task-id",
        required=True,
        metavar="ID",
        help=(
            "任务 ID，例如 demo001、login-test、register_flow。"
            "只能包含字母、数字、短横线和下划线，且以字母或数字开头，最长 64 个字符。"
            "产物目录名为 task_<ID>，位于项目根目录的 artifacts/ 下。"
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        metavar="PATH",
        help=(
            "project-profile.yaml 的路径。本轮只校验它存在且是普通文件，"
            "不读取内容、不解析 YAML（解析将在 T012 实现）。"
        ),
    )
    return parser.parse_args(argv)


def validate_task_id(task_id: str) -> str:
    """校验任务 ID 是否可以安全地当目录名使用。

    为什么必须限制字符：任务 ID 会被拼进目录名，
    一旦允许 ``/``、``\\`` 或 ``..``，就可能被用来写到 ``artifacts/`` 之外，
    甚至覆盖项目里的其他文件。这里采用“白名单”而不是“过滤危险字符”，
    因为过滤很容易漏，而白名单漏不掉。
    """
    if not TASK_ID_PATTERN.fullmatch(task_id):
        raise ValueError(
            f"--task-id 不合法：{task_id!r}\n"
            "  要求：只能包含英文字母、数字、短横线（-）和下划线（_），"
            "必须以字母或数字开头，长度 1～64。\n"
            "  不能包含空格、斜杠（/）、反斜杠（\\）、点（.）或其他符号。\n"
            "  合法示例：demo001、login-test、register_flow"
        )
    return task_id


def resolve_profile_path(raw_path: str) -> Path:
    """确认档案文件存在，并返回它的绝对路径。

    注意：这里**只看路径**，不打开、不读取、不解析文件内容。
    """
    path = Path(raw_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"--profile 指向的文件不存在：{raw_path}")
    if not path.is_file():
        raise IsADirectoryError(
            f"--profile 指向的不是普通文件（可能是目录或其他类型）：{raw_path}"
        )
    return path.resolve()


def create_task_directory(task_id: str) -> Path:
    """创建 ``artifacts/task_<task_id>/`` 并返回该目录。

    已存在时抛 ``FileExistsError``：**不删除、不清空、不覆盖**。
    """
    if ARTIFACTS_DIR.exists() and not ARTIFACTS_DIR.is_dir():
        raise NotADirectoryError(f"artifacts 已存在但不是目录：{ARTIFACTS_DIR}")

    task_dir = ARTIFACTS_DIR / f"task_{task_id}"

    # 双保险：即便上游校验被绕过，也不允许目录落到 artifacts/ 之外。
    if task_dir.parent.resolve() != ARTIFACTS_DIR.resolve():
        raise ValueError(f"任务目录不在 artifacts/ 之下，已拒绝创建：{task_dir}")

    if task_dir.exists():
        raise FileExistsError(str(task_dir))

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    task_dir.mkdir()
    return task_dir


def _print_error(message: str) -> None:
    """错误信息统一写到 stderr，方便调用方把正常输出和错误分开处理。"""
    print(f"错误：{message}", file=sys.stderr)


def _print_success(task_id: str, task_dir: Path, profile_path: Path) -> None:
    """成功信息统一写到 stdout，并如实说明“尚未扫描”。"""
    print("任务目录初始化成功。")
    print()
    print(f"  任务 ID   : {task_id}")
    print(f"  任务目录  : {task_dir}")
    print(f"  项目档案  : {profile_path}")
    print("              （仅确认文件存在，未读取内容、未解析 YAML）")
    print()
    print("说明：本次只创建了任务目录，尚未扫描任何代码，也未生成任何扫描结果。")
    print("      仓库扫描与技术栈识别将在 T008 实现。")


def main(argv: list[str] | None = None) -> int:
    """程序入口，返回明确的整数退出码。

    只捕获“预期内”的失败并给出可读信息，不吞掉意外异常，
    也不把原始 traceback 直接抛给用户。
    """
    args = parse_args(argv)

    try:
        task_id = validate_task_id(args.task_id)
    except ValueError as exc:
        _print_error(str(exc))
        return EXIT_TASK_ID_ERROR

    try:
        profile_path = resolve_profile_path(args.profile)
    except (FileNotFoundError, IsADirectoryError) as exc:
        _print_error(str(exc))
        return EXIT_PROFILE_ERROR

    try:
        task_dir = create_task_directory(task_id)
    except FileExistsError as exc:
        _print_error(
            f"任务目录已存在，本工具不会覆盖或清空它：{exc}\n"
            "  请换一个 --task-id 后重试。"
        )
        return EXIT_TASK_DIR_EXISTS
    except (ValueError, OSError) as exc:
        _print_error(f"创建任务目录失败：{exc}")
        return EXIT_ARTIFACTS_ERROR

    _print_success(task_id, task_dir, profile_path)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
