# Task Log

用途：帮助新的开发者或 AI 在 1～2 分钟内理解项目目标、当前状态、已完成工作、验证证据和下一步行动。

维护原则：顶部“当前快照”随进度更新；底部“历史任务记录”只追加、不覆盖。不要粘贴完整聊天、完整源代码或冗长终端输出。

最后更新：2026-09-14 05:23 UTC

日志维护者：GitHub Copilot

---

## 0. 阅读顺序

接手项目时，请依次阅读：

1. 一分钟项目摘要；
2. 当前状态快照；
3. 8. 下一步交接；
4. 与当前任务相关的 6. 关键设计决定；
5. 必要时再查看 10. 历史任务记录。

如果本日志与代码或实际测试结果冲突，以代码和最新验证结果为准，并在本轮任务结束时修正日志。

---

## 1. 一分钟项目摘要

### 1.1 最终目标

输入一个代码仓库和一份固定格式的选填项目信息表，Agent 自动理解业务、生成并执行测试、定位缺陷，并输出可复现的 Debug 报告（Bug JSON + Markdown/HTML 报告）。

### 1.2 当前阶段

当前版本：V0.1

当前里程碑：Week 1 / 代码理解原型

当前阶段目标：让 Agent 在不依赖人工讲解的情况下读懂一个 React + Flask 项目的主要结构，并输出可审阅、可追溯的 `system_map.json`。

### 1.3 当前范围

- React + Flask 首个技术栈适配；
- 静态代码扫描（Flask 路由、React 页面与请求）；
- 固定格式选填表（`project-profile.yaml`）读取与校验；
- 系统地图 JSON 输出；
- 命令行运行入口。

### 1.4 当前不做

- API 测试（`httpx`）、页面测试（Playwright）；
- LLM 自动生成测试用例；
- Bug 判定、报告生成、FastAPI 服务；
- 自动启动被测环境；
- 任意语言或任意框架支持；
- 自动修复业务代码。

### 1.5 当前真实能力

已经可以做到：

- 用 Python 3.12 + Pydantic v2 定义并校验“项目档案”的数据格式（`ProjectProfile` / `StartupInfo` / `BusinessRule`）；
- 定义并校验“仓库扫描结果”的数据格式（`RepositorySummary` / `Finding` / `SourceType`）；
- 定义并校验“系统地图”的数据格式（`SystemMap` / `FrontendPage` / `FrontendRequest` / `BackendRoute` / `DataModel` / `CallChain` 及 3 个枚举），并检查同类对象 ID 是否重复、调用链引用是否真实存在；
- 所有“结论型”数据强制携带来源类型、来源文件、定位与 0～1 置信度；
- 拒绝空字符串、纯空格字符串、拼错的字段名、非 http/https 的 `base_url`、越界置信度、非法的来源类型、非法 HTTP 方法、无效状态码；
- 把模型安全地转换为 Python 字典与 JSON，并导出 JSON Schema。

尚不能做到（**定义了数据格式 ≠ 系统已经能生成它**）：

- 读取 `project-profile.yaml`（YAML 解析未实现）；
- 扫描仓库、识别技术栈与入口文件（只有数据契约，没有扫描逻辑）；
- 识别 Flask 路由、React 页面、表单字段、调用链（属于 T009～T011）；
- **自动生成 `system_map.json`**：`SystemMap` 目前只能手工构造，没有任何代码去填充它；
- 通过命令行一条命令跑完整个发现流程。

---

## 2. 当前状态快照

| 项目 | 当前值 |
|---|---|
| 当前任务 | T002-B：配置 GitHub 远程仓库并首次推送 |
| 当前状态 | completed |
| 上一个完成任务 | T005：定义 SystemMap 数据模型 |
| 下一任务 | T006：创建 project-profile.yaml 模板 |
| 当前里程碑完成度 | Day 1 清单 4/6 项；Week 1 共 7 天，处于 Day 1 |
| 阻塞项 | 无 |
| 最后一次成功验证 | 2026-09-14 05:23 UTC；首次推送成功（`origin/main` = `ea3d6d3`，14 个文件，与本地完全一致） |
| 日志维护者 | GitHub Copilot |

### 状态定义

| 状态 | 含义 | 允许的下一状态 |
|---|---|---|
| planned | 已规划，尚未开始 | in_progress、blocked |
| in_progress | 正在实现 | verification_needed、blocked |
| verification_needed | 实现完成，等待或正在验证 | completed、in_progress、blocked |
| completed | 验收条件满足且有验证证据 | ready |
| ready | 上一步结束，可以启动下一任务 | in_progress |
| blocked | 因明确问题无法继续 | in_progress、planned |

---

## 3. 任务总览

| ID | 任务 | 状态 | 验收摘要 | 依赖 |
|---|---|---|---|---|
| T001 | 建立项目骨架与目录结构 | completed | `core/`、`schemas/`、`templates/`、`artifacts/` 四个目录就位 | 无 |
| T002 | 环境与现状检查（只读） | completed | 确认解释器、依赖缺口、无测试框架、非 Git 仓库 | T001 |
| T002-A | 落实 Q002 / Q003：Git 版本控制与依赖锁定 | completed | `git init -b main` 成功；`requirements.lock` 与 `pip freeze` 完全一致 | T002、T004 |
| T002-B | 配置 GitHub 远程仓库并首次推送 | completed | 仓库可见性 PRIVATE，`origin/main` 与本地 `HEAD` 同一提交（14 个文件） | T002-A、T005 |
| T003 | 实现 ProjectProfile 数据模型 | completed | 三个模型通过 10 项最小验证 | T002 |
| T004 | 定义 RepositorySummary 数据模型 | completed | 技术栈/依赖/入口文件可通过 Pydantic 校验，每条结论带来源与置信度（26/26 PASS） | T003 |
| T005 | 定义 SystemMap 数据模型 | completed | 页面/API/路由/数据模型/调用链可通过 Pydantic 校验，并检查重复 ID 与悬空引用（49/49 PASS） | T004 |
| T006 | 创建 project-profile.yaml 模板 | planned | 模板字段与 `ProjectProfile` 完全一致 | T003 |
| T007 | 建立 run_discovery.py 命令行入口 | planned | 一条命令生成 `artifacts/task_<id>/` 目录 | T006 |
| T008 | 仓库扫描与技术栈识别（Day 2） | planned | 输出 `repository_summary.json` | T007 |
| T009 | Flask 后端分析器（Day 3） | planned | 输出 `backend_apis` 列表 | T008 |
| T010 | React 前端分析器（Day 4） | planned | 输出 `frontend_pages`、`frontend_requests` | T009 |
| T011 | 调用链构建器（Day 5） | planned | 输出两条完整“页面 → API → 后端路由”链路 | T010 |
| T012 | 选填表与事实合并（Day 6） | planned | `declared` / `observed` / `inferred` 三类来源可分 | T011 |
| T013 | 完整联调与周验收（Day 7） | planned | 一条命令连续 3 次稳定产出系统地图 | T012 |

### 当前里程碑清单

Week 1 验收标准（全部未达成）：

- [ ] 对当前登录注册系统，能识别注册页和登录页；
- [ ] 能识别注册、登录 API；
- [ ] 能提取 `username`、`password` 等关键字段；
- [ ] 能建立至少两条“页面 → API → 后端路由”的链路；
- [ ] 每一条结论带来源文件与行号或代码片段定位；
- [ ] 不确认的内容不会伪装成确定事实。

Day 1 清单进度：

- [x] 建立 `core/`、`schemas/`、`templates/`、`artifacts/`；
- [x] 定义 `ProjectProfile`：项目名、仓库路径、启动信息、业务规则；
- [x] 定义 `RepositorySummary`：语言、框架、依赖、入口文件；
- [x] 定义 `SystemMap`：页面、API、后端路由、数据模型、调用链；
- [ ] 建立 `run_discovery.py` 命令行入口；
- [ ] 创建 `project-profile.yaml` 模板。

---

## 4. 当前代码与文档状态

| 文件或目录 | 作用 | 状态 | 最近相关任务 |
|---|---|---|---|
| `core/` | 核心分析模块包（当前只有 docstring，无实现） | 已实现（占位） | T001 |
| `core/__init__.py` | 声明规划中的 5 个分析器子模块 | 已实现（占位） | T001 |
| `schemas/` | 跨模块共享的数据契约包 | 已实现 | T005 |
| `schemas/__init__.py` | 导出 15 个公开模型（新增 9 个 SystemMap 相关名字） | 已验证 | T005 |
| `schemas/project_profile.py` | `BusinessRule`、`StartupInfo`、`ProjectProfile` | 已验证 | T003 |
| `schemas/repository_summary.py` | `Finding`、`SourceType`、`RepositorySummary` | 已验证 | T004 |
| `schemas/system_map.py` | `FrontendPage`、`FrontendRequest`、`BackendRoute`、`DataModel`、`CallChain`、`SystemMap` 及 `HttpMethod`、`CallChainStatus`、`DataModelKind` | 已验证 | T005 |
| `templates/` | 配置模板目录（当前为空，仅 `.gitkeep`） | 未开始 | T001 |
| `artifacts/` | 运行期产物目录（当前为空，仅 `.gitkeep`） | 未开始 | T001 |
| `requirements.txt` | 运行依赖声明（`pydantic>=2,<3`），注释说明锁文件用法 | 已验证 | T002-A |
| `requirements.lock` | 精确版本锁定（`pip freeze` 产物，5 个包） | 已验证 | T002-A |
| `.gitignore` | 忽略 `.venv/`、`__pycache__/`、`*.pyc`、`.DS_Store` | 已生效（T002-A 起纳入 Git） | T002-A |
| `.venv/` | 项目专属虚拟环境（Python 3.12.13） | 已验证 | T003 |
| `logs/universal-ai-debug-agent-design.md` | 总体设计文档（V1 范围、架构、目录规划） | 已实现 | 无 |
| `logs/week-1-code-understanding-plan.md` | 第 1 周任务清单（Day 1～Day 7） | 已实现 | 无 |
| `logs/logs/TASK_LOG_template.md` | 本日志的模板与维护规则 | 已实现 | 无 |
| `logs/logs/TASK_LOG_1.md` | 本文件 | 已实现 | T005 |

