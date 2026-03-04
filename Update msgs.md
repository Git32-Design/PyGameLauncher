# 更新节点

# v1.0.0 Alpha - Initial Release

## 初始化

### 核心功能

- **游戏市场**: 内置游戏市场,支持浏览可用游戏

- **游戏管理**:
  - 安装: 通过 Git 克隆 GitHub 仓库
  - 更新: 更新已安装的游戏到最新版本
  - 卸载: 删除本地游戏
  - 运行: 启动已安装的游戏

- **安全功能**:
  - 密码保护: 为游戏设置启动密码
  - 安全模式: 检测课堂管理软件,自动切换至安全模式

- **智能功能**:
  - 自动检测启动脚本(client.py, main.py, start.py 等)
  - 游戏版本管理(支持 Git 标签和提交哈希)
  - 不区分大小写的游戏 ID 匹配

### 环境要求

- Python 3.7 或更高版本
- Git (必须预装)

### 启动方式

1. **命令行模式**: `python PyGameLauncher.py <命令>`
2. **交互模式**: `python PyGameLauncher.py` (不带参数)

### 命令格式

所有命令必须使用 `pgl` 前缀(交互模式下可选):

| 命令 | 说明 | 示例 |
|------|------|------|
| `pgl help` | 显示帮助信息 | `pgl help` |
| `pgl install <游戏名>` | 安装游戏 | `pgl install pychat` |
| `pgl run <游戏名> [密码]` | 运行游戏 | `pgl run pychat` |
| `pgl update <游戏名>` | 更新游戏 | `pgl update pychat` |
| `pgl remove <游戏名>` | 卸载游戏 | `pgl remove pychat` |
| `pgl secure-set <add\|remove> <游戏名> [密码]` | 设置游戏密码 | `pgl secure-set add pychat mypassword` |
| `pgl list` | 列出已安装的游戏 | `pgl list` |
| `pgl market` | 浏览游戏市场 | `pgl market` |
| `pgl info <游戏名>` | 查看游戏详情 | `pgl info pychat` |

### 安全模式

当检测到课堂管理软件(如极域课堂管理)时,启动器会自动切换至安全模式。

**检测的进程:**
- `StudentMain.exe` - 极域学生端
- `Teacher.exe` - 极域教师端
- `Student.exe` - 极域学生端(旧版)
- `LanStar.exe` - 蓝鸽
- `NetSupport.exe` - NetSupport
- `ClassManager.exe` - 课堂管理通用

**安全模式限制:**
- ✅ 允许运行已安装的游戏
- ❌ 禁用游戏安装功能
- ❌ 禁用游戏更新功能
- ❌ 禁用游戏卸载功能

**安全模式密码:** 默认为 `safe`

### 内置游戏市场

| ID | 名称 | 分类 | 描述 | 仓库 | 分支 | 启动脚本 |
|----|------|------|------|------|------|---------|
| `pychat` | PyChat - 你的休闲搭子 | 社交 | 基于 Python 的多人在线聊天应用 | `Git32Design/Python-Chat---Project--003` | `master` | `client.py` |
| `pycmd` | PYcmd | 工具 | 个人工具集合 | `Git32Design/logrec-and-PYcmd` | `main` | `PYcmd/PYcmd.py` |

### 添加新游戏

在 `PyGameLauncher.py` 的 `BUILTIN_MARKET` 字典中添加新游戏配置:

```python
"game_id": {
    "name": "游戏名称",
    "repo": "owner/repository",
    "branch": "main",
    "description": "游戏描述",
    "startup_script": "main.py",
    "category": "分类"
}
```

### 项目结构

```
PyGameLauncher/
├── PyGameLauncher.py       # 主程序
├── games_security.db       # 游戏密码数据库
├── gamessrc/               # 游戏安装目录
│   └── [游戏名]/
├── README.md               # 项目说明
└── Update msgs.md          # 更新日志
```

### 数据库

**games_security.db:**
存储游戏密码保护信息,使用 SQLite 数据库。

表结构:
```sql
CREATE TABLE game_security (
    game_id TEXT PRIMARY KEY,
    password TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 智能功能

1. **自动检测启动脚本**:
   按优先级检测以下脚本:
   - `client.py` - 客户端
   - `main.py` - 主程序
   - `start.py` - 启动脚本
   - `run.py` - 运行脚本
   - `launcher.py` - 启动器
   - `app.py` - 应用程序
   - `game.py` - 游戏主程序

2. **游戏 ID 不区分大小写**:
   - 安装: `pgl install PYCHAT` 等同于 `pgl install pychat`
   - 运行: `pgl run PyChat` 等同于 `pgl run pychat`

3. **版本管理**:
   - 优先使用 Git 标签(tag)
   - 如果没有标签,使用提交哈希的前 7 位

### 密码保护

为游戏设置密码保护:

1. **设置密码**:
```bash
pgl secure-set add pychat mypassword
```

2. **运行时需要密码**:
```bash
pgl run pychat mypassword
```

3. **移除密码**:
```bash
pgl secure-set remove pychat
```

### 常见问题

1. **Git 未安装**:
   - Windows: https://git-scm.com/download/win
   - macOS: `brew install git`
   - Linux: `sudo apt install git`

2. **课堂环境限制**:
   - 启动器会自动进入安全模式
   - 输入密码 `safe` 即可验证

3. **游戏启动失败**:
   - 检查游戏是否已安装: `pgl list`
   - 检查启动脚本是否存在
   - 检查是否需要密码: `pgl info <游戏名>`

# 未来规划

## 预计: v2.0.0 Beta - GUI Version

### 图形界面

1. 开发 PyGame Launcher 的 GUI 版本
2. 支持游戏封面和截图预览
3. 更直观的游戏管理界面

## 预计: v3.0.0 Beta - Advanced Features

### 高级功能

1. **游戏评分系统**:
   - 用户可以给游戏评分
   - 显示游戏平均评分

2. **游戏自动更新**:
   - 自动检测游戏更新
   - 可配置自动更新策略

3. **多游戏市场支持**:
   - 支持自定义游戏市场
   - 支持从多个源获取游戏

4. **游戏依赖管理**:
   - 自动检测和安装游戏依赖
   - 支持 `requirements.txt`

5. **云存档同步**:
   - 支持游戏存档上传和下载
   - 跨设备同步存档

## 预计: v4.0.0 Beta - Ecosystem

### 生态系统

1. **开发者工具**:
   - 游戏开发者上传工具
   - 游戏验证系统

2. **社区功能**:
   - 游戏评论系统
   - 用户社区和论坛

3. **插件系统**:
   - 支持第三方插件
   - 插件市场
