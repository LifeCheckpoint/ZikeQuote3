<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# ZikeQuote3

_✨ 一个 LLM 介入的群聊语录插件 ✨_

</div>

## 📖 介绍

ZikeQuote3 基于 NoneBot 开发，便于群聊语录自动收集与管理，支持通过 LLM 自动收集群聊消息作为语录、手动管理语录、以及多种方式查看等功能。

## 🗒️ 功能

- **自动收集**: 监听群聊消息，当消息数量达到配置阈值时，自动触发 LLM 对消息历史进行筛选和提取，将符合条件的消收集为语录。
- **手动管理**: 支持通过命令手动添加、删除和评论语录。
- **语录排行**: 统计群组成员的语录数量，生成排行榜，并以图片形式展示。
- **随机语录**: 随机获取一条语录，支持按关键词过滤，并根据语录的展示次数进行权重调整，使不常出现的语录有更高概率被选中。
- **语录卡片**: 将单条语录生成卡片图片，方便分享。
- **语录列表**: 查看某个用户（默认为命令发送者）的语录列表，支持分页，并生成图片展示。
- **语录搜索**: 搜索包含指定关键词的语录，并生成图片展示。
- **LLM 集成**: 利用 LLM 对消息历史进行智能分析，自动提取 1~3 条高质量语录并生成评论。
- **HTML 渲染**: 使用 HTML 模板和外部渲染工具（Puppeteer）将语录信息渲染成图片输出。
- **权限控制**: 支持基于群组 ID 的白名单或黑名单权限控制。

## 🔧 安装

1. 确保您已经安装了 NoneBot2，然后安装插件本体
    <details open>
    <summary>手动安装</summary>
    下载该仓库后，进入命令行并使用

        poetry install
    
    以安装 `pyproject.toml` 依赖
    </details>

    <details open>
    <summary>使用 nb-cli 安装</summary>
    在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

        nb plugin install nonebot-plugin-ZikeQuote3

    </details>

    <details>
    <summary>使用包管理器安装</summary>
    在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

    <details>
    <summary>pip</summary>

        pip install nonebot-plugin-ZikeQuote3
    </details>
    <details>
    <summary>pdm</summary>

        pdm add nonebot-plugin-ZikeQuote3
    </details>
    <details>
    <summary>poetry</summary>

        poetry add nonebot-plugin-ZikeQuote3
    </details>
    <details>
    <summary>conda</summary>

        conda install nonebot-plugin-ZikeQuote3
    </details>

    打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    ```toml
    plugins = ["nonebot-plugin-ZikeQuote3"]
    ```

</details>

1. 确保系统安装 Node.js，安装截图相关后端及其依赖。
    ```bash
    cd your/bot/plugins/external/html_render/
    npm install
    ```
2. 在 `utils/api_key` 配置 OpenAI API Key，或自行修改 `utils/llm_solo.py` 使用自定义模型与参数
3. 在 `config.py` 进行插件相关配置，详见“⚙ 配置”

## ⚙ 配置

插件的配置项位于 `config.py` 文件中。您可以在 NoneBot2 项目的 `.env` 文件中覆盖这些配置。

### Config

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enable` | `bool` | `True` | 启用插件 |
| `enable_auto_collect` | `bool` | `True` | 启用自动收集与 LLM 整理 |
| `enable_advanced_search` | `bool` | `True` | 允许通过 LLM 高级查找（TODO） |
| `quote_managers` | `list[int]` | `[]` | 管理 QQ 号列表 |
| `pickup_interval` | `int` | `80` | 语录收集间隔（达到此消息数量触发自动收集） |
| `msg_max_length` | `int` | `35` | 允许被处理的最大消息长度 |
| `mapping_max_size` | `int` | `50` | 储存消息ID-语录ID映射的最大数量，用于回复消息映射 |
| `weight_p_transform` | `float` | `1.2` | 随机语录算法的权重幂变换参数，越小越平滑，越大越容易选到高权重语录 |
| `enable_duplicate` | `bool` | `False` | 是否允许个人语录重复收录 |
| `max_rank_show` | `int` | `40` | 排行榜允许显示的最大人数 |
| `quote_list_num_perpage` | `int` | `20` | 语录列表每页显示的数量 |
| `quote_list_page_limit` | `int` | `4` | 语录列表允许显示的最大页数，超出将不显示之前的页数 |
| `quote_list_show_comment` | `int` | `1` | 语录列表显示评论模式，0: 不显示，1: 显示最新评论（不包括自动生成），2: 显示最新评论（包括自动生成） |
| `hitokoto_url` | `str` | `"https://v1.hitokoto.cn/"` | 获取名人名言的 Hitokoto API 地址 |

### PermissionConfig

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `mode` | `str` | `"white"` | 权限模式，可选值: `"white"` (白名单) 或 `"black"` (黑名单) |
| `white_list` | `list[int]` | `[]` | 白名单，允许使用插件的群组 ID 列表 |
| `black_list` | `list[int]` | `[]` | 黑名单，禁止使用插件的群组 ID 列表 |

### PathConfig

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `root` | `Path` | `Path(__file__).parent` | 插件根目录 |
| `templates` | `Path` | `root / "templates"` | 模板目录 |
| `prompts` | `Path` | `root / "prompts"` | 提示词目录 |

## 🎉 使用

插件主要命令：

- `/语录rank [数字]`: 查看语录排行榜，可指定显示前几名。
- `(reply) /加语录`: 添加语录。
- `/删语录 语录ID 或 回复消息 /删语录`: 删除语录（需要管理员权限）。
- `(reply) /评语录 评价内容`: 评论语录。
- `/语录 [关键词]`: 随机获取一条语录，可按关键词搜索。
- `/语录卡 [关键词]`: 生成语录卡片图片，可按关键词搜索。
- `/语录列表 [用户]`: 查看某个用户的语录列表。
- `/查语录 关键词`: 搜索包含指定关键词的语录。


## 🚧 实现

- **数据存储**:
    - 语录数据和聊天历史记录均以 JSON 格式存储在本地文件系统中，每个群组对应一个独立的文件（位于插件数据目录下的 `history` 和 `quotes` 子目录）。

- **自动收集机制**:
    - 如果相关配置 `cfg.enable_auto_collect` 被启用，插件将捕获群聊消息，并将消息暂存。
    - 当暂存的消息数量达到配置的阈值 `cfg.pickup_interval`，触发自动收集流程 `interface/message_handle.py`。
    - 消息历史被发送给集成 LLM，LLM 根据预设的 Prompt `prompts/quote_pickup.txt` 对消息进行分析，提取潜在的语录并生成评论。
    - 提取出的语录和评论会被添加到语录库中。

- **语录处理**:
    - 语录的添加、删除和评论等操作通过 `interface/quote_handle.py` 中的函数实现，直接操作对应的 JSON 数据文件。
    - 随机语录的选取采用了基于展示次数的简单权重算法 `interface/quote_handle.py::calculate_weight`。

- **HTML 渲染**:
    - 插件利用外部的 HTML 渲染模块 `external/html_render/` 将语录排行榜、语录卡片和语录列表等信息渲染成图片。
    - 渲染过程通过 Python 调用 Node.js 脚本 `external/html_render/screenshot.py` 调用 `external/html_render/screenshot.js` 实现。
    - Node.js 脚本使用 Puppeteer 库来控制无头浏览器加载本地 HTML 模板文件 `templates/` 目录，并进行截图。

- **消息文本管理**:
    - 插件的消息回复文本通过 `external/msg_text/msg.py` 进行管理。
    - 支持带有概率的文本片段字典和固定文本混合。