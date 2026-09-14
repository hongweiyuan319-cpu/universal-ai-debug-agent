# 第 1 周任务清单｜代码理解原型 V0.1

> **本周只做一件事：让 Agent 在不依赖人工讲解的情况下，读懂一个 React + Flask 项目的主要结构，并输出可审阅的系统地图。**

---

## 1. 本周总体目标

输入一个代码仓库和一份选填项目信息表后，Agent 能识别并关联：

```text
前端页面 / 表单
  → 前端接口调用
  → Flask API 路由
  → 请求参数与响应字段
  → 数据库模型或持久化位置
```

第 1 周结束时，系统应输出 `system_map.json`，以登录注册 Demo 为例：

```text
/register 页面
  → POST /api/register
  → Flask register 路由
  → username / password 参数
  → users 数据表

/login 页面
  → POST /api/login
  → Flask login 路由
  → 登录态 / Token / Session
```

**本周不执行测试、不生成 Bug、不接 Playwright。**

---

## 2. 本周完成效果

| 输入 | Agent 要做到 | 可见产物 |
|---|---|---|
| React + Flask 代码仓库 | 判断前后端技术栈、入口与依赖 | `repository_summary.json` |
| `project-profile.yaml` | 读取环境、业务描述和手工补充规则 | `project_context.json` |
| 前端 + 后端源码 | 找到页面、接口、参数与调用链 | `system_map.json` |
| 未确认的推断 | 标明置信度和证据文件 | `analysis_notes.md` |

### 本周验收标准

- [ ] 对当前登录注册系统，能识别注册页和登录页；
- [ ] 能识别注册、登录 API；
- [ ] 能提取 `username`、`password` 等关键字段；
- [ ] 能建立至少两条“页面 → API → 后端路由”的链路；
- [ ] 每一条结论带来源文件与行号或代码片段定位；
- [ ] 不确认的内容不会伪装成确定事实。

---

## 3. 本周范围

### 做

- React + Flask 首个技术栈适配；
- 静态代码扫描；
- 固定格式选填表读取与校验；
- 系统地图 JSON 输出；
- 命令行运行入口；
- 当前登录注册 Demo 验证。

### 不做

- API 测试、`httpx`、Playwright；
- LLM 自动生成测试用例；
- Bug 判定、报告、FastAPI 服务；
- 自动启动复杂环境；
- 任意语言或任意框架支持；
- 自动修复代码。

---

## 4. 目录与模块清单

```text
universal-ai-debug-agent/
├── core/
│   ├── repository_scanner.py      # 扫描目录、识别技术栈和入口文件
│   ├── flask_analyzer.py          # 提取 Flask 路由、参数、响应与模型
│   ├── react_analyzer.py          # 提取 React 路由、页面、表单和请求
│   ├── call_chain_builder.py      # 匹配“页面 → API → 后端路由”
│   └── context_merger.py          # 合并代码事实与选填表信息
├── schemas/
│   ├── project_profile.py
│   ├── repository_summary.py
│   └── system_map.py
├── templates/
│   └── project-profile.yaml
├── artifacts/
│   └── task_<id>/
├── run_discovery.py
└── README.md
```

---

## 5. 每日任务清单

| 日期 | 目标 | 任务 | 当天验收 |
|---|---|---|---|
| Day 1 | 建立骨架 | 初始化目录；定义 Pydantic Schema；准备 Demo 仓库路径 | 可运行空入口，生成任务目录 |
| Day 2 | 识别项目 | 实现目录扫描、依赖识别、入口文件发现 | 输出前后端技术栈与入口文件 |
| Day 3 | 看懂 Flask | 提取路由、HTTP 方法、参数、响应和模型引用 | 输出 `/api/register`、`/api/login` |
| Day 4 | 看懂 React | 提取页面路由、表单字段、Axios/Fetch 请求 | 输出 `/register`、`/login` 与字段 |
| Day 5 | 连成业务链 | 匹配前端请求和 Flask 路由；生成系统地图 | 输出两条完整调用链 |
| Day 6 | 接入选填表 | 读取 YAML；合并业务规则；加入来源与置信度 | 规则与代码事实不混淆 |
| Day 7 | 联调与整理 | 连续运行、修复异常、补 README 与示例产物 | 一条命令稳定产出地图 |

---

