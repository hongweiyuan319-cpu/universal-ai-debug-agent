"""选填项目信息表（``project-profile.yaml``）对应的 Pydantic 数据模型。

本模块只做一件事：**把「一份项目档案」的数据结构定义清楚，并校验它是否合法**。

它不读取 YAML 文件、不扫描代码仓库、不启动任何项目，
也不执行 ``startup`` 里的启动命令 —— 那些命令本轮只作为配置信息保存。

设计要点
--------
- 全部使用 Pydantic v2 写法：``model_config = ConfigDict(...)`` 搭配
  ``@field_validator``；不使用 v1 的 ``@validator`` 或旧式 ``class Config``。
- ``extra="forbid"``：多写一个没定义过的字段会直接报错，
  避免字段名拼错后被系统悄悄忽略。
- ``str_strip_whitespace=True``：字符串首尾的多余空格会被自动清除。
"""

from __future__ import annotations

from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator

__all__ = ["BusinessRule", "StartupInfo", "ProjectProfile"]


class BusinessRule(BaseModel):
    """一条业务规则，例如 ``R-REG-001 / 用户名长度不得少于6位``。

    业务规则是整个系统判断「是不是 Bug」的最高依据：
    代码能说明「系统做了什么」，而业务规则说明「系统应该做什么」。
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    id: str = Field(description="规则编号，例如 R-REG-001")
    rule: str = Field(description="规则内容，例如 用户名长度不得少于6位")

    @field_validator("id", "rule")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        """拒绝空字符串和「只由空格组成」的字符串。

        注意：``str_strip_whitespace=True`` 已经在校验前清除了首尾空格，
        所以这里拿到的 ``value`` 是修剪后的结果，只需判断是否为空即可。
        """
        if not value:
            raise ValueError("不能是空字符串，也不能只包含空格")
        return value


class StartupInfo(BaseModel):
    """被测系统的启动信息。

    ``backend`` / ``frontend`` 只是**配置文本**，本模块绝对不会去执行它们。
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    backend: str | None = Field(default=None, description="后端启动命令，例如 python app.py")
    frontend: str | None = Field(default=None, description="前端启动命令，例如 npm run dev")
    base_url: AnyHttpUrl | None = Field(
        default=None,
        description="系统访问地址，必须是合法的 http 或 https 地址",
    )


class ProjectProfile(BaseModel):
    """一份完整的项目档案。

    只有 ``project_name`` 和 ``repository_path`` 是必填的；
    其余字段留空时由 Agent 后续从代码和运行行为中推断。

    关于 ``repository_path``：本轮**故意不检查**该路径是否真实存在，
    因为「路径是否存在」属于运行环境问题，不属于数据格式问题。
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    project_name: str = Field(description="项目名称")
    repository_path: Path = Field(description="代码仓库路径")
    startup: StartupInfo = Field(
        default_factory=StartupInfo,
        description="启动信息，不填写时自动创建一个空的 StartupInfo",
    )
    business_rules: list[BusinessRule] = Field(
        default_factory=list,
        description="业务规则列表，不填写时默认为空列表",
    )

    @field_validator("project_name")
    @classmethod
    def _name_must_not_be_blank(cls, value: str) -> str:
        """项目名不能是空字符串，也不能只由空格组成。"""
        if not value:
            raise ValueError("project_name 不能是空字符串，也不能只包含空格")
        return value

    @field_validator("repository_path", mode="before")
    @classmethod
    def _path_must_not_be_blank(cls, value: object) -> object:
        """仓库路径不能是空字符串，也不能只由空格组成。

        使用 ``mode="before"``：在 Pydantic 把输入转成 ``Path`` 对象**之前**
        先检查原始值。否则 ``"   "`` 会被转成当前目录 ``.``，
        等发现时已经看不出「用户其实什么都没填」。
        """
        if isinstance(value, str):
            trimmed = value.strip()
            if not trimmed:
                raise ValueError("repository_path 不能是空字符串，也不能只包含空格")
            return trimmed
        return value