尚未建立（属于 V1 后期，本阶段不需要）：`app/`、`executors/`、`projects/`。

### 关键模块关系

```text
① project-profile.yaml（未实现，T006）
        ↓
② ProjectProfile 校验（已实现，T003）   ←── 代码仓库扫描（未实现，T008）
        ↓                                    ※ 扫描结果的数据契约已就位（已实现，T004）
③ 系统地图 system_map.json（未实现，T005）
        ↓
④ API / UI 测试与报告（不属于 Week 1）
```

### 事实来源优先级

出现冲突时按以下顺序判断：

1. 当前代码与配置；
2. 最新实际测试结果；
3. 已接受的设计决定；
4. 本任务日志；
5. 旧计划或聊天记录。

---

## 5. 技术环境与运行方式

### 5.1 环境

| 项目 | 当前值 |
|---|---|
| 操作系统 | macOS（Apple Silicon，arm64） |
| Python / Node 等运行时 | Python 3.12.13（来自 `.venv`）；Node 本轮未使用（后续测试 React Demo 时才需要） |
| 虚拟环境 | `.venv/`（项目根目录，已在 `.gitignore` 中忽略） |
| 包管理器 | pip（始终通过 `.venv/bin/python -m pip` 调用） |
| 核心依赖 | pydantic 2.13.5、pydantic-core 2.46.5、annotated-types 0.8.0、typing-extensions 4.16.0、typing-inspection 0.4.4 |
| 测试框架 | 暂未安装（本轮明确不引入 pytest） |
| 依赖锁定 | `requirements.lock`（5 个包，与 `.venv` 当前安装完全一致） |
| 是否为 Git 仓库 | 是（`main` 分支）；远程 `origin` → `git@github.com:hongweiyuan319-cpu/universal-ai-debug-agent.git`（PRIVATE） |

其他可用但**不应使用**的解释器：`/usr/bin/python3`（3.9.6，CommandLineTools 自带）、`/opt/miniconda3/bin/python`（3.13.13，Conda base）。

### 5.2 安装命令

```bash
# 在项目根目录执行
python3.12 -m venv .venv

# 方式一（复现验证环境）：按锁定版本安装
.venv/bin/python -m pip install -r requirements.lock

# 方式二（开发期，允许 pydantic 小版本升级）：按范围声明安装
.venv/bin/python -m pip install -r requirements.txt
```

### 5.3 运行命令

```bash
# 尚未建立：命令行入口 run_discovery.py 属于 T007
```

### 5.4 测试与检查命令

```bash
# 正式测试套件尚未建立（未安装 pytest）。当前可用的最小冒烟检查：
.venv/bin/python -c "from schemas import ProjectProfile, RepositorySummary, SystemMap; print('ok')"

# 锁文件是否与当前环境完全一致（无输出即一致）
diff <(.venv/bin/python -m pip freeze) requirements.lock

# 版本控制状态
git status --short
git log --oneline

# 推送到 GitHub（远程已配好 origin）
git push
```

静态检查：由 Pylance 提供（编辑器解释器已指向 `.venv/bin/python`），当前 `schemas/` 下三个文件均无错误。尚未安装 ruff / flake8。

版本控制：仓库已初始化（`main` 分支，见 D007）；忽略规则命中 `.venv/`、`__pycache__/`、`*.pyc`、`.DS_Store`。

### 5.5 环境注意事项

- **必须使用 `.venv/bin/python`**；不要向系统 Python 3.9（`/usr/bin/python3`）安装任何依赖。
- `.venv` 由 Homebrew 的 `python3.12` 创建；不要使用 Conda base 环境，避免 base 环境污染。
- pip 走清华镜像源（用户级配置 `pypi.tuna.tsinghua.edu.cn`），换机器可能拉取到不同时间点的版本。
- 编辑器 / Pylance 解释器已指向 `.venv/bin/python`，无需手动切换。
- `StartupInfo` 中的 `backend` / `frontend` 只是配置文本，**任何阶段都不得执行**。
- T003 的验证使用一次性脚本，**未在仓库留下验证文件**。
- 推送前先看 `git status --short`：仓库是 **PRIVATE**，但一旦改为公开，提交中内置的作者姓名与邮箱会对所有人可见。敏感信息（密码、Token、Cookie、数据库口令）一律不入库。

禁止在本文件中记录密码、Token、Cookie、私钥、数据库口令或其他敏感信息。

---

## 6. 关键设计决定

### D001：使用项目内 `.venv`（Python 3.12），不使用系统 Python 3.9

状态：accepted

日期：2026-09-14

关联任务：T002、T003

**背景**

T002 检查发现编辑器默认指向 `/usr/bin/python3`，实为 Apple CommandLineTools 自带的 Python 3.9.6，且不在虚拟环境中；该项目解释器上没有任何 Web / 校验类依赖（`pydantic`、`yaml`、`pytest` 全部缺失）。

**决定**

用 Homebrew 的 `python3.12` 在项目根目录创建 `.venv`，所有依赖只装进这个环境。

**原因**

系统 Python 属于操作系统组件：向其安装包可能需要 `sudo`，且可能影响系统工具；Python 3.9 已停止维护；项目内虚拟环境可随时删除重建，不污染机器。

**影响**

- 正面：依赖相互隔离、可复现、可干净重建。
- 代价：每条命令都要显式写成 `.venv/bin/python ...`。
- 后续约束：`.venv/` 必须留在 `.gitignore` 中；文档与脚本不得依赖系统 `python3`。

**考虑过的替代方案**

- 直接装到系统 Python 3.9：会污染系统环境，且 3.9 已 EOL，未选择。
- 使用 Conda 环境：路径与 base 环境耦合，容易误用，未选择。

**替代关系**

无。

---

### D002：采用 Pydantic v2 而非 v1

状态：accepted

日期：2026-09-14

关联任务：T003

**背景**

项目需要为选填表、系统地图、测试规格等提供统一的数据校验，并需要导出 JSON 供后续报告使用。

**决定**

`requirements.txt` 中声明 `pydantic>=2,<3`，全部模型使用 v2 写法。

**原因**

v2 是当前主流版本，性能更好，`model_dump()` / `model_dump_json()` / `model_json_schema()` 语义统一，适合后续直接生成报告与接口文档。

**影响**

- 正面：写法统一，后续 5 个 schema 模块可复用同一套模式。
- 代价：若后续需要兼容引用 v1 的第三方库，需额外适配。
- 后续约束：所有模型必须使用 `model_config = ConfigDict(...)` 搭配 `@field_validator`；**禁止**使用 v1 的 `@validator` 或旧式 `class Config`。

**考虑过的替代方案**

- Pydantic v1：新项目无理由选择旧版本，未选择。
- dataclass + 手写校验：无内置 JSON Schema 导出，校验代码重复，未选择。

**替代关系**

无。

---

### D003：所有模型统一开启 `extra="forbid"` 与 `str_strip_whitespace=True`

状态：accepted

日期：2026-09-14

关联任务：T003

**背景**

选填表由人工手写，字段名容易拼错（例如把 `repository_path` 写成 `repository_pth`），YAML 中也常出现多余空格。若采用默认的 `extra="ignore"`，拼错字段会被**静默丢弃**。

**决定**

`BusinessRule`、`StartupInfo`、`ProjectProfile` 三个模型都开启这两个配置。

**原因**

本项目要在“预期 vs 实际”之间找差异并判定 Bug，任何静默丢失信息的行为都会直接损害结论的可信度，因此宁可让配置在第一时间报错。

**影响**

- 正面：配置拼写错误立即暴露；字符串首尾空格自动清除，避免“看起来相等实际不等”的假 Bug。
- 代价：对接会传入未知字段的外部系统时，需要单独放宽该模型。
- 后续约束：新增 profile 类模型应默认沿用这两个配置，除非有明确理由并在本日志记录。

**考虑过的替代方案**

- 保留默认 `ignore`：拼错字段被悄悄忽略，对判定 Bug 的系统风险过高，未选择。
- 用 `extra="allow"`：会把未知字段带进模型，破坏数据结构稳定性，未选择。

**替代关系**

无。

---

### D004：`StartupInfo` 中的启动命令只保存、不执行

状态：accepted

日期：2026-09-14

关联任务：T003

**背景**

总体设计文档要求“AI 不直接拥有任意代码执行权限”。启动命令来自人工填写的 YAML，本质是不可信输入。

**决定**

`backend` / `frontend` 仅作为配置文本存储，数据模型层在任何情况下都不执行它们。

**原因**

这是安全边界：一旦允许 schema 层执行配置中的字符串，等于把任意 shell 命令的执行权交给了一份配置文件。

**影响**