## 6. 每日详细 Checklist

### Day 1｜项目骨架与数据模型

- [x] 建立 `core/`、`schemas/`、`templates/`、`artifacts/`；
- [x] 定义 `ProjectProfile`：项目名、仓库路径、启动信息、业务规则；
- [x] 定义 `RepositorySummary`：语言、框架、依赖、入口文件；
- [x] 定义 `SystemMap`：页面、API、后端路由、数据模型、调用链；
- [ ] 建立 `run_discovery.py` 命令行入口；
- [x] 创建 `project-profile.yaml` 模板。

**产出：** 可被 Pydantic 校验的空 `system_map.json`。

### Day 2｜仓库扫描与技术栈识别

- [ ] 扫描目录树，排除 `node_modules`、`.git`、虚拟环境、构建产物；
- [ ] 检测 `package.json`、`requirements.txt`、`pyproject.toml`；
- [ ] 判断 React、Flask、SQLite 是否存在；
- [ ] 查找前端与后端入口文件；
- [ ] 输出 `repository_summary.json`；
- [ ] 对未识别的项目给出“当前不支持”的明确提示。

**产出：** 技术栈、入口文件、依赖摘要。

### Day 3｜Flask 后端分析器

- [ ] 解析 `@app.route()`、Blueprint 路由；
- [ ] 提取 HTTP 方法、路径和函数名；
- [ ] 识别 `request.json`、`request.form`、`request.args` 中的参数；
- [ ] 识别 `jsonify()`、状态码和错误信息；
- [ ] 尝试识别 SQLite、SQLAlchemy 或用户存储文件；
- [ ] 为每项发现保存源码位置。

**产出：** `backend_apis` 列表。

### Day 4｜React 前端分析器

- [ ] 识别 React Router 的页面路由；
- [ ] 识别 `<input>`、`Form.Item`、`name`、`placeholder`；
- [ ] 提取 Axios / Fetch 的请求方法与 URL；
- [ ] 识别提交按钮与事件函数；
- [ ] 将注册、登录页面关联到对应表单字段；
- [ ] 为每项发现保存源码位置。

**产出：** `frontend_pages` 和 `frontend_requests` 列表。

### Day 5｜调用链构建器

- [ ] 根据 URL + HTTP 方法匹配前端请求和 Flask 路由；
- [ ] 输出 `Page → Request → Route → Storage` 链路；
- [ ] 处理 API 前缀差异，如 `/api`、`/v1`；
- [ ] 标记“已确认匹配”和“疑似匹配”；
- [ ] 为未匹配请求输出待人工补充项。

**产出：** 第一版 `system_map.json`。

### Day 6｜选填表与事实合并

- [ ] 完成 `project-profile.yaml` 校验；
- [ ] 合并 `business_description`、`test_scope`、`business_rules`；
- [ ] 规则按来源标记为 `declared`；
- [ ] 代码扫描结果标记为 `observed`；
- [ ] 无法确认的业务推断标记为 `inferred`；
- [ ] 输出 `analysis_notes.md`，列出待确认项。

**产出：** 可审阅、可追溯的系统地图。

### Day 7｜完整联调与周验收

- [ ] 用当前登录注册 Demo 完整运行；
- [ ] 检查 JSON 是否符合 Schema；
- [ ] 对错误路径、缺失配置、未知框架给出清晰报错；
- [ ] 连续执行 3 次，确认输出一致；
- [ ] 写 README：安装、配置、运行、示例输出；
- [ ] 整理下周要接入的 API 测试接口清单。

**产出：** 可演示的 V0.1 代码理解原型。

---

## 7. 周末最终运行方式

```bash
python run_discovery.py \
  --repo /path/to/login-register-demo \
  --profile templates/project-profile.yaml
```

预期生成：

```text
artifacts/task_001/
├── repository_summary.json
├── project_context.json
├── system_map.json
└── analysis_notes.md
```

---

## 8. 本周完成的定义

不是“代码写了很多”，而是满足下面这一句话：

> 给 Agent 一个陌生的 React + Flask 登录注册项目，它无需人工解释，就能说清楚注册和登录分别在哪个页面触发、调用哪个接口、后端由哪个路由处理、涉及哪些字段与数据存储。

做到这一点，才进入第 2 周的“自动生成 API 测试并发现 Bug”。
