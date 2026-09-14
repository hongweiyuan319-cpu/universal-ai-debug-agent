"""仓库扫描结果（``repository_summary.json``）对应的 Pydantic 数据模型。

本模块只做一件事：**把「一次仓库扫描的结论」的数据结构定义清楚，并校验它是否合法**。

它不读取文件、不扫描目录、不检查路径是否存在、不执行任何命令 ——
真正的扫描逻辑属于 T008 的 ``core/repository_scanner.py``，
本模块只是那份扫描结果必须遵守的数据契约。

为什么每条结论都要带「来源」和「置信度」
--------------------------------------
Week 1 的验收标准要求：每一条结论都要能说清“从哪来”，
并且“不确认的内容不会伪装成确定事实”。
所以这里不把结论设计成裸字符串（例如 ``languages: list[str]``），
而是设计成 ``Finding``：值 + 来源类型 + 来源文件 + 定位 + 置信度。

三类来源的含义
--------------
- ``observed``：代码里直接看到的事实（例如 ``package.json`` 里写了 ``react``）；
- ``declared``：人工在选填表 ``project-profile.yaml`` 里声明的信息；
- ``inferred``：模型根据线索推断出来的结论，天生不确定，必须带更低的置信度。

设计要点
--------
- 全部使用 Pydantic v2 写法：``model_config = ConfigDict(...)`` 搭配
  ``@field_validator`` / ``@model_validator``；不使用 v1 的 ``@validator``
  或旧式 ``class Config``。
- ``extra="forbid"``：多写一个没定义过的字段会直接报错，
  避免字段名拼错后被系统悄悄忽略。
- ``str_strip_whitespace=True``：字符串首尾的多余空格会被自动清除。
- 列表字段一律使用 ``default_factory=list``，省略时得到空列表而不是 ``None``，
  调用方可以直接遍历，不会因为缺少可选字段而崩溃。
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

__all__ = ["Finding", "RepositorySummary", "SourceType"]


class SourceType(str, Enum):
    """一条结论的来源类型。

    只有这三种取值，保证后续「预期 vs 实际」的对比里，
    代码事实、人工声明、模型推断永远不会被混为一谈。
    """

    OBSERVED = "observed"
    DECLARED = "declared"
    INFERRED = "inferred"


class Finding(BaseModel):
    """一条「带证据的扫描结论」，是本模块最基础的组成单元。

    例如「这个仓库使用 React」就是一条 Finding：

    - ``value``       = ``"React"``
    - ``source_type`` = ``"observed"``
    - ``file_path``   = ``"frontend/package.json"``
    - ``snippet``     = ``'"react": "^18.2.0"'``
    - ``version``     = ``"18.2.0"``
    - ``confidence``  = ``1.0``

    同一个模型同时用于语言、框架、依赖和入口文件，
    因此不需要为每一类结论各写一个类，避免出现复杂的继承体系。
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    value: str = Field(description="结论的值，例如 Python、React、frontend/src/main.tsx")
    source_type: SourceType = Field(
        description="来源类型：observed（代码事实）/ declared（人工声明）/ inferred（模型推断）",
    )
    file_path: str = Field(
        description="该结论的来源文件，相对仓库根目录，例如 backend/requirements.txt",
    )
    line: int | None = Field(
        default=None,
        ge=1,
        description="来源文件中的行号（从 1 开始）。没有行号时必须填写 snippet",
    )
    snippet: str | None = Field(
        default=None,
        description="来源处的代码片段或配置原文，用于人工复核",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="置信度，取值 0～1；1.0 表示有直接证据，越小越不确定",
    )
    version: str | None = Field(
        default=None,
        description="该结论的版本号，例如 18.2.0；入口文件这类结论通常不填",
    )

    @field_validator("value", "file_path")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        """拒绝空字符串和「只由空格组成」的字符串。

        注意：``str_strip_whitespace=True`` 已经在校验前清除了首尾空格，
        所以这里拿到的 ``value`` 是修剪后的结果，只需判断是否为空即可。
        """
        if not value:
            raise ValueError("不能是空字符串，也不能只包含空格")
        return value

    @field_validator("version", "snippet")
    @classmethod
    def _optional_text_must_not_be_blank(cls, value: str | None) -> str | None:
        """可选的文本字段：可以不填，但一旦填写就不能是空的或只有空格。"""
        if value is not None and not value:
            raise ValueError("如果不填写请省略该字段，填写了就不能是空字符串或只包含空格")
        return value

    @model_validator(mode="after")
    def _must_have_location_and_honest_confidence(self) -> Self:
        """检查「定位信息」和「置信度」这两条诚实性约束。

        1. 每条结论至少要能定位：``line`` 与 ``snippet`` 不能同时为空，
           否则这条结论无法被人工复核。
        2. ``inferred`` 是推断出来的结论，因此置信度必须小于 1.0，
           不允许把推断包装成 100% 确定的代码事实。
        """
        if self.line is None and self.snippet is None:
            raise ValueError("每条结论都必须能定位：line 与 snippet 至少填写一个")
        if self.source_type is SourceType.INFERRED and self.confidence >= 1.0:
            raise ValueError("source_type 为 inferred 时，confidence 必须小于 1.0")
        return self


class RepositorySummary(BaseModel):
    """一次仓库扫描的完整结论。

    它回答的是「这是个什么项目」：用什么语言、前后端各用什么框架、
    依赖有哪些、前后端的入口文件分别在哪里。

    所有列表字段都是可选的，省略时得到空列表 ——
    扫描器可以先只填已知的部分，不必为了凑字段而编造内容。
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    repository_path: Path = Field(
        description="被扫描的仓库路径。只做记录，不检查该路径是否存在（沿用 D005）",
    )
    languages: list[Finding] = Field(
        default_factory=list,
        description="识别到的编程语言，例如 Python、JavaScript、TypeScript",
    )
    frontend_frameworks: list[Finding] = Field(
        default_factory=list,
        description="识别到的前端框架或构建工具，例如 React、Vite",
    )
    backend_frameworks: list[Finding] = Field(
        default_factory=list,
        description="识别到的后端框架，例如 Flask、FastAPI",
    )
    dependencies: list[Finding] = Field(
        default_factory=list,
        description="识别到的依赖，value 为包名，version 为版本号",
    )
    frontend_entry_files: list[Finding] = Field(
        default_factory=list,
        description="前端入口文件，value 为文件路径，例如 frontend/src/main.tsx",
    )
    backend_entry_files: list[Finding] = Field(
        default_factory=list,
        description="后端入口文件，value 为文件路径，例如 backend/app.py",
    )

    @field_validator("repository_path", mode="before")
    @classmethod
    def _path_must_not_be_blank(cls, value: object) -> object:
        """仓库路径不能是空字符串，也不能只由空格组成。

        使用 ``mode="before"``：在 Pydantic 把输入转成 ``Path`` 对象**之前**
        先检查原始值。否则 ``"   "`` 会被转成当前目录 ``.``，
        等发现时已经看不出「调用方其实什么都没填」。
        """
        if isinstance(value, str):
            trimmed = value.strip()
            if not trimmed:
                raise ValueError("repository_path 不能是空字符串，也不能只包含空格")
            return trimmed
        return value