- 正面：模型层无副作用，可安全地反复构造与序列化。
- 代价：未来要真正启动被测环境时，必须另建受控通道。
- 后续约束：将来执行启动命令必须经由独立的白名单/沙箱模块（设计文档中的 `executors/sandbox.py`），不得在 schema 层实现。

**考虑过的替代方案**

- 在模型校验时顺便做一次“命令是否可执行”的探测：会引入副作用与安全风险，未选择。

**替代关系**

无。

---

### D005：`repository_path` 只校验格式，不校验路径是否真实存在

状态：accepted

日期：2026-09-14

关联任务：T003

**背景**

“路径为空 / 只有空格”属于数据格式问题；“路径不存在”属于运行环境问题。两者混在一起会让模型创建失败的原因难以区分。

**决定**

模型层只拒绝空字符串与纯空格字符串，**不检查**路径是否存在（本轮明确要求）。

**原因**

设计文档规定：环境不可访问、依赖安装失败等情况应让任务进入 `BLOCKED` 并报告环境问题，而不是被误报为产品 Bug。把环境探测留在模型层会破坏这一区分。

**影响**

- 正面：模型可离线、可测试、无文件系统依赖。
- 代价：调用方必须自行确认路径存在性。
- 后续约束：T008 仓库扫描器必须把“仓库路径不存在”映射为环境问题（`BLOCKED`）而非数据错误，并为此补充验证。

**考虑过的替代方案**

- 在模型里用 `Path.exists()` 校验：让数据模型承担环境探测职责，且难以在无该路径的机器上测试，未选择。

**替代关系**

无。

---

### D006：用 `Finding` 统一承载「结论值 + 来源 + 定位 + 置信度」

状态：accepted

日期：2026-09-14

关联任务：T004

**背景**

R004 指出：`declared`（表格声明）/ `observed`（代码事实）/ `inferred`（推断）三类来源尚未落到任何模型，而 Week 1 验收标准要求“每一条结论带来源文件与行号或代码片段定位”且“不确认的内容不会伪装成确定事实”。T004 必须把这个要求固化到数据结构里。

**决定**

1. 新增 `SourceType` 枚举（`observed` / `declared` / `inferred`）与 `Finding` 模型；
2. 语言、框架、依赖、前端入口文件、后端入口文件**全部复用 `Finding`**，不为每一类结论各建一个类，也不建立多级继承；
3. `confidence` 为必填 `float`，范围 0～1（`ge=0.0, le=1.0`）；
4. 每条结论必须给出定位：`line` 与 `snippet` 至少填写一个；行号从 1 开始；
5. `source_type = inferred` 时 `confidence` 必须严格小于 1.0；
6. `RepositorySummary.repository_path` 只记录、不检查存在性（沿用 D005）。

**原因**

后续要回答“这算不算 Bug”，必须先能分清“代码里看到的事实”与“模型猜的结论”。把来源与置信度做成必填字段，扫描器就没有“偷懒不写证据”的选项，Week 1 的验收标准才能被机器自动检查。

**影响**

- 正面：语言、框架、依赖、入口文件四类结论结构完全一致，T008 只需学会一个 `Finding` 的构造方式；`Finding` 也可直接被 T005 的 `SystemMap` 复用。
- 代价：写入方必须提供来源文件与定位，不能只输出一个裸字符串。
- 后续约束：新增“扫描结论”类模型一律基于 `Finding`，不要另起一套无证据的字段。

**考虑过的替代方案**

- 为语言/框架/依赖/入口文件各建一个模型：字段与校验重复，或被迫引入多级继承，未选择。
- 结论用裸字符串（`languages: list[str]`）：无法携带来源与置信度，直接违反验收标准，未选择。
- 给 `confidence` 一个默认值（如 1.0）：会让“忘了写置信度”等价于“100% 确定”，与 D003 的快速失败思路相反，未选择。

**替代关系**

无。

---

### D007：把项目纳入 Git 版本控制（`main` 分支）

状态：accepted

日期：2026-09-14

关联任务：T002-A（原 Q002）

**背景**

T002 确认目录不是 Git 仓库，因此 `.gitignore` 与两个 `.gitkeep` 一直不产生实际作用，也没有任何变更历史可供回溯。

**决定**

在项目根目录执行 `git init -b main`，以 `main` 为主分支；`.venv/`、`__pycache__/`、`*.pyc`、`.DS_Store` 继续忽略。

**原因**

成本极低（不需要服务器或网络），却能立即获得变更历史、可回滚能力，并让已有的 `.gitignore` 真正生效。

**影响**

- 正面：可以查看改动、对比版本、撤销误操作；忽略规则开始实际生效。
- 代价：提交前需要确认没有把 `.venv/`、缓存文件或敏感信息暂存进去。
- 后续约束：提交身份沿用用户级配置（Sid Zhang）；`.venv/` 永不入库。

**考虑过的替代方案**

- 暂不纳入：随着 `artifacts/` 产物增多，误删与回溯风险上升，未选择。
- 使用云端仓库：当前单人本地开发不需要，未选择。

**替代关系**

关闭 Q002（用户 2026-09-14 确认“建议现在做”）。

**遗留事项**

`.gitignore` 目前**未忽略** `artifacts/`，运行期产物会被纳入版本控制。是否要忽略已另开 Q004 跟踪。

---

### D008：用 `requirements.lock` 锁定精确依赖版本

状态：accepted

日期：2026-09-14

关联任务：T002-A（原 Q003）

**背景**

`requirements.txt` 只声明 `pydantic>=2,<3`，实际安装 2.13.5。不同时间、不同机器安装可能得到不同版本，而 T003 / T004 的验证结论是绑定在具体版本上的（R001）。

**决定**

保留 `requirements.txt` 的范围声明，另建 `requirements.lock`（`.venv/bin/python -m pip freeze` 产物，共 5 个包）。复现验证环境时用锁文件安装；升级依赖后必须重新生成锁文件。

**原因**

既保留升级弹性（`requirements.txt`），又能精确复现验证过的环境（`requirements.lock`）；锁文件是 pip 原生格式，可直接 `-r` 安装，不需要引入额外工具。

**影响**

- 正面：验证结论可绑定到确定版本，换机器能装出同一套依赖。
- 代价：多维护一个文件；依赖升级后需手动刷新，忘记刷新会导致锁文件与实际环境不一致。
- 后续约束：任何依赖变更都必须同步刷新 `requirements.lock`，并在日志中记录。

**考虑过的替代方案**

- 直接钉死 `requirements.txt`（`pydantic==2.13.5`）：会失去范围声明，且间接依赖仍需单独管理，未选择。
- 不锁定：无法复现，未选择。

**替代关系**

关闭 Q003（用户 2026-09-14 确认“建议增加锁定文件”）。

---

### D009：`SystemMap` 用 ID 引用连接对象，并强制检查唯一性与悬空引用

状态：accepted

日期：2026-09-14

关联任务：T005（继承 D006）

**背景**

系统地图需要表达“页面 → API → 后端路由 → 数据模型”。假如每个对象内嵌被引用对象的整份内容，同一实体就会出现多份副本，改一处就会产生互相矛盾的数据；反之，如果只存 ID 却不检查，调用链就可能指向一个根本不存在的对象，报告里会出现“看起来已经确认、实际无源头”的链路。

**决定**

1. 五类对象（页面、请求、后端路由、数据模型、调用链）各有一个非空 `id`，对象之间**只用 ID 引用**，不整份复制；
2. `SystemMap` 在构造时统一检查：同类对象内 ID 不重复；调用链的 `page_id` / `api_id` / `backend_route_id` / `data_model_ids` 以及后端路由的 `related_data_model_ids`，被引用对象必须真实存在；
3. 调用链状态与引用完整度必须自洽：`complete` 必须齐“页面 + 请求 + 后端路由”三段；`partial` / `unresolved` 至少引用一个已确认对象；
4. 证据与置信度**直接复用 T004 的 `Finding`**，`system_map.py` 不新建 Evidence / SourceType / Confidence；每个对象至少一条证据（`min_length=1`）；
5. HTTP 方法用 `HttpMethod` 枚举（GET / POST / PUT / PATCH / DELETE），写入时统一转大写；
6. 数据模型类型用 `DataModelKind` 枚举，并保留 `other` 兜底。

**原因**

报告要用来判定 Bug，任何“看起来成立的链路”都必须能追溯到真实代码。用 ID 引用 + 强制校验，能让不完整的知识要么被标为 `partial` / `unresolved`，要么直接报错，而不是默默地编造出一段关系。

**影响**

- 正面：同一实体只有一份数据；链路状态和引用完整度无法“装出来”；T009～T011 的分析器只需生成 ID 引用，不必拼装嵌套对象。
- 代价：分析器必须先建立稳定的 ID 命名约定（见 R007），构造数据比写裸字典繁琐。
- 后续约束：T009～T011 不得绕过 `SystemMap` 自行拼接引用；未确认的关系留空，不要编造 ID 来“凑完整”。

**考虑过的替代方案**

- 内嵌整份被引用对象：副本会漂移、改名后出现矛盾，未选择。
- 只存 ID 但不做引用检查：悬空引用会变成“假结论”，与本项目的核心目标直接冲突，未选择。
- 在 `system_map.py` 里再定义一套证据模型：与 D006 “统一复用 `Finding`”矛盾，未选择。

**替代关系**

落实 R004 的剩余部分（`RepositorySummary` 与 `SystemMap` 现在都要求证据）。

---

### D010：新建独立远程仓库，不覆盖已有的 `QA_ai_agent` 仓库

状态：accepted

日期：2026-09-14

关联任务：T002-B

**背景**

准备推送时发现账号 `hongweiyuan319-cpu` 下已存在 `QA_ai_agent` 仓库，里面是 2026-08-05 的“自动化测试全流程插件原型（登录注册 Demo）”（68 个文件，含 `frontend/`、`qa_plugin/`、`bts/`、`docs/`），与本项目**无共同历史**。两者根目录都存在 `.gitignore`，合并会产生冲突；强推则永久丢失那份原型。

**决定**

新建**独立**私有仓库 `universal-ai-debug-agent`，将本项目推送至该仓库；原有 `QA_ai_agent` 仓库保持不动。

**原因**

两个项目用途不同（一个是自动化测试插件原型，一个是通用 Debug Agent 骨架），共用仓库会让目录结构混淆；任何不可逆的强推都不应作为默认选择。

**影响**

- 正面：两个项目各自独立演进，互不干扰；本项目的历史从初始提交开始，干净可读。
- 代价：GitHub 上多一个仓库；需要记得向哪个仓库推送。
- 后续约束：本项目的远程固定为 `origin` → `universal-ai-debug-agent`；若以后要把两个项目合并，必须单独评估并保留双方历史。

**考虑过的替代方案**

- 强推覆盖 `QA_ai_agent`：会永久删除那 68 个文件，未选择。
- 合并入 `QA_ai_agent`：两套项目共存一个仓库、需处理 `.gitignore` 冲突，未选择。
- 只保留本地：失去远程备份与协作能力，未选择。

**替代关系**

无（新增，不影响 Q002 / Q003 的结论）。

---

## 7. 已知限制、风险与阻塞

### 7.1 已知限制

| ID | 限制 | 影响 | 计划处理阶段 |
|---|---|---|---|
| L001 | 不能读取 `project-profile.yaml`，只能手工构造 `ProjectProfile` | 无法从配置文件驱动流程 | T006 |
| L002 | 未实现仓库扫描与代码分析（`RepositorySummary` / `SystemMap` 仅有数据契约，无任何代码填充） | 无法产出 `repository_summary.json` 与 `system_map.json` | T008～T011 |
| L003 | 没有正式测试套件（未安装 pytest） | 回归依赖一次性脚本，历史验证无法复现 | 见 Q001 |
| L004 | ~~项目未纳入 Git 版本控制~~ **已解决（T002-A、T002-B）** | 已有变更历史，并已推送到私有远程仓库 | 已完成 |
| L005 | 没有命令行入口 | 只能通过交互式 Python 调用 | T007 |
| L006 | ~~缺少 `SystemMap` 模型~~ **已解决（T005）** | 数据契约已就位 | 已完成 |
| L007 | ~~依赖未锁定精确版本~~ **已解决（T002-A）** | 已可用 `requirements.lock` 复现 5 个包的精确版本 | 已完成 |

### 7.2 风险

| ID | 风险 | 可能性 | 影响程度 | 应对方式 |
|---|---|---|---|---|
| R001 | `pydantic>=2,<3` 范围内的小版本升级改变校验行为（例如 URL 归一化、`extra` 报错结构） | 中 | 低 | **锁文件已建立（T002-A）**；升级依赖时重跑全部验证并刷新 `requirements.lock` |
| R002 | 依赖用户级 pip 镜像源配置，换机器或换 CI 时拉取结果不一致 | 低 | 低 | 已记录镜像源（5.5）；**锁文件进一步降低影响（T002-A）**；CI 中仍需显式指定 `--index-url` |
| R003 | 模型层不校验路径存在性，若调用方忘记检查，会把“路径写错”当成“仓库为空” | 中 | 中 | T008 必须显式映射为环境问题并补验证（见 D005） |
| R004 | ~~`declared`（表格声明）/ `observed`（代码事实）/ `inferred`（模型推断）三类来源尚未落到模型~~ **已解决（T004 + T005）** | 低 | 高 | `SourceType` + `Finding` 已把来源类型、来源文件、定位、置信度固化为必填（D006）；`SystemMap` 五类对象均要求至少一条证据（D009）。剩余风险转移到“分析器写错来源”，由 T009～T011 自行举证 |
| R005 | 缺乏回归测试，后续改动可能悄悄破坏已通过的校验（T003 的 10 项、T004 的 26 项、T005 的 49 项） | 高 | 中 | 见 Q001，尽快建立可重复执行的验证 |
| R006 | `Finding` 强制要求 `line` 或 `snippet`，若 T008 遇到确实无法定位的结论，可能被迫编造位置 | 中 | 中 | 允许用 `snippet` 承载原文；若 T008 反复受阻，再讨论放宽为“至少一项来源定位”并记录决定 |
| R007 | `SystemMap` 的 ID 引用体系需要稳定的命名约定；若 T009～T011 各自随手生成 ID，可能出现同义不同名、或把链路指向错误对象 | 中 | 中 | 在 T009 开工前先确定并记录 ID 命名约定（例如 `page-xxx` / `req-xxx` / `route-xxx` / `model-xxx` / `chain-xxx`），并由 T011 生成 `SystemMap` 时统一校验 |

### 7.3 当前阻塞

当前无阻塞项。

---

## 8. 下一步交接

### 8.1 下一任务

任务编号：T006

任务名称：创建 project-profile.yaml 模板

当前状态：planned

目标：在 `templates/` 下交付一份人工可填的 `project-profile.yaml` 模板，键名与 `ProjectProfile` 的校验规则一一对应，并附最小示例值（以登录注册 Demo 为例）。

**开工前必须先解决的范围冲突**：设计文档 2.2 的示例包含 `business_description`、`test_scope`、`test_accounts`、`reset`、`risk_focus`，而当前 `ProjectProfile` 只支持 `project_name`、`repository_path`、`startup`、`business_rules`，且开启了 `extra="forbid"` —— 模板写上述字段会被模型直接拒绝。两种处理方式：

- 方案 A（建议）：模板只包含模型当前支持的字段，保持 T006 单一职责；待 T012 真需要时再扩展 `ProjectProfile`；
- 方案 B：在 T006 内同步扩展 `ProjectProfile`，会改动 T003 已验证代码，必须重跑 T003 回归。

### 8.2 开始前必须阅读

- `logs/universal-ai-debug-agent-design.md`（2.2 固定格式选填表、2.3 表格设计原则）
- `logs/week-1-code-understanding-plan.md`（Day 1 第 6 项、Day 6 选填表要求）
- `schemas/project_profile.py`（模板键名必须与它一一对应）
- 决定 D002、D003、D004、D005

### 8.3 开始前必须检查

- 当前工作目录为 `/Users/hongweiyuan/Desktop/项目/QA_ai_agent`；
- `.venv/bin/python -V` 输出 `Python 3.12.13`；
- `.venv/bin/python -c "import pydantic; print(pydantic.VERSION)"` 输出 `2.13.5`；
- `schemas/project_profile.py` 的实际内容与本日志描述一致；
- 没有与本任务冲突的用户改动（当前 `schemas/` 下有 `__init__.py`、`project_profile.py`、`repository_summary.py`、`system_map.py`）；
- 工作区干净（`git status --short` 无输出），否则先确认变更来源。

**需要确认的一个问题**：当前依赖里**没有 `PyYAML`**。若要用 YAML 解析来验证模板，需要新增依赖；若不希望新增依赖，可在验证脚本里用纯文本方式提取键名后比对。建议默认后者，保持依赖最小。

### 8.4 预计修改

- 新建 `templates/project-profile.yaml`
- 可选：删除 `templates/.gitkeep`（目录已有真实文件后不再需要；保留也无害），并在日志记录选择
- 不修改 `schemas/` 下任何文件（除非采纳 8.1 的方案 B，并重跑 T003 回归）

### 8.5 实现要求

- 模板键名与 `ProjectProfile` 字段逐一同名：`project_name`、`repository_path`、`startup`（`backend` / `frontend` / `base_url`）、`business_rules`（`id` / `rule`）；
- 不写入模型未支持的键，否则 `extra="forbid"` 会直接报错；
- 示例值必须与登录注册 Demo 相关，`business_rules` 使用 `R-REG-xxx` 风格，便于 T012 与代码事实对照；
- `startup` 中的命令只作为文本示例；不得在注释或文档中引导执行未经确认的命令（见 D004）；
- 不写入密码、Token、Cookie 等敏感值；
- 模板要说明「除 `project_name`、`repository_path` 外均可留空」这一事实。

### 8.6 验收标准

- `templates/project-profile.yaml` 存在，键名可人工逐项对照 `ProjectProfile`；
- 模板中出现的键集合与 `ProjectProfile` 支持的键集合**完全一致**（不多、不少）；验证脚本用纯文本方式提取键名后与模型字段比对；
- 用模板中的示例值手工构造 `ProjectProfile` 能通过校验（当前阶段直接构造模型，不解析 YAML）；
- 原有 `schemas/` 代码无改动、无 Pylance 报错（若采纳方案 B，需重跑 T003 的 10 项回归）；
- 提交后 `git status --short` 干净。

### 8.7 本任务不要做

- 不实现 YAML 读取、仓库扫描、Flask / React 分析、调用链匹配、项目启动；
- 不建立 `run_discovery.py`（属于 T007）；
- 不安装 `pytest`、`PyYAML` 或其他新依赖；不建立 `tests/` 目录；
- 只允许新增 `templates/project-profile.yaml`（可含删除 `templates/.gitkeep`），不修改 `core/`、`artifacts/` 与 `schemas/`。

### 8.8 建议验证命令

```bash
cd "/Users/hongweiyuan/Desktop/项目/QA_ai_agent"

# 1) 环境正确
.venv/bin/python -c "import sys, pydantic; print(sys.version.split()[0], pydantic.VERSION)"

# 2) 回归：三个 schema 模块仍可导入
.venv/bin/python -c "from schemas import ProjectProfile, RepositorySummary, SystemMap; print('ok')"

# 3) 模板验证（一次性 heredoc；不落盘、不新增依赖）：
#    用文本方式提取 YAML 键名，与 ProjectProfile.model_fields 比对
```

---

## 9. 待确认问题

### Q001：是否引入 pytest、建立正式测试套件？

状态：open

关联任务：T003、T004

**为什么现在需要决定**

T003 的 10 项验证是用一次性 heredoc 执行的，脚本没有落盘，因此**无法重复执行**——代码一改，之前的验证证据就失效了（见 R005）。从 T004 起模型数量增加，回归成本会持续上升。

**方案 A**：引入 `pytest` 与 `tests/` 目录（依赖放 `requirements-dev.txt`）。
影响：验证可重复、可回归，未来可接 CI；代价是多一个依赖和一层目录。

**方案 B**：继续使用一次性脚本。
影响：保持依赖最小；代价是每次验证都要重写，历史验证无法复现，Day 7“连续执行 3 次输出一致”的验收将难以自动化。

**建议**

方案 A，但建议推迟到 Day 1 的模型全部定型后（即 T006 完成之后）一次性建立，避免中途反复修改测试。

**暂不决定的影响**

不阻塞 T004，但 Day 1 结束前必须决定，否则 T008 引入真实解析逻辑后将失去安全网。

**进展**

- T004（2026-09-14）：用户明确要求“不安装 pytest、不建 `tests/`”，因此本轮仍用一次性 heredoc 脚本验证（26 项全通过）；脚本未落盘，同样不可重复执行。T003、T004 两次验证的脚本都已在会话中丢失，R005 的敞口在 T005 后会继续放大。

**最终答复**：未答复

---

### Q002：是否现在把项目纳入 Git 版本控制？

状态：closed（2026-09-14 采纳方案 A，已由 T002-A 执行）

关联任务：T001、T002、T003

**为什么现在需要决定**

T002 已确认当前目录**不是** Git 仓库。因此 `.gitignore` 和两个 `.gitkeep` 目前不产生任何实际作用，也没有任何变更历史可回滚。

**方案 A**：现在 `git init` 并提交一次初始版本。
影响：立刻获得变更历史、可用 `.gitignore` 生效；代价可忽略。

**方案 B**：暂不纳入。
影响：保持最小；代价是随着 `artifacts/` 产出的文件增多，误删与回溯风险上升。

**建议**

方案 A。成本极低，且能立即让 T003 已建立的 `.gitignore` 生效。

**暂不决定的影响**

不阻塞任何任务，但 `.gitkeep` / `.gitignore` 的价值会持续处于“悬空”状态，本日志需继续记录这一偏差。

**最终答复**：方案 A。用户于 2026-09-14 确认“建议现在做”，已由 T002-A 执行（`git init -b main`，13 个文件入库，`.venv/` 与缓存文件未入库）。

---

### Q003：`requirements.txt` 是否锁定精确版本？

状态：closed（2026-09-14 采纳方案 A，已由 T002-A 执行）

关联任务：T002、T003

**为什么现在需要决定**

当前声明为 `pydantic>=2,<3`，实际安装到 2.13.5。不同时间、不同机器安装可能得到不同版本，与 Week 1 的“连续执行 3 次，确认输出一致”验收目标存在潜在冲突（见 R001）。

**方案 A**：保留范围声明，另建 `requirements.lock`（`pip freeze` 产物）。
影响：开发期灵活、复现时稳定；代价是多维护一个文件，需要定期刷新。

**方案 B**：直接钉死为 `pydantic==2.13.5`。
影响：最简单直接；代价是升级需手工修改。

**建议**

方案 A。既保留升级弹性，又能保证验证结果可复现。

**暂不决定的影响**

不阻塞，但 T003 记录的“10/10 通过”严格来说绑定在 Pydantic 2.13.5 上，换版本后需重新验证。

**最终答复**：方案 A。用户于 2026-09-14 确认“建议增加锁定文件”，已由 T002-A 执行（新增 `requirements.lock`，5 个包，与 `pip freeze` 完全一致）。

---

### Q004：`artifacts/` 下的运行期产物是否纳入版本控制？

状态：open

关联任务：T002-A（由 D007 引出）

**为什么需要决定**

当前 `.gitignore` 未忽略 `artifacts/`。T007 建立命令入口后，每次运行都会生成 `artifacts/task_<id>/`（包含 JSON、报告、后续还有截图），这些产物会被 Git 全部跟踪，导致提交历史被大量生成物污染。

**方案 A**：忽略 `artifacts/`（保留 `.gitkeep`），产物不入库。
影响：历史干净；代价是测试结果无法通过 Git 回溯。

**方案 B**：全部入库。
影响：产物可回溯；代价是仓库体积与噪声持续增长。

**建议**

方案 A，并在需要留存时把关键产物（如报告）手工整理到 `docs/` 或 `examples/` 下。

**暂不决定的影响**

不阻塞 T005；T007 生成首个产物前决定即可。

**最终答复**：未答复

---

## 10. 历史任务记录

### T002-B：配置 GitHub 远程仓库并首次推送

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14 05:23 UTC（日志记录时刻）

执行者：GitHub Copilot（用户完成浏览器授权）

关联决定：D007、D010

**目标**

把本地项目推送到 GitHub。推送前需要先确认账号下已有的 `QA_ai_agent` 仓库与本项目的关系，避免误覆盖。

**实际修改**

| 位置 | 动作 | 修改内容 |
|---|---|---|
| 本地 Git 配置 | 新增 | `origin` → `git@github.com:hongweiyuan319-cpu/universal-ai-debug-agent.git` |
| `main` 分支 | 新增 | 首次推送，`origin/main` = `ea3d6d3`，并设置上游跟踪 |
| GitHub | 新增 | 创建 **PRIVATE** 仓库 `hongweiyuan319-cpu/universal-ai-debug-agent` |
| 本机工具 | 新增 | 安装 `gh` 2.100.0（Homebrew），并登录为 `hongweiyuan319-cpu` |
| `logs/logs/TASK_LOG_1.md` | 修改 | 本轮日志更新 |

未改动：`schemas/`、`core/`、`templates/`、`artifacts/`、依赖文件；原有 `QA_ai_agent` 仓库**未做任何修改**。

**实现结果**

- 推送前只读检查发现：`QA_ai_agent` 已存在，内含 2026-08-05 的另一套原型（68 个文件），与本项目无共同祖先；两种目录都有 `.gitignore`。
- 用户选择方案 A（新建独立仓库），仓库名 `universal-ai-debug-agent`，本审查决定记为 D010。
- 推送结果：`origin/main` 与本地 `HEAD` 同为 `ea3d6d3`；本地与远程均为 14 个文件，内容一一对应。
- `.venv/`、`__pycache__/`、`.DS_Store` 均未入库。

与原计划存在的差异：本轮不在第 1 周任务清单内，属于用户临时要求的环境任务，已记为 `T002-B`。

**验证证据**

| 验证项 | 命令 | 结果 |
|---|---|---|
| SSH 认证 | `ssh -T git@github.com`（BatchMode） | PASS（`Hi hongweiyuan319-cpu!`） |
| 已有仓库排查 | `git ls-remote <repo>` × 4 个候选名 | PASS（发现 `QA_ai_agent` 已存在且有 1 个提交、68 个文件） |
| 仓库创建 | `gh repo create universal-ai-debug-agent --private` | PASS |
| 首次推送 | `git push -u origin main` | PASS（`[new branch] main -> main`，33 个对象，51.28 KiB） |
| 远程可见性 | `gh repo view --json visibility` | PASS（`PRIVATE`，默认分支 `main`） |
| 内容一致性 | `git ls-tree -r origin/main` vs `git ls-files` | PASS（两边各 14 个文件） |
| 提交一致性 | `git rev-parse HEAD` vs `origin/main` | PASS（同为 `ea3d6d3`） |

关键输出摘要：

```text
✓ Created repository hongweiyuan319-cpu/universal-ai-debug-agent on github.com
 * [new branch]      main -> main
## main...origin/main
本地 14 个 / 远程 14 个
一致：ea3d6d3
```

**遇到的问题与处理**

问题：账号下已存在同名意图的仓库 `QA_ai_agent`，且内容完全不相关。
原因：该仓库是 8 月 5 日的旧原型，并非本项目早期版本。
处理：没有推送到它、没有强推、没有合并；而是向用户说明情况并请求选择，最终新建独立仓库（D010）。

问题：环境里没有 `gh`，无法在命令行创建仓库。
原因：之前未安装。
处理：用 Homebrew 安装 `gh` 2.100.0，用户完成一次浏览器设备码授权（验证码 `401D-D49A`，仅一次性使用）。授权时 gh 询问是否上传 SSH 公钥，选择 **Skip**，因为 `~/.ssh/id_ed25519` 已在账号上注册且能正常认证。

**未完成或未覆盖**

- 未配置 GitHub Actions / CI（属于后期事项，与 Q003 的锁文件配合更好）；
- 未添加 `README.md`（计划在 T013 / Day 7 编写）；
- `artifacts/` 产物是否入库仍未决定（Q004）。

**给下一任务的影响**

- 从 T006 起，任务结束时除了提交还应 `git push`；
- 推送前用 `git status --short` 确认未暂存 `.venv/`、缓存或敏感信息；
- T006 的远程仓库地址固定为 `origin`（`universal-ai-debug-agent`），不要推到 `QA_ai_agent`。

---

### T005：定义 SystemMap 数据模型

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14 05:02 UTC（日志记录时刻）

执行者：GitHub Copilot

关联决定：D002、D003、D006、D009

**目标**

定义 `system_map.json` 对应的 Pydantic v2 数据模型：页面、API 请求、后端路由、数据模型、调用链，并通过 ID 引用把它们连起来，同时强制检查重复 ID 与悬空引用。本轮不扫描任何真实仓库，不实现 React / Flask 分析逻辑。

**实际修改**

| 文件 | 动作 | 修改内容 |
|---|---|---|
| `schemas/system_map.py` | 新增 | `HttpMethod`、`CallChainStatus`、`DataModelKind` 三个枚举；`FrontendPage`、`FrontendRequest`、`BackendRoute`、`DataModel`、`CallChain`、`SystemMap` 六个模型 |
| `schemas/__init__.py` | 修改 | 追加导入与 `__all__`（15 个公开名字）；docstring 补充“对象间只用 ID 互相引用”的约定 |
| `logs/logs/TASK_LOG_1.md` | 修改 | 本轮日志更新 |

未改动：`core/`、`templates/`、`artifacts/`、`requirements.txt`、`requirements.lock`、`schemas/project_profile.py`、`schemas/repository_summary.py`（**未修改 T004 的任何代码**，`Finding` 原样复用）。

**实现结果**

- 五类对象（全部 `extra="forbid"` + `str_strip_whitespace=True`）：
  - `FrontendPage`：`id` / `name` / `path` / `component_file`（可选）/ `form_fields` / `evidence`；
  - `FrontendRequest`：`id` / `method` / `path` / `file_path` / `request_fields` / `evidence`（只表示“前端准备发什么”，不代表后端存在该路由）；
  - `BackendRoute`：`id` / `method` / `path` / `handler_function` / `file_path` / `input_fields` / `output_fields` / `status_codes` / `related_data_model_ids` / `evidence`；
  - `DataModel`：`id` / `name` / `kind` / `file_path` / `fields` / `evidence`；
  - `CallChain`：`id` / `status` / `page_id` / `api_id` / `backend_route_id` / `data_model_ids` / `evidence`。
- 证据复用 T004 的 `Finding`（**没有新建 Evidence / SourceType / Confidence**），每个对象 `evidence` 至少一条（`min_length=1`）。
- 引用完整性：`SystemMap` 构造时检查同类对象 ID 不重复，并检查 `CallChain` 的 `page_id` / `api_id` / `backend_route_id` / `data_model_ids` 与 `BackendRoute.related_data_model_ids` 是否指向真实存在的对象。
- 状态自洽：`complete` 必须齐“页面 + 请求 + 后端路由”；`partial` / `unresolved` 至少引用一个已确认对象（未确认的环节留空，不编造 ID）。
- HTTP 方法统一转大写；`status_codes` 限制在 100～599；`DataModelKind` 保留 `other` 兜底。
- 列表字段全部 `default_factory=list`，代码中无 `default=[]`；已用“两个实例互不影响”验证无共享状态问题。

与原计划存在的差异：无。用户要求的 18 项验证全部覆盖并额外增加了边界用例，未做范围外扩展。

**新增设计决定**

D009：`SystemMap` 用 ID 引用连接对象，并强制检查唯一性与悬空引用；证据复用 T004 的 `Finding`。

**验证证据**

验证方式：`.venv/bin/python` 执行一次性 heredoc 脚本（未落盘，`tests/` 未建立）。

| 验证组 | 覆盖内容 | 结果 |
|---|---|---|
| 导入与回归 | 新增 9 个名字可从 `schemas` 导入；`ProjectProfile` / `RepositorySummary` 仍可导入与使用 | PASS |
| 完整地图 | 2 个页面 + 2 个请求 + 2 个后端路由 + 1 个 `User` 模型 + 2 条 `complete` 调用链 | PASS |
| 默认值 | 7 个可选列表省略时均为 `[]`；两个 `SystemMap` 实例不共享列表 | PASS |
| 字符串校验 | 8 项空字符串 / 纯空格用例（含可选 `component_file`、`page_id`）全部被拒 | PASS |
| 多余字段 | 页面、调用链、`SystemMap` 拼错字段名均触发 `extra_forbidden` | PASS |
| HTTP 方法 | `FETCH` / `GETS` / 数字被拒；`post` / `patch` / `delete` 自动转大写 | PASS |
| 证据规则 | `inferred` + 1.0 被拒、`inferred` + 0.6 通过；无行号且无片段被拒；空证据列表被拒 | PASS |
| 重复 ID | 页面、请求、路由、数据模型、调用链五类重复 ID 全部被拒 | PASS |
| 悬空引用 | 不存在的 `page_id` / `api_id` / `backend_route_id` / 数据模型 ID、以及路由关联不存在模型，全部被拒 | PASS |
| 链路状态 | `complete` 缺任一段被拒；`partial` / `unresolved` 可缺目标但至少引用一个；零引用被拒 | PASS |
| 其他约束 | 状态码 9999 被拒；数据模型 `kind` 非法被拒 | PASS |
| 序列化 | `model_dump()`、`model_dump_json()`、`model_json_schema()` 正常（含 5 个顶层字段） | PASS |

关键输出摘要：

```text
python  : 3.12.13
pydantic: 2.13.5
完整地图: pages=2 requests=2 routes=2 models=1 chains=2
通过 49 / 49
```

静态检查：Pylance 对 `schemas/` 下 4 个文件均无报错。

**遇到的问题与处理**

问题：无。一次执行全部通过（无失败重跑）。

**未完成或未覆盖**

- 没有任何代码去填充 `SystemMap`；`system_map.json` 目前只能手工构造（L002）；
- 未在真实 React + Flask 仓库上验证模型的表达力（例如一个后端路由对应多个前端请求、同一页面多个入口文件），留给 T009～T011；
- ID 命名约定尚未确定（R007），待 T009 开工前明确；
- 仍未建立可重复执行的回归测试（Q001，R005）。

**给下一任务的影响**

- T006 只创建 YAML 模板，不涉及 `schemas/`；但开工前必须先解决设计文档字段与 `ProjectProfile` 支持范围不一致的问题（见 8.1）；
- T006 的验收若要真正解析 YAML，会需要 `PyYAML`；建议先用纯文本比对键名，保持“不新增依赖”的约定；
- 从 T009 起，分析器必须遵守 D009：只用 ID 引用、未确认就留空、每个对象带至少一条证据。

---

### T002-A：Git 版本控制与依赖锁定（Q002 / Q003 落实）

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14 03:59 UTC（日志记录时刻）

执行者：GitHub Copilot

关联决定：D007、D008（关闭 Q002、Q003）

**目标**

按用户 2026-09-14 的答复，落实两项环境收尾工作：把项目纳入 Git 版本控制；新增依赖锁定文件，使当前验证过的依赖版本可被精确复现。本轮不涉及任何业务代码。

**实际修改**

| 文件 | 动作 | 修改内容 |
|---|---|---|
| `.git/` | 新增 | `git init -b main`，仓库初始化，主分支 `main` |
| `requirements.lock` | 新增 | `pip freeze` 产物，锁定 5 个包（annotated-types 0.8.0、pydantic 2.13.5、pydantic_core 2.46.5、typing-inspection 0.4.4、typing_extensions 4.16.0） |
| `requirements.txt` | 修改 | 仅补注释：说明 `requirements.lock` 的用途与安装方式；`pydantic>=2,<3` 声明未变 |
| `logs/logs/TASK_LOG_1.md` | 修改 | 本轮日志更新 |

未改动：`core/`、`schemas/`、`templates/`、`artifacts/`、`.gitignore`。

**实现结果**

- 仓库已初始化（`main` 分支），初始提交 `118ab14` 共 13 个文件（含本记录）；`.venv/`、`__pycache__/`、`*.pyc`、`.DS_Store` 均未入库，忽略规则经 `git check-ignore -v` 逐条确认命中。
- 提交身份沿用用户级 Git 配置，未新增仓库级配置（具体身份信息不写入本日志，避免公开仓库暴露个人邮箱）。
- 依赖锁定：`requirements.lock` 与 `.venv/bin/python -m pip freeze` 输出 byte 级一致；可用 `pip install -r requirements.lock` 复现同一环境。
- `requirements.txt` 与 `requirements.lock` 分工：前者保留升级弹性，后者用于复现验证环境（D008）。

与原计划存在的差异：本轮不在第 1 周任务清单内，属于用户临时确认的环境收尾任务，已在任务总览中记为 `T002-A`。

**验证证据**

