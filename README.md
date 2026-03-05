# PyGame Launcher - CLI Version

<div align="center">

一个基于 Python 的命令行游戏启动器,用于管理和启动基于 GitHub 仓库的游戏。

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v2.2.2%20Beta-orange)](Update%20msgs.md)

</div>

---

## 项目简介

PyGame Launcher 是一个命令行版本的游戏启动器,用于管理和启动基于 GitHub 仓库的游戏。支持游戏下载、安装、更新、卸载和启动功能,内置游戏市场和安全特性。

### 主要特性

- **游戏市场** - 浏览和下载可用的游戏
- **游戏安装** - 通过 Git 克隆 GitHub 仓库
- **游戏更新** - 更新已安装的游戏到最新版本
- **游戏卸载** - 删除本地游戏
- **游戏启动** - 启动已安装的游戏
- **版本管理** - 查看游戏版本信息
- **密码保护** - 为游戏设置启动密码
- **安全模式** - 检测课堂管理环境,自动切换至安全模式
- **智能检测** - 自动检测启动脚本,无需手动配置

---

## 环境要求

- Python 3.7 或更高版本
- Git (必须预装) - 下载地址: https://git-scm.com/downloads

---

## 快速开始

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/Git32-Design/PyGameLauncher.git
cd PyGameLauncher
```

2. 确保已安装 Git
```bash
git --version
```

### 启动方式

#### 命令行模式

直接运行命令:
```bash
python PyGameLauncher.py
```

运行指定命令:
```bash
python PyGameLauncher.py help
python PyGameLauncher.py install pychat
python PyGameLauncher.py run pychat
```

#### 交互模式

不带参数运行进入交互模式:
```bash
python PyGameLauncher.py
```

交互模式提示符:
```
PGL [I:]-|> help
PGL [I:]-|> install pychat
PGL [I:]-|> run pychat
PGL [I:]-|> exit
```

---

## 使用指南

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

### 游戏安装

1. 查看可用游戏:
```bash
pgl market
```

2. 安装游戏:
```bash
pgl install pychat
```

3. 运行游戏:
```bash
pgl run pychat
```

### 密码保护

为游戏设置密码保护:

1. 设置密码:
```bash
pgl secure-set add pychat mypassword
```

2. 运行时需要密码:
```bash
pgl run pychat mypassword
```

3. 移除密码:
```bash
pgl secure-set remove pychat
```

### 游戏更新

更新已安装的游戏:
```bash
pgl update pychat
```

### 游戏卸载

卸载游戏:
```bash
pgl remove pychat
```

---

## 安全模式

当检测到课堂管理软件(如极域课堂管理)时,启动器会自动切换至安全模式。

**安全模式限制:**
- ✅ 允许运行已安装的游戏
- ❌ 禁用游戏安装功能
- ❌ 禁用游戏更新功能
- ❌ 禁用游戏卸载功能

**安全模式密码:** 默认为 `safe`

---

## 项目结构

```
PyGameLauncher/
├── PyGameLauncher.py       # 主程序
├── games_security.db       # 游戏密码数据库
├── games_market.db         # 游戏市场数据库(未使用,采用内置市场)
├── gamessrc/               # 游戏安装目录
│   └── [游戏名]/
├── README.md               # 项目说明
└── Update msgs.md          # 更新日志
```

---

## 游戏市场

### 内置游戏

| ID | 名称 | 分类 | 描述 |
|----|------|------|------|
| `pychat` | PyChat - 你的休闲搭子 | 社交 | 基于 Python 的多人在线聊天应用 |
| `pycmd` | PYcmd | 工具 | 个人工具集合 |

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

---

## 更新日志

### v1.0.0 Beta (2026-03-03)
- 初始版本发布
- 基础游戏安装/卸载/运行功能
- 内置游戏市场
- 密码保护功能
- 安全模式(课堂环境检测)
- 交互模式和命令行模式
- 自动启动脚本检测
- 游戏版本管理

查看完整更新日志: [Update msgs.md](Update%20msgs.md)

---

## 团队贡献

| 角色 | 贡献者 | 职责 |
|------|--------|------|
| 概念设计 | Git32-Design | 设计游戏启动器概念 |
| 代码实现 | Tencent Cloud CodeBuddy | 使用 Tencent Cloud CodeBuddy 工具编写 |

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 未来规划

- [ ] GUI 图形界面版本
- [ ] 游戏评分系统
- [ ] 游戏自动更新
- [ ] 游戏截图预览
- [ ] 多游戏市场支持
- [ ] 游戏依赖管理
- [ ] 云存档同步

---

## 常见问题

### Git 未安装

如果提示 "Git 未安装或不可用",请先安装 Git:
- Windows: https://git-scm.com/download/win
- macOS: `brew install git`
- Linux: `sudo apt install git`

### 课堂环境限制

如果在电脑课环境中使用,启动器会自动进入安全模式。输入密码 `safe` 即可验证。

### 游戏启动失败

如果游戏启动失败,检查:
1. 游戏是否已安装: `pgl list`
2. 启动脚本是否存在
3. 是否需要密码: `pgl info <游戏名>`

---

## 联系我们

如有问题或建议,欢迎提交 Issue 或 Pull Request!

<div align="center">

**Made with ❤️ by Git32-Design & Tencent Cloud CodeBuddy**

</div>
