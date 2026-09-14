"""系统地图（``system_map.json``）对应的 Pydantic 数据模型。

本模块只做一件事：**把「一次代码理解的结论」定义成结构化数据，并校验它是否自洽**。

它不扫描仓库、不解析 React 或 Flask 代码、不读取 YAML、不启动任何项目 ——
真正的分析逻辑属于 T009～T011。本轮只交付数据契约。

``SystemMap`` 和 ``RepositorySummary`` 的区别
-------------------------------------------
- ``RepositorySummary`` 回答「这是个什么项目」：语言、框架、依赖、入口文件；
- ``SystemMap`` 回答「这个系统的业务是怎么连起来的」：

      登录页（FrontendPage）
        → 前端发出的请求（FrontendRequest）
          → 后端声明的路由（BackendRoute）
            → 用到的数据模型（DataModel）
              = 一条调用链（CallChain）

四类对象分开存，用 ID 互相指
----------------------------
每类对象都有稳定的 ``id``；``CallChain`` 只保存这些 ID，不复制整份对象。
这样改一处名称时不会出现两份互相矛盾的数据。

为什么必须检查重复 ID 和悬空引用
--------------------------------
- **重复 ID**：同一类对象里出现两个相同 ID，后面「按 ID 找对象」就会随机命中一个，
  最终可能把 Bug 结论建立在错误的代码上；
- **悬空引用**：调用链指向一个并不存在的对象，报告里就会出现「查不到源头的链路」，
  这比缺少信息更危险 —— 它看起来像一条已经确认的结论。

来源与证据
----------
本模块**不重新定义**证据模型，直接复用 ``schemas.repository_summary`` 里的
``Finding``（值 + 来源类型 + 来源文件 + 行号或片段 + 置信度）。
每个对象都至少携带一条证据，规则与 T004 完全一致。

设计要点
--------
- 全部使用 Pydantic v2 写法：``model_config = ConfigDict(...)`` 搭配
  ``@field_validator`` / ``@model_validator``；不使用 v1 的 ``@validator``
  或旧式 ``class Config``；
- ``extra="forbid"``：字段名拼错会立即报错，不会被静默忽略；
- ``str_strip_whitespace=True``：字符串首尾空格自动清除；
- 列表字段一律 ``default_factory=list``，省略时得到空列表，
  不用可变对象做默认值，避免多个实例共享同一个列表。
"""

from __future__ import annotations

from enum import Enum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from schemas.repository_summary import Finding

__all__ = [
    "BackendRoute",
    "CallChain",
    "CallChainStatus",
    "DataModel",
    "DataModelKind",
    "FrontendPage",
    "FrontendRequest",
    "HttpMethod",
    "SystemMap",
]


# --------------------------------------------------------------------------
# 共用的校验小工具（放在模块级，避免每个模型重复写一遍同样的逻辑）
# --------------------------------------------------------------------------


def _require_text(value: str) -> str:
    """必填文本：拒绝空字符串与「只由空格组成」的字符串。

    ``str_strip_whitespace=True`` 已经清除了首尾空格，
    所以这里拿到的是修剪后的结果，只需判断是否为空。
    """
    if not value:
        raise ValueError("不能是空字符串，也不能只包含空格")
    return value


def _require_optional_text(value: str | None) -> str | None:
    """可选文本：可以不填，但一旦填写就不能是空的或只有空格。"""
    if value is not None and not value:
        raise ValueError("如果不填写请省略该字段，填写了就不能是空字符串或只包含空格")
    return value


# --------------------------------------------------------------------------
# 枚举
# --------------------------------------------------------------------------