| 验证项 | 命令 | 结果 |
|---|---|---|
| Git 可用 | `git --version` | PASS（git 2.50.1，Apple Git-155） |
| 仓库初始化 | `git init -b main` | PASS（Initialized empty Git repository） |
| 忽略规则生效 | `git check-ignore -v .venv/bin/python schemas/__pycache__/… .DS_Store logs/.DS_Store` | PASS（4 条路径全部命中 `.gitignore` 对应规则） |
| 入库文件清单 | `git add -A && git status --short` | PASS（13 个文件，全部为 `A`；无 `.venv/`、无 `__pycache__`、无 `.DS_Store`） |
| 锁文件与当前环境一致 | `diff <(.venv/bin/python -m pip freeze) requirements.lock` | PASS（无输出，完全一致） |
| 锁文件可解析且已满足 | `.venv/bin/python -m pip install --no-index --dry-run -r requirements.lock` | PASS（5 个包全部 “Requirement already satisfied”，未联网） |
| 初始提交 | `git add -A && git commit -m …` | PASS（`118ab14`，`13 files changed, 2552 insertions(+)`） |
| 提交后状态 | `git status --short`；`git ls-files \| wc -l` | PASS（工作区无输出即干净；入库 13 个文件） |

关键输出摘要：

```text
git version 2.50.1 (Apple Git-155)
Initialized empty Git repository in /…/QA_ai_agent/.git/
.gitignore:1:.venv/     .venv/bin/python
.gitignore:2:__pycache__/       schemas/__pycache__/…
.gitignore:4:.DS_Store  .DS_Store
待提交文件总数：13
diff: 完全一致
```

**遇到的问题与处理**

问题：无。前置条件齐备（Git 已安装、用户级提交身份已配置、`.gitignore` 已覆盖需要排除的目录），一次执行成功。

**未完成或未覆盖**

- 未添加远程仓库（本地提交即可满足当前需求）；
- 未决定 `artifacts/` 产物是否入库（新增 Q004，T007 生成首个产物前需决定）；
- 未建立分支策略、提交信息规范等协作约定（单人开发暂不需要）。

**给下一任务的影响**

- 从 T005 起，每次任务结束应把代码与日志一并提交，提交前用 `git status --short` 确认未暂存 `.venv/` 或敏感信息；
- 依赖升级时必须重新生成 `requirements.lock` 并重跑验证；
- T005 不因本轮变更而改变实现范围。

---

### T004：定义 RepositorySummary 数据模型

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14 03:51 UTC（日志记录时刻）

执行者：GitHub Copilot

关联决定：D002、D003、D005、D006

**目标**

为 T008 的仓库扫描器定义稳定的数据契约：用 Pydantic v2 定义能承载“语言、框架、依赖、前后端入口文件”的模型，并让每一项扫描结论都携带来源类型、来源文件、定位与 0～1 置信度。本轮不实现任何扫描逻辑。

**实际修改**

| 文件 | 动作 | 修改内容 |
|---|---|---|
| `schemas/repository_summary.py` | 新增 | `SourceType` 枚举、`Finding`、`RepositorySummary` 三个模型（共 3 个公开模型） |
| `schemas/__init__.py` | 修改 | 追加导入与 `__all__`（`Finding`、`RepositorySummary`、`SourceType`）；docstring 的“约定”改为描述 `Finding` 的证据要求；`__version__` 保持不变 |
| `logs/logs/TASK_LOG_1.md` | 修改 | 本轮日志更新 |

未改动：`core/`、`templates/`、`artifacts/`、`requirements.txt`、`schemas/project_profile.py`。

**实现结果**

- `SourceType`：`str` 枚举，只有 `observed` / `declared` / `inferred` 三种取值。
- `Finding`：`value`（结论值）、`source_type`、`file_path`、`line`、`snippet`、`confidence`、`version`。
  - `value` / `file_path` 拒绝空字符串与纯空格；`version` / `snippet` 可以不填，但填了就不能是空白；
  - `confidence` 必填，`ge=0.0, le=1.0`；`line` 从 1 开始（`ge=1`）；
  - `model_validator` 强制两条诚实性约束：`line` 与 `snippet` 至少一个；`source_type=inferred` 时 `confidence` 必须 `< 1.0`。
- `RepositorySummary`：`repository_path` 必填（`mode="before"` 拒绝空白，不检查存在性）；`languages`、`frontend_frameworks`、`backend_frameworks`、`dependencies`、`frontend_entry_files`、`backend_entry_files` 六个列表全部 `default_factory=list`。
- 未引入继承体系：六类结论共用同一个 `Finding`，用 `version` 承载依赖/框架的版本号。
- 模型层无文件系统与进程副作用：整个模块只依赖 `enum`、`pathlib`、`pydantic`。

与原计划存在的差异：无。用户提出的每项要求均已实现，未做范围外扩展。

**新增设计决定**

D006：用 `Finding` 统一承载「结论值 + 来源 + 定位 + 置信度」，含“至少一个定位”“inferred 置信度 < 1.0”两条强制规则。

**验证证据**

验证方式：`.venv/bin/python` 执行一次性 heredoc 脚本（未落盘，`tests/` 未建立）。

| 验证项 | 结果 |
|---|---|
| 1. 新增模型可从 `schemas` 包导入 | PASS |
| 2. 完整合法数据可创建 `RepositorySummary` | PASS |
| 3. 省略可选列表时得到空列表（6 个列表均验证） | PASS |
| 4. 必填字符串为空 / 纯空格被拒绝（4a～4e） | PASS |
| 5. 未知字段与拼错字段名触发 `extra_forbidden`（`Finding` 与 `RepositorySummary` 各一） | PASS |
| 6. 来源类型只能是 observed / declared / inferred（含大小写与非法值） | PASS |
| 7. 置信度校验（1.5、-0.1 被拒；inferred + 1.0 被拒；inferred + 0.6 可用） | PASS |
| 8. `model_dump()` 正常 | PASS |
| 9. `model_dump_json()` 正常 | PASS |
| 10. 原有 `ProjectProfile` 导入、构造、JSON 导出与空白校验仍生效 | PASS |
| 11. 仓库路径不存在时仍可创建（无副作用） | PASS |
| 12. `model_json_schema()` 可导出 | PASS |

关键输出摘要：

```text
python  : 3.12.13
pydantic: 2.13.5
通过 26 / 26
```

**遇到的问题与处理**

问题：第一轮验证脚本出现 5 处 `NameError: name 'RepositorySummary' is not defined`。
原因：脚本把导入放在第一个检查函数内部，模块级作用域没有绑定这些名字，属于**验证脚本自身的缺陷**，与模型代码无关。
处理：把导入提到脚本顶部后重跑，26 项全部通过。

**未完成或未覆盖**

- 未编写任何扫描逻辑，`RepositorySummary` 目前只能手工构造（L006、L002）；
- 未验证 `Finding` 在真实仓库数据上的表达力（例如一个代码位置对应多个语言/框架结论时是否需要去重），留给 T008；
- 未建立可重复执行的测试（Q001，R005）。

**给下一任务的影响**

- T005 必须复用 `Finding` 与 `SourceType`，不要另建重复字段（D006）；
- T005 沿用 `model_validator` 处理跨字段规则时，须继续保持“只有一种 v2 写法”的风格；
- `schemas/__init__.py` 的导出列表需在每个新模型加入后同步维护。

---

### T003：实现 ProjectProfile 数据模型

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14 03:46 UTC（日志记录时刻）

执行者：GitHub Copilot

关联决定：D001、D002、D003、D004、D005

**目标**

在项目内建立隔离的 Python 3.12 + Pydantic v2 环境，并用 Pydantic v2 定义 `BusinessRule`、`StartupInfo`、`ProjectProfile` 三个数据模型，通过最小运行验证。本轮不实现任何后续功能。

**实际修改**

| 文件 | 动作 | 修改内容 |
|---|---|---|
| `.venv/` | 新增 | 由 `python3.12 -m venv` 创建，Python 3.12.13，已在 `.gitignore` 中忽略 |
| `requirements.txt` | 新增 | 声明 `pydantic>=2,<3`，附安装说明注释 |
| `.gitignore` | 新增 | `.venv/`、`__pycache__/`、`*.pyc`、`.DS_Store` |
| `schemas/project_profile.py` | 新增 | `BusinessRule`、`StartupInfo`、`ProjectProfile` 三个模型 |
| `schemas/__init__.py` | 修改 | 追加导入与 `__all__`；原 docstring 与 `__version__` 原样保留 |

未改动：`core/__init__.py`、`templates/.gitkeep`、`artifacts/.gitkeep`、`logs/` 下既有文档。

**实现结果**

- `BusinessRule`：`id`、`rule` 均为必填字符串，拒绝空字符串与纯空格，首尾空格自动清除。
- `StartupInfo`：`backend`、`frontend`、`base_url` 默认均为 `None`；`base_url` 使用 `AnyHttpUrl`，只接受 http/https；启动命令只保存不执行。
- `ProjectProfile`：`project_name`、`repository_path` 必填；`repository_path` 为 `Path` 类型且不检查存在性；`startup` 用 `default_factory=StartupInfo`；`business_rules` 用 `default_factory=list`；`extra="forbid"` 拒绝未定义字段。
- 环境：编辑器 / Pylance 解释器在创建 `.venv` 后自动切换到 `.venv/bin/python`，原先预判的“导入无法解析”问题未发生。

与原计划存在的差异：无。用户提出的每一项要求均已实现，未做范围外扩展。

**验证证据**

