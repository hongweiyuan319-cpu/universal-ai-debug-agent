"""Pydantic 数据模型（第 1 周 · 代码理解原型 V0.1）。

本包定义跨模块共享的数据契约，保证 artifacts 产物可被校验。

规划中的子模块：

- ``project_profile``     : 选填项目信息表 ``project-profile.yaml`` 的模型
- ``repository_summary``  : 技术栈、依赖、入口文件摘要
- ``system_map``          : 页面、API、后端路由、数据模型、调用链

约定
----
凡表达「扫描结论」的模型，都使用 ``Finding``：
结论的值（``value``）必须同时带上来源类型（``source_type``）、
来源文件（``file_path``）、定位（``line`` 或 ``snippet``）与置信度（``confidence``），
禁止用默认值伪装成确定事实。

``SystemMap`` 中的页面、请求、路由、数据模型、调用链之间**只用 ID 互相引用**，
不复制整份对象；引用必须真实存在，未确认的关系留空而不是编造 ID。
"""

from schemas.project_profile import BusinessRule, ProjectProfile, StartupInfo
from schemas.repository_summary import Finding, RepositorySummary, SourceType
from schemas.system_map import (
    BackendRoute,
    CallChain,
    CallChainStatus,
    DataModel,
    DataModelKind,
    FrontendPage,
    FrontendRequest,
    HttpMethod,
    SystemMap,
)

__all__ = [
    "BackendRoute",
    "BusinessRule",
    "CallChain",
    "CallChainStatus",
    "DataModel",
    "DataModelKind",
    "Finding",
    "FrontendPage",
    "FrontendRequest",
    "HttpMethod",
    "ProjectProfile",
    "RepositorySummary",
    "SourceType",
    "StartupInfo",
    "SystemMap",
]

__version__ = "0.1.0"