class HttpMethod(str, Enum):
    """HTTP 请求方法。

    只保留本周需要的五种取值。写入时统一转成大写，
    这样 ``post`` 与 ``POST`` 不会被当成两种不同的方法。
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class CallChainStatus(str, Enum):
    """一条调用链的完成程度。

    三者的区别不是「写得好不好」，而是**证据够不够**：

    - ``complete``   页面、API、后端路由三段都已确认连通；
    - ``partial``    只确认了其中一部分关系，还有环节待补；
    - ``unresolved`` 看到了调用行为，但暂时无法确认目标。
    """

    COMPLETE = "complete"
    PARTIAL = "partial"
    UNRESOLVED = "unresolved"


class DataModelKind(str, Enum):
    """数据模型在代码里的类型。

    ``OTHER`` 是兜底值：遇到本周没预设的写法时，
    宁可如实标成「其他」，也不要硬塞进一个不准确的分类。
    """

    SQLALCHEMY = "sqlalchemy"
    PYDANTIC = "pydantic"
    DATACLASS = "dataclass"
    PLAIN_CLASS = "plain_class"
    OTHER = "other"


# --------------------------------------------------------------------------
# 五类对象
# --------------------------------------------------------------------------


class FrontendPage(BaseModel):
    """一个用户实际能打开的页面，例如登录页 ``/login``。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(description="页面唯一 ID，例如 page-login")
    name: str = Field(description="页面名称，例如 登录页")
    path: str = Field(description="前端访问路径，例如 /login")
    component_file: str | None = Field(
        default=None,
        description="对应组件文件，例如 frontend/src/pages/Login.jsx；暂时找不到时可以不填",
    )
    form_fields: list[Finding] = Field(
        default_factory=list,
        description="页面上识别到的表单字段，每个字段一条 Finding（value 为字段名）",
    )
    evidence: list[Finding] = Field(
        min_length=1,
        description="支撑「这个页面存在」的证据，至少一条",
    )

    @field_validator("id", "name", "path")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        return _require_text(value)

    @field_validator("component_file")
    @classmethod
    def _optional_must_not_be_blank(cls, value: str | None) -> str | None:
        return _require_optional_text(value)


class FrontendRequest(BaseModel):
    """前端代码主动发出的一个请求，例如 ``POST /api/login``。

    注意：这里记录的是**前端准备发送什么**。
    后端是否真的有对应路由，由 ``BackendRoute`` 单独回答，
    两者只能靠 ``CallChain`` 连接 —— 不能仅凭前端代码就断定后端存在该接口。
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(description="请求唯一 ID，例如 req-login")
    method: HttpMethod = Field(description="HTTP 方法，例如 POST")
    path: str = Field(description="请求路径，例如 /api/login")
    file_path: str = Field(description="发起请求的前端文件，例如 frontend/src/api/auth.js")
    request_fields: list[Finding] = Field(
        default_factory=list,
        description="随请求一起发送的字段，每个字段一条 Finding（value 为字段名）",
    )
    evidence: list[Finding] = Field(
        min_length=1,
        description="支撑「这里发过这个请求」的证据，至少一条",
    )

    @field_validator("id", "path", "file_path")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        return _require_text(value)

    @field_validator("method", mode="before")
    @classmethod
    def _normalize_method(cls, value: object) -> object:
        """HTTP 方法统一转成大写：``post`` 与 ``POST`` 视为同一个方法。"""
        if isinstance(value, str):
            return value.strip().upper()
        return value


class BackendRoute(BaseModel):
    """后端代码真正声明的路由，例如 Flask 的 ``@app.post("/api/login")``。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(description="路由唯一 ID，例如 route-login")
    method: HttpMethod = Field(description="HTTP 方法，例如 POST")
    path: str = Field(description="路由路径，例如 /api/login")
    handler_function: str = Field(description="处理函数名，例如 login")
    file_path: str = Field(description="声明该路由的后端文件，例如 backend/app.py")
    input_fields: list[Finding] = Field(
        default_factory=list,
        description="从请求中读取的输入字段（request.json / form / args），每个字段一条 Finding",
    )
    output_fields: list[Finding] = Field(
        default_factory=list,
        description="返回给前端的输出字段，每个字段一条 Finding",
    )
    status_codes: list[int] = Field(
        default_factory=list,
        description="可能返回的 HTTP 状态码，例如 [200, 400]",
    )
    related_data_model_ids: list[str] = Field(
        default_factory=list,
        description="该路由用到的数据模型 ID，只存 ID，指向 SystemMap.data_models",
    )
    evidence: list[Finding] = Field(
        min_length=1,
        description="支撑「这个路由存在」的证据，至少一条",
    )

    @field_validator("id", "path", "handler_function", "file_path")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        return _require_text(value)

    @field_validator("method", mode="before")
    @classmethod
    def _normalize_method(cls, value: object) -> object:
        """HTTP 方法统一转成大写，与 ``FrontendRequest`` 保持一致。"""
        if isinstance(value, str):
            return value.strip().upper()
        return value

    @field_validator("status_codes")
    @classmethod
    def _status_codes_must_be_valid(cls, value: list[int]) -> list[int]:
        """状态码必须是合法的 HTTP 状态码范围，避免把 0 或 9999 写进来。"""
        for code in value:
            if not 100 <= code <= 599:
                raise ValueError(f"HTTP 状态码必须在 100～599 之间，收到 {code}")
        return value


class DataModel(BaseModel):
    """代码里的数据结构或业务实体，例如 ``User``、``RegisterRequest``。

    这里说的是**被测项目代码中的数据模型**，不是本项目用来校验数据的 Pydantic 模型。
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(description="数据模型唯一 ID，例如 model-user")
    name: str = Field(description="模型名称，例如 User")
    kind: DataModelKind = Field(description="模型在代码里的类型，例如 sqlalchemy")
    file_path: str = Field(description="定义该模型的文件，例如 backend/models.py")
    fields: list[Finding] = Field(
        default_factory=list,
        description="模型包含的字段，每个字段一条 Finding（value 为字段名）",
    )
    evidence: list[Finding] = Field(
        min_length=1,
        description="支撑「这个模型存在」的证据，至少一条",
    )

    @field_validator("id", "name", "file_path")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        return _require_text(value)


class CallChain(BaseModel):
    """一条「页面 → API → 后端路由」的连接关系。

    它本身不存放页面或路由的内容，只保存它们的 ID：

    - ``page_id``         指向 ``SystemMap.frontend_pages``
    - ``api_id``          指向 ``SystemMap.frontend_requests``
    - ``backend_route_id`` 指向 ``SystemMap.backend_routes``
    - ``data_model_ids``  指向 ``SystemMap.data_models``

    尚未确认的环节留空即可，但**不允许**填一个不存在的 ID 来「凑完整」。
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(description="调用链唯一 ID，例如 chain-login")
    status: CallChainStatus = Field(description="链路状态：complete / partial / unresolved")
    page_id: str | None = Field(default=None, description="对应的页面 ID，未确认时留空")
    api_id: str | None = Field(default=None, description="对应的前端请求 ID，未确认时留空")
    backend_route_id: str | None = Field(
        default=None,
        description="对应的后端路由 ID，未确认时留空",
    )
    data_model_ids: list[str] = Field(
        default_factory=list,
        description="该链路涉及的数据模型 ID 列表",
    )
    evidence: list[Finding] = Field(
        min_length=1,
        description="支撑「这几段能连起来」的证据，至少一条",
    )

    @field_validator("id")
    @classmethod
    def _must_not_be_blank(cls, value: str) -> str:
        return _require_text(value)

    @field_validator("page_id", "api_id", "backend_route_id")
    @classmethod
    def _optional_ref_must_not_be_blank(cls, value: str | None) -> str | None:
        return _require_optional_text(value)

    @model_validator(mode="after")
    def _status_must_match_references(self) -> Self:
        """链路状态与引用的完整度必须对得上。

        - ``complete``：前端页面、前端请求、后端路由三段缺一不可，
          缺少任何一段都说明链路并没有真正打通，不允许标成「已完成」；
        - ``partial`` / ``unresolved``：至少要引用一个已经确认的对象，
          否则这条记录什么也没说明，不如不写。

        至于引用是否存在，单条链路看不到其他对象，由 ``SystemMap`` 统一检查。
        """
        references = {
            "page_id": self.page_id,
            "api_id": self.api_id,
            "backend_route_id": self.backend_route_id,
        }
        if self.status is CallChainStatus.COMPLETE:
            missing = [name for name, value in references.items() if value is None]
            if missing:
                raise ValueError(
                    "status=complete 的调用链必须同时给出 page_id、api_id、"
                    f"backend_route_id，当前缺少：{'、'.join(missing)}"
                )
        elif not any(references.values()):
            raise ValueError(
                "status 为 partial 或 unresolved 时，page_id / api_id / "
                "backend_route_id 至少要引用一个"
            )
        return self