| 验证项 | 命令或方式 | 结果 |
|---|---|---|
| 1. 三个模型可导入 | `from schemas import BusinessRule, ProjectProfile, StartupInfo` | PASS |
| 2. 完整数据可创建 `ProjectProfile` | 一次性 heredoc 验证脚本 | PASS |
| 3. 省略可选字段得到默认 `StartupInfo` 与空规则列表 | 同上 | PASS |
| 4a. `project_name` 只有空格被拒绝 | 同上 | PASS |
| 4b. `BusinessRule` 空字符串 / 只有空格被拒绝 | 同上 | PASS |
| 4c. `repository_path` 只有空格被拒绝 | 同上 | PASS |
| 4d. 未定义字段被拒绝（`extra_forbidden`） | 同上 | PASS |
| 4e. `base_url` 必须为 http/https（`ftp://` 被拒） | 同上 | PASS |
| 5. 仓库路径不存在时仍允许创建 | 同上 | PASS |
| 6. `model_dump` / `model_dump_json` 正常 | 同上 | PASS |
| 依赖安装 | `.venv/bin/python -m pip install -r requirements.txt` | PASS |
| 静态检查 | Pylance（`schemas/project_profile.py`、`schemas/__init__.py`） | PASS（无错误） |

关键输出摘要：

```text
Python   : 3.12.13
Pydantic : 2.13.5
解释器   : /Users/hongweiyuan/Desktop/项目/QA_ai_agent/.venv/bin/python
是否 venv: True
...
通过 10 / 10
```

**遇到的问题与处理**

问题：`python3.12` 单文件网络受限，安装 Pydantic 时需要拉取依赖。
原因：无。
处理：直接使用用户级 pip 镜像源配置（清华镜像），5 个包全部安装成功。

问题：`pip show pydantic | head -n 3` 输出末尾出现 `ERROR: Pipe to stdout was broken`。
原因：`head` 提前关闭管道，属于正常现象，并非安装失败。
处理：无需处理；版本号已正确打印为 2.13.5，后续改用 `-c "import pydantic; print(pydantic.VERSION)"` 更稳妥。

**未完成或未覆盖**

- 未读取 YAML 文件；`ProjectProfile` 目前只能手工构造；
- 未实现 `RepositorySummary`、`SystemMap`、命令行入口；
- 未建立正式测试套件（未安装 pytest）；
- 未验证 `business_rules` 为空列表时在 `model_dump_json()` 中的输出形态（不阻塞）；
- 未验证 `base_url` 未填写时 `model_dump_json()` 的字段表现（不阻塞）。

**给下一任务的影响**

- T004 必须沿用 D002、D003 的写法与配置，确保 5 个 schema 模块风格一致；
- T004 起必须引入来源定位与置信度字段（见 R004），否则 Week 1 验收标准无法满足；
- 所有验证命令必须使用 `.venv/bin/python`；
- `schemas/__init__.py` 的导出列表需要在每个新模型加入后同步维护。

---

### T002：环境与现状检查（只读）

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14（会话内，精确时刻未记录）

执行者：GitHub Copilot

关联决定：D001、D002

**目标**

在不修改任何文件的前提下，确认目录结构、已有文件、Python 依赖状态，以及是否存在测试目录与测试框架，为 T003 的技术选型提供事实依据。

**实际修改**

| 文件 | 动作 | 修改内容 |
|---|---|---|
| 无 | 无 | 本轮为只读检查，未创建或修改任何文件 |

**实现结果**

检查结论：

- `schemas/` 目录与 `schemas/__init__.py` 均存在，但只有 docstring，无任何模型；
- 没有 `requirements.txt` / `pyproject.toml` / `setup.py`，即**未声明**任何依赖；
- `pydantic` **未安装**，因此“Pydantic v1 还是 v2”在检查时属于悬而未决，由后续轮次决定；
- 没有 `tests/` 目录，没有 `pytest.ini` / `tox.ini`，`pytest` 未安装；
- 编辑器解释器为 `/usr/bin/python3`（实为 3.9.6，CommandLineTools 自带），不在虚拟环境中；
- 机器上另有 Homebrew Python 3.12.13 与 Conda Python 3.13.13；
- 当前目录**不是** Git 仓库。

共发现 7 项需要先解决的问题（虚拟环境、Python 版本、Pydantic 版本、依赖声明、测试框架、Git、编辑器解释器），已在当轮报告中逐条列出并给出建议。

**验证证据**

| 验证项 | 命令或方式 | 结果 |
|---|---|---|
| 依赖是否可导入 | 在指定解释器中逐个 `importlib.import_module` | NOT RUN（预期失败，`pydantic` / `yaml` / `pytest` / `httpx` / `playwright` / `typer` / `rich` 全部 `ModuleNotFoundError`，属预期结果） |
| 解释器与虚拟环境状态 | `sys.version` / `sys.executable` / `sys.prefix != sys.base_prefix` | PASS（3.9.6、非虚拟环境，已确认） |
| 可用 Python 版本 | `python3 -V`（3 个解释器） | PASS |
| Git 仓库状态 | `git rev-parse --is-inside-work-tree` | PASS（确认不是 Git 仓库） |
| 文件清单 | `find . -type f` 排除 `.DS_Store` | PASS（当时共 6 个文件） |

关键输出摘要：

```text
python  : 3.9.6 (default, Apr 17 2026, 18:15:52)  [Clang 21.0.0]
venv?   : False
  pydantic     MISSING (ModuleNotFoundError)
  pytest       MISSING (ModuleNotFoundError)
fatal: not a git repository (or any of the parent directories): .git
```

**遇到的问题与处理**

问题：无。

原因：无。

处理：无。

**未完成或未覆盖**

- 未检查 Node.js / npm 是否可用（Day 4 分析 React 时才需要）；
- 未验证被测的登录注册 Demo 仓库是否可得（T008 才需要）。

**给下一任务的影响**

直接决定了 T003 的两项技术选型：必须新建项目内 `.venv`（D001）、采用 Pydantic v2（D002）；并引出 D003～D005 三条约束。

---

### T001：建立项目骨架与目录结构

状态：completed

开始时间：2026-09-14（会话内，精确时刻未记录）

完成时间：2026-09-14（会话内，精确时刻未记录）

执行者：GitHub Copilot

关联决定：无

**目标**

按第 1 周计划完成 Day 1 的第一步：建立 `core/`、`schemas/`、`templates/`、`artifacts/` 四个目录。

**实际修改**

| 文件 | 动作 | 修改内容 |
|---|---|---|
| `core/__init__.py` | 新增 | Python 包声明；docstring 中列出规划中的 5 个分析器子模块 |
| `schemas/__init__.py` | 新增 | Python 包声明；docstring 中列出规划中的 3 个数据模型子模块 |
| `templates/.gitkeep` | 新增 | 空目录占位，后续放 `project-profile.yaml` |
| `artifacts/.gitkeep` | 新增 | 空目录占位，运行期生成 `task_<id>/` |

**实现结果**

四个目录就位。`core/` 与 `schemas/` 建为 Python 包（含 `__init__.py`），后续新增模块可直接 `from core.xxx import ...`；`templates/` 与 `artifacts/` 为数据目录，用 `.gitkeep` 占位。

与原计划存在的差异：无。

**验证证据**

| 验证项 | 命令或方式 | 结果 |
|---|---|---|
| 目录结构就位 | 列出项目根目录 | PASS（`artifacts/`、`core/`、`schemas/`、`templates/`） |
| 文件内容正确 | 读取两个 `__init__.py` | PASS |

关键输出摘要：

```text
artifacts/
core/
schemas/
templates/
```

需要说明：`templates/.gitkeep` 与 `artifacts/.gitkeep` 在 T002 中确认项目不是 Git 仓库，因此这两个文件当前不产生实际作用（见 L004 与 Q002）。

**遇到的问题与处理**

问题：无。

原因：无。

处理：无。

**未完成或未覆盖**

- Day 1 剩余 4 项（`RepositorySummary`、`SystemMap`、`run_discovery.py`、`project-profile.yaml` 模板）留待 T004～T007。

**给下一任务的影响**

确立了“Python 包目录用 `__init__.py`、数据目录用 `.gitkeep` 占位”的约定。

---

## 11. 日志维护规则

每次任务开始时：

- 阅读本日志的第 1、2、6、8 节；
- 对照代码确认日志没有过期；
- 将当前任务状态改为 in_progress；
- 不得擅自扩大“当前范围”。

每次任务结束时：

- 更新 last_updated、当前任务和状态；
- 更新任务总览及代码状态；
- 记录实际修改过的文件；
- 记录真实执行的验证命令和结果；
- 有重要选择时新增设计决定；
- 更新限制、风险、阻塞和待确认问题；
- 写好下一步交接；
- 在历史记录顶部追加本次任务。

禁止事项：

- 不把聊天记录直接粘贴进日志；
- 不复制完整源代码；
- 不复制冗长终端输出；
- 不把“计划做”写成“已经完成”；
- 没有验证证据时，不将任务标记为 completed；
- 不删除仍有参考价值的旧决定；
- 不记录密码、Token、Cookie、私钥和其他敏感信息；
- 不使用“基本完成”“应该没问题”等无法验证的模糊表述。

---

## 12. 归档规则

- 当前快照始终保留在本文件顶部；
- 历史任务按最新在前排列；
- 当历史部分过长时，按里程碑移动到 `logs/task-log/<milestone>.md`；
- 本文件保留已归档日志的链接和最近一个里程碑的记录；
- 架构决定增多后，将第 6 节拆分到 `docs/decisions/`，本文件保留决定索引；
- 正式发布后，用 `CHANGELOG.md` 记录面向用户的重要版本变化，避免把任务流水直接当发布日志。
