"""核心分析模块（第 1 周 · 代码理解原型 V0.1）。

本包负责从代码仓库中提取事实，不执行测试、不生成 Bug。

规划中的子模块：

- ``repository_scanner`` : 扫描目录、识别技术栈和入口文件
- ``flask_analyzer``     : 提取 Flask 路由、参数、响应与模型
- ``react_analyzer``     : 提取 React 路由、页面、表单和请求
- ``call_chain_builder`` : 匹配「页面 → API → 后端路由」
- ``context_merger``     : 合并代码事实与选填表信息

约定
----
所有结论都必须携带来源定位（``file`` / ``line`` / ``snippet``），
并按 ``observed`` / ``declared`` / ``inferred`` 标记置信度来源。
"""

__version__ = "0.1.0"