def _collect_unique_ids(
    items: list[FrontendPage | FrontendRequest | BackendRoute | DataModel | CallChain],
    label: str,
) -> set[str]:
    """收集一组对象的 ID，同时检查是否出现重复。

    返回集合，供 ``SystemMap`` 检查「引用是否存在」时使用。
    """
    seen: set[str] = set()
    for item in items:
        if item.id in seen:
            raise ValueError(f"{label} 中出现重复 ID：{item.id}")
        seen.add(item.id)
    return seen


class SystemMap(BaseModel):
    """一次代码理解得到的完整系统地图。

    所有列表都可以留空 —— 分析器可以只填已经确认的部分，
    不必为了凑字段而编造内容。
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    frontend_pages: list[FrontendPage] = Field(
        default_factory=list,
        description="识别到的前端页面",
    )
    frontend_requests: list[FrontendRequest] = Field(
        default_factory=list,
        description="识别到的前端请求（注意：不代表后端一定存在对应路由）",
    )
    backend_routes: list[BackendRoute] = Field(
        default_factory=list,
        description="识别到的后端路由",
    )
    data_models: list[DataModel] = Field(
        default_factory=list,
        description="识别到的数据模型",
    )
    call_chains: list[CallChain] = Field(
        default_factory=list,
        description="页面 → API → 后端路由的连接关系",
    )

    @model_validator(mode="after")
    def _ids_must_be_unique_and_references_must_exist(self) -> Self:
        """整张地图的自洽性检查。

        1. 同一类对象里不能有重复 ID；
        2. 凡是写了引用（调用链的 page_id / api_id / backend_route_id /
           data_model_ids，以及后端路由关联的 related_data_model_ids），
           被引用的对象必须真实存在于这张地图里。

        没有确认的关系请留空，不要编造 ID。
        """
        page_ids = _collect_unique_ids(self.frontend_pages, "frontend_pages")
        request_ids = _collect_unique_ids(self.frontend_requests, "frontend_requests")
        route_ids = _collect_unique_ids(self.backend_routes, "backend_routes")
        data_model_ids = _collect_unique_ids(self.data_models, "data_models")
        _collect_unique_ids(self.call_chains, "call_chains")

        for route in self.backend_routes:
            for reference in route.related_data_model_ids:
                if reference not in data_model_ids:
                    raise ValueError(
                        f"后端路由 {route.id} 关联了不存在的数据模型 ID：{reference}"
                    )

        for chain in self.call_chains:
            references = (
                ("page_id", chain.page_id, page_ids),
                ("api_id", chain.api_id, request_ids),
                ("backend_route_id", chain.backend_route_id, route_ids),
            )
            for name, reference, existing in references:
                if reference is not None and reference not in existing:
                    raise ValueError(
                        f"调用链 {chain.id} 引用了不存在的 {name}：{reference}"
                    )
            for reference in chain.data_model_ids:
                if reference not in data_model_ids:
                    raise ValueError(
                        f"调用链 {chain.id} 引用了不存在的数据模型 ID：{reference}"
                    )
        return self
