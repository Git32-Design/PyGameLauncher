# PyGameLauncher.py

"""
NoticeInfo
---------------------------|
Project: PyGame Launcher - CLI Version 启动器命令行版
Author: Git32-Design/Tencent Cloud CodeBuddy
Description:
PyGame Launcher 的 CLI 版本，用于管理和启动基于 GitHub 仓库的游戏。
支持游戏下载、安装、更新、卸载和启动功能。
Created: 2026-03-03
License: MIT License
Features:
- 游戏市场：浏览可用游戏
- 游戏安装：通过 Git 克隆 GitHub 仓库
- 游戏更新：更新已安装的游戏
- 游戏卸载：删除本地游戏
- 游戏启动：启动已安装的游戏
- 版本管理：查看游戏版本信息
Dependencies:
- Git (必须预装)
- Python 3.7+
Usage:
    python PyGameLauncher.py
Main Designs:
    Git32-Design - 概念设计
    TC Codebuddy - 代码实现
Exceptions:
- 未安装Git则禁用install和update指令
- 检测到“极域课堂管理”软件（检测电脑课环境），则需要输入safe-mode转入安全模式，安全模式下禁用install、update、remove等指令，仅允许运行已安装的游戏
======
"""
import os
import sys
import subprocess
import shutil
from typing import Optional, List, Dict
from pathlib import Path

# ------------------- 配置 -------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 更改工作目录为脚本所在目录
GAMES_DIR = "./gamessrc"
MARKET_DB = "./games_market.db"
# 内置游戏市场（可扩展为数据库）
BUILTIN_MARKET = {
    "pychat": {
        "name": "PyChat - 你的休闲搭子",
        "repo": "Git32Design/Python-Chat---Project--003",
        "branch": "master",
        "description": "基于 Python 的多人在线聊天应用",
        "startup_script": "client.py",
        "category": "社交"
    },
    "pycmd": {
        "name": "PYcmd",
        "repo": "Git32Design/logrec-and-PYcmd",
        "branch": "main",
        "description": "个人工具集合",
        "startup_script": "PYcmd/PYcmd.py",
        "category": "工具"
    },
    # 可以添加更多游戏/项目
}


class GitHubGameDownloader:
    """使用 Git 下载/更新游戏"""
    
    def __init__(self, games_dir: str = GAMES_DIR):
        self.games_dir = games_dir
        self.git_available = self._check_git_available()
        self._ensure_directory_exists()
    
    def _check_git_available(self) -> bool:
        """检查 Git 是否可用"""
        try:
            subprocess.run(
                ["git", "--version"],
                capture_output=True,
                check=True,
                shell=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _ensure_git_available(self):
        """确保 Git 可用（旧方法，已弃用）"""
        if not self.git_available:
            raise RuntimeError(
                "Git 未安装或不在 PATH 中。请先安装 Git: https://git-scm.com/downloads"
            )
    
    def _ensure_directory_exists(self):
        """确保游戏目录存在"""
        if not os.path.exists(self.games_dir):
            os.makedirs(self.games_dir)
    
    def clone_game(
        self,
        repo: str,
        game_name: str,
        branch: Optional[str] = None,
        tag: Optional[str] = None
    ) -> str:
        """
        克隆游戏仓库
        
        Args:
            repo: GitHub 仓库格式 (owner/repo)
            game_name: 游戏在本地的文件夹名
            branch: 指定分支 (可选)
            tag: 指定标签/版本 (可选)
        
        Returns:
            游戏安装路径
        """
        game_path = os.path.join(self.games_dir, game_name)
        
        if os.path.exists(game_path):
            return game_path
        
        clone_url = f"https://github.com/{repo}.git"
        cmd = ["git", "clone"]
        
        if branch:
            cmd.extend(["--branch", branch])
        elif tag:
            cmd.extend(["--branch", tag])
        
        cmd.extend([clone_url, game_path])
        
        try:
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            return game_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"克隆失败: {e.stderr}")
    
    def update_game(self, game_name: str) -> str:
        """更新已安装的游戏"""
        game_path = os.path.join(self.games_dir, game_name)
        
        if not os.path.exists(game_path):
            raise FileNotFoundError(f"游戏未安装: {game_name}")
        
        try:
            os.chdir(game_path)
            subprocess.run(
                ["git", "pull"],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            return game_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"更新失败: {e.stderr}")
    
    def get_game_version(self, game_name: str) -> str:
        """获取游戏当前版本"""
        game_path = os.path.join(self.games_dir, game_name)
        
        if not os.path.exists(game_path):
            raise FileNotFoundError(f"游戏未安装: {game_name}")
        
        os.chdir(game_path)
        
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            return result.stdout.strip()
    
    def remove_game(self, game_name: str) -> bool:
        """删除已安装的游戏"""
        game_path = os.path.join(self.games_dir, game_name)
        
        if not os.path.exists(game_path):
            return False
        
        try:
            shutil.rmtree(game_path)
            return True
        except Exception:
            return False
    
    def list_installed_games(self) -> List[str]:
        """列出已安装的游戏"""
        if not os.path.exists(self.games_dir):
            return []
        
        games = []
        for name in os.listdir(self.games_dir):
            game_path = os.path.join(self.games_dir, name)
            if os.path.isdir(game_path) and os.path.exists(os.path.join(game_path, ".git")):
                games.append(name)
        
        return games


class GameSecurity:
    """游戏安全管理"""

    def __init__(self, db_path: Optional[str] = None):
        # 使用绝对路径,避免因工作目录切换而在错误位置创建数据库
        if db_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "games_security.db")
        self.db_path = os.path.abspath(db_path)
        self._init_db()
    
    def _init_db(self):
        """初始化安全数据库"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_security (
                game_id TEXT PRIMARY KEY,
                password TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_password(self, game_id: str, password: str) -> bool:
        """添加游戏密码"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT OR REPLACE INTO game_security (game_id, password) VALUES (?, ?)',
                (game_id, password)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
    
    def remove_password(self, game_id: str) -> bool:
        """移除游戏密码"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM game_security WHERE game_id = ?', (game_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            return False
        finally:
            conn.close()
    
    def verify_password(self, game_id: str, password: str) -> bool:
        """验证游戏密码"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT password FROM game_security WHERE game_id = ?',
                (game_id,)
            )
            result = cursor.fetchone()
            
            if result is None:
                # 没有设置密码，允许运行
                return True
            
            return result[0] == password
        except Exception:
            return False
        finally:
            conn.close()
    
    def has_password(self, game_id: str) -> bool:
        """检查游戏是否设置了密码"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT COUNT(*) FROM game_security WHERE game_id = ?',
                (game_id,)
            )
            result = cursor.fetchone()
            return result[0] > 0
        except Exception:
            return False
        finally:
            conn.close()
    
    def list_secured_games(self) -> List[str]:
        """列出所有设置了密码的游戏"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT game_id FROM game_security')
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception:
            return []
        finally:
            conn.close()


class ClassroomMonitor:
    """课堂环境检测"""
    
    @staticmethod
    def detect_classroom_software() -> bool:
        """检测是否在课堂管理环境（如极域课堂管理）"""
        try:
            # 检测 Windows 常见的课堂管理软件进程
            if sys.platform == 'win32':
                # 检查极域课堂管理进程
                processes = subprocess.run(
                    ['tasklist', '/FI', 'IMAGENAME eq StudentMain.exe'],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                if 'StudentMain.exe' in processes.stdout:
                    return True
                
                # 检查其他常见的课堂管理软件
                classroom_processes = [
                    'Teacher.exe',      # 极域教师端
                    'Student.exe',      # 极域学生端
                    'LanStar.exe',      # 蓝鸽
                    'NetSupport.exe',   # NetSupport
                    'ClassManager.exe', # 课堂管理通用名称
                ]
                
                for process_name in classroom_processes:
                    result = subprocess.run(
                        ['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
                        capture_output=True,
                        text=True,
                        shell=True
                    )
                    if process_name in result.stdout:
                        return True
            
            return False
        except Exception:
            return False
    
    @staticmethod
    def verify_safe_mode() -> bool:
        """验证安全模式密码"""
        print("\n" + "=" * 60)
        print("⚠ 检测到课堂管理软件环境")
        print("=" * 60)
        print("系统已自动切换至安全模式")
        print("安全模式下仅允许运行已安装的游戏")
        print("禁用功能：安装、更新、卸载等操作")
        print("=" * 60)
        
        password = input("\n请输入安全模式密码 (默认密码: safe): ").strip()
        
        # 默认密码验证（实际使用中可修改）
        return password.lower() == 'safe'


class GameMarket:
    """游戏市场"""
    
    def __init__(self, downloader: GitHubGameDownloader):
        self.downloader = downloader
        self.market = BUILTIN_MARKET
    
    def list_available_games(self) -> Dict[str, Dict]:
        """列出市场中的可用游戏"""
        return self.market
    
    def get_game_info(self, game_id: str) -> Optional[Dict]:
        """获取游戏信息"""
        return self.market.get(game_id)
    
    def install_game(self, game_id: str) -> str:
        """从市场安装游戏"""
        game_info = self.get_game_info(game_id)
        if not game_info:
            raise ValueError(f"游戏不存在: {game_id}")
        
        game_path = self.downloader.clone_game(
            repo=game_info['repo'],
            game_name=game_id,
            branch=game_info.get('branch')
        )
        
        return game_path
    
    def is_installed(self, game_id: str) -> bool:
        """检查游戏是否已安装"""
        return game_id in self.downloader.list_installed_games()


class PyGameLauncherCLI:
    """PyGame Launcher CLI 版本"""
    
    def __init__(self):
        self.downloader = GitHubGameDownloader()
        self.market = GameMarket(self.downloader)
        self.security = GameSecurity()
        
        # 检测环境
        self.safe_mode = False
        self.classroom_detected = ClassroomMonitor.detect_classroom_software()
        
        if self.classroom_detected:
            self.safe_mode = ClassroomMonitor.verify_safe_mode()
            if not self.safe_mode:
                print("\n✗ 安全模式验证失败，程序退出")
                sys.exit(1)
    
    def _normalize_game_id(self, game_id: str) -> str:
        """标准化游戏 ID（转换为小写用于查询市场）"""
        return game_id.lower()
    
    def _get_actual_game_dir(self, game_id: str) -> Optional[str]:
        """获取实际的游戏目录名称（可能包含原始大小写）"""
        normalized_id = self._normalize_game_id(game_id)
        
        # 如果游戏存在于市场，使用市场配置的 ID
        if self.market.get_game_info(normalized_id):
            return normalized_id
        
        # 否则，检查已安装的游戏目录
        if not os.path.exists(self.downloader.games_dir):
            return None
        
        # 查找匹配的目录（不区分大小写）
        for dir_name in os.listdir(self.downloader.games_dir):
            game_path = os.path.join(self.downloader.games_dir, dir_name)
            if os.path.isdir(game_path) and dir_name.lower() == normalized_id:
                return dir_name
        
        return None
    
    def print_help(self):
        """打印帮助信息"""
        print("\n" + "=" * 60)
        print("                     PyGame Launcher")
        print("                   命令行帮助文档")
        print("=" * 60)
        
        if self.safe_mode:
            print("\n【安全模式已启用】")
            print("  课堂管理环境检测中")
            print("  仅允许运行已安装的游戏")
            print("=" * 60)
        
        if not self.downloader.git_available:
            print("\n【警告】")
            print("  Git 未安装或不可用")
            print("  install 和 update 指令已被禁用")
            print("=" * 60)
        
        print("\n所有命令必须使用 'pgl' 前缀")
        print("\n可用命令:")
        print("  pgl help")
        print("      显示此帮助信息")
        
        if not self.safe_mode:
            if self.downloader.git_available:
                print("\n  pgl install <游戏名> | pgl append <游戏名>")
                print("      克隆 GitHub 游戏库至游戏资源文件夹")
                print("      示例: pgl install pychat")
            else:
                print("\n  pgl install <游戏名> | pgl append <游戏名>")
                print("      [已禁用] 需要安装 Git")
            
            if self.downloader.git_available:
                print("\n  pgl update <游戏名>")
                print("      更新指定的游戏")
                print("      示例: pgl update pychat")
            else:
                print("\n  pgl update <游戏名>")
                print("      [已禁用] 需要安装 Git")
        
        print("\n  pgl run <游戏名> [密码]")
        print("      打开对应游戏的主程序")
        print("      如果游戏设置了密码，必须提供正确密码才能启动")
        print("      示例: pgl run pychat")
        print("      示例: pgl run pychat mypassword")
        
        if not self.safe_mode:
            print("\n  pgl remove <游戏名> | pgl delete <游戏名>")
            print("      删除对应的游戏")
            print("      示例: pgl remove pychat")
        else:
            print("\n  pgl remove <游戏名> | pgl delete <游戏名>")
            print("      [已禁用] 安全模式下不可用")
        
        print("\n  pgl secure-set <add|remove> <游戏名> [密码]")
        print("      添加或移除游戏的运行密码")
        print("      添加: pgl secure-set add pychat mypassword")
        print("      移除: pgl secure-set remove pychat")
        
        print("\n  pgl list")
        print("      列出所有已安装的游戏")
        
        print("\n  pgl market")
        print("      浏览游戏市场")
        
        print("\n  pgl info <游戏名>")
        print("      查看游戏详细信息")
        
        print("\n" + "=" * 60)
    
    def cmd_install(self, game_id: str):
        """安装游戏"""
        # 检查安全模式
        if self.safe_mode:
            print("✗ 安装功能在安全模式下不可用")
            print("   安全模式仅允许运行已安装的游戏")
            return
        
        # 检查 Git 是否可用
        if not self.downloader.git_available:
            print("✗ Git 未安装或不可用")
            print("   请先安装 Git: https://git-scm.com/downloads")
            return
        
        normalized_id = self._normalize_game_id(game_id)
        
        info = self.market.get_game_info(normalized_id)
        if not info:
            print(f"✗ 游戏不存在: {game_id}")
            print(f"   使用 'pgl market' 查看可用游戏")
            return
        
        # 检查是否已安装
        actual_dir = self._get_actual_game_dir(normalized_id)
        if actual_dir:
            print(f"⚠ 游戏已安装: {actual_dir}")
            print(f"   如需更新，请使用: pgl run \"{actual_dir}\"")
            return
        
        try:
            print(f"正在安装 {info['name']}...")
            print(f"   仓库: {info['repo']}")
            
            path = self.market.install_game(normalized_id)
            version = self.downloader.get_game_version(normalized_id)
            
            print(f"✓ 安装成功！")
            print(f"   安装路径: {path}")
            print(f"   当前版本: {version}")
            print(f"   启动命令: pgl run {normalized_id}")
        except Exception as e:
            print(f"✗ 安装失败: {e}")
    
    def cmd_append(self, game_id: str):
        """安装游戏（install 的别名）"""
        self.cmd_install(game_id)
    
    def cmd_run(self, game_id: str, password: Optional[str] = None):
        """启动游戏"""
        normalized_id = self._normalize_game_id(game_id)
        actual_dir = self._get_actual_game_dir(game_id)
        
        if not actual_dir:
            print(f"✗ 游戏未安装: {game_id}")
            # 如果游戏在市场中，提示安装命令
            if self.market.get_game_info(normalized_id):
                print(f"   使用 'pgl install {normalized_id}' 进行安装")
            return
        
        # 检查密码（使用规范化的 ID）
        if self.security.has_password(normalized_id):
            if password is None:
                print(f"⚠ 游戏设置了密码保护")
                password = input("请输入密码: ").strip()
            
            if not self.security.verify_password(normalized_id, password):
                print("✗ 密码错误，无法启动游戏")
                return
            print("✓ 密码验证通过")
        elif password is not None:
            print("⚠ 游戏未设置密码，密码参数将被忽略")
        
        game_path = os.path.join(self.downloader.games_dir, actual_dir)
        info = self.market.get_game_info(normalized_id)
        
        # 获取启动脚本
        if info and 'startup_script' in info:
            startup_script = info['startup_script']
        else:
            # 尝试自动检测启动脚本
            startup_script = self._detect_startup_script(game_path)
        
        script_path = os.path.join(game_path, startup_script)
        
        if not os.path.exists(script_path):
            print(f"✗ 未找到启动脚本: {startup_script}")
            print(f"   游戏路径: {game_path}")
            print(f"   请检查启动脚本名称或手动启动")
            return
        
        try:
            print(f"正在启动 {info['name'] if info else actual_dir}...")
            print(f"按 Ctrl+C 可关闭游戏\n")
            
            os.chdir(game_path)
            
            # 使用 subprocess.run 运行游戏，传递 Ctrl+C 信号
            subprocess.run(
                [sys.executable, startup_script],
                check=False
            )
            
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
        except KeyboardInterrupt:
            print("\n游戏已关闭")
        except Exception as e:
            print(f"✗ 启动失败: {e}")
    
    def _detect_startup_script(self, game_path: str) -> str:
        """自动检测启动脚本"""
        # 常见的启动脚本名称（按优先级排序）
        possible_scripts = [
            'client.py',      # 客户端
            'main.py',        # 主程序
            'start.py',       # 启动脚本
            'run.py',         # 运行脚本
            'launcher.py',    # 启动器
            'app.py',         # 应用程序
            'game.py',        # 游戏主程序
        ]
        
        # 检查目录中是否存在这些脚本
        for script in possible_scripts:
            script_path = os.path.join(game_path, script)
            if os.path.exists(script_path) and os.path.isfile(script_path):
                return script
        
        # 如果找不到，返回默认的 main.py
        return 'main.py'
    
    def cmd_remove(self, game_id: str):
        """删除游戏"""
        # 检查安全模式
        if self.safe_mode:
            print("✗ 卸载功能在安全模式下不可用")
            print("   安全模式仅允许运行已安装的游戏")
            return
        
        normalized_id = self._normalize_game_id(game_id)
        actual_dir = self._get_actual_game_dir(game_id)
        
        if not actual_dir:
            print(f"✗ 游戏未安装: {game_id}")
            return
        
        info = self.market.get_game_info(normalized_id)
        name = info['name'] if info else actual_dir
        
        confirm = input(f"确定要卸载 {name} 吗？(y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消卸载")
            return
        
        # 移除密码保护
        self.security.remove_password(normalized_id)
        
        try:
            if self.downloader.remove_game(actual_dir):
                print(f"✓ 卸载成功: {name}")
            else:
                print("✗ 卸载失败")
        except Exception as e:
            print(f"✗ 卸载失败: {e}")
    
    def cmd_delete(self, game_id: str):
        """删除游戏（remove 的别名）"""
        self.cmd_remove(game_id)
    
    def cmd_secure_set(self, action: str, game_id: str, password: Optional[str] = None):
        """设置游戏安全"""
        normalized_id = self._normalize_game_id(game_id)
        actual_dir = self._get_actual_game_dir(game_id)
        
        if action == 'add':
            if not actual_dir:
                print(f"✗ 游戏未安装: {game_id}")
                return
            
            if self.security.has_password(normalized_id):
                print("⚠ 游戏已设置密码")
                confirm = input("是否覆盖现有密码？(y/n): ").strip().lower()
                if confirm != 'y':
                    print("已取消")
                    return
            
            if password is None:
                password = input("请输入密码: ").strip()
                password2 = input("请再次输入密码: ").strip()
                if password != password2:
                    print("✗ 两次密码不一致")
                    return
            
            if self.security.add_password(normalized_id, password):
                print(f"✓ 密码设置成功")
                print(f"   游戏: {game_id}")
            else:
                print("✗ 密码设置失败")
        
        elif action == 'remove':
            if not self.security.has_password(normalized_id):
                print(f"⚠ 游戏未设置密码: {game_id}")
                return
            
            confirm = input(f"确定要移除 {game_id} 的密码吗？(y/n): ").strip().lower()
            if confirm != 'y':
                print("已取消")
                return
            
            if self.security.remove_password(normalized_id):
                print(f"✓ 密码已移除")
            else:
                print("✗ 密码移除失败")
        
        else:
            print(f"✗ 无效的操作: {action}")
            print("   可用操作: add, remove")
    
    def cmd_list(self):
        """列出已安装的游戏"""
        print("\n【已安装的游戏】")
        print("-" * 60)
        
        games = self.downloader.list_installed_games()
        if not games:
            print("暂未安装任何游戏")
            print("   使用 'pgl market' 查看可用游戏")
            return
        
        for i, game_id in enumerate(games, 1):
            try:
                version = self.downloader.get_game_version(game_id)
                info = self.market.get_game_info(game_id)
                name = info['name'] if info else game_id
                secured = " [🔒]" if self.security.has_password(game_id) else ""
                
                print(f"{i}. {name}{secured}")
                print(f"   ID: {game_id}")
                print(f"   版本: {version}")
                print()
            except Exception as e:
                print(f"{i}. {game_id} (版本信息获取失败)")
        
        print("-" * 60)
    
    def cmd_market(self):
        """列出游戏市场"""
        print("\n【游戏市场】")
        print("-" * 60)
        
        games = self.market.list_available_games()
        if not games:
            print("暂无可用游戏")
            return
        
        for i, (game_id, info) in enumerate(games.items(), 1):
            installed = " [已安装]" if self.market.is_installed(game_id) else ""
            secured = " [🔒]" if self.security.has_password(game_id) else ""
            
            print(f"\n{i}. {info['name']}{installed}{secured}")
            print(f"   ID: {game_id}")
            print(f"   分类: {info.get('category', '未分类')}")
            print(f"   描述: {info.get('description', '暂无描述')}")
            print(f"   仓库: {info['repo']}")
        
        print("-" * 60)
    
    def cmd_update(self, game_id: str):
        """更新游戏"""
        # 检查安全模式
        if self.safe_mode:
            print("✗ 更新功能在安全模式下不可用")
            print("   安全模式仅允许运行已安装的游戏")
            return
        
        # 检查 Git 是否可用
        if not self.downloader.git_available:
            print("✗ Git 未安装或不可用")
            print("   请先安装 Git: https://git-scm.com/downloads")
            return
        
        normalized_id = self._normalize_game_id(game_id)
        actual_dir = self._get_actual_game_dir(game_id)
        
        if not actual_dir:
            print(f"✗ 游戏未安装: {game_id}")
            return
        
        try:
            print(f"正在更新 {actual_dir}...")
            self.downloader.update_game(actual_dir)
            version = self.downloader.get_game_version(actual_dir)
            
            print(f"✓ 更新成功！")
            print(f"   当前版本: {version}")
        except Exception as e:
            print(f"✗ 更新失败: {e}")
    
    def cmd_info(self, game_id: str):
        """查看游戏信息"""
        normalized_id = self._normalize_game_id(game_id)
        
        info = self.market.get_game_info(normalized_id)
        if not info:
            print(f"✗ 游戏不存在: {game_id}")
            print(f"   使用 'pgl market' 查看可用游戏")
            return
        
        actual_dir = self._get_actual_game_dir(normalized_id)
        
        print(f"\n【游戏信息】")
        print("-" * 60)
        print(f"  名称: {info['name']}")
        print(f"  ID: {game_id}")
        print(f"  分类: {info.get('category', '未分类')}")
        print(f"  描述: {info.get('description', '暂无描述')}")
        print(f"  仓库: {info['repo']}")
        print(f"  分支: {info.get('branch', 'main')}")
        print(f"  启动脚本: {info.get('startup_script', 'main.py')}")
        
        if actual_dir:
            try:
                version = self.downloader.get_game_version(actual_dir)
                secured = "是" if self.security.has_password(normalized_id) else "否"
                print(f"  安装状态: 已安装")
                print(f"  实际目录: {actual_dir}")
                print(f"  当前版本: {version}")
                print(f"  密码保护: {secured}")
            except Exception:
                print(f"  安装状态: 已安装 (版本信息获取失败)")
        else:
            print(f"  安装状态: 未安装")
        
        print("-" * 60)
    
    def execute(self, args: List[str]):
        """执行命令"""
        if len(args) < 1:
            # 无参数时进入交互模式
            self.interactive_mode()
            return
        
        command = args[0].lower()
        
        if command == 'help':
            self.print_help()
        elif command in ('install', 'append'):
            if len(args) < 2:
                print("✗ 用法: pgl install <游戏名>")
                print("   示例: pgl install pychat")
                return
            if command == 'install':
                self.cmd_install(args[1])
            else:
                self.cmd_append(args[1])
        
        elif command == 'run':
            if len(args) < 2:
                print("✗ 用法: pgl run <游戏名> [密码]")
                print("   示例: pgl run pychat")
                return
            password = args[2] if len(args) > 2 else None
            self.cmd_run(args[1], password)
        
        elif command in ('remove', 'delete'):
            if len(args) < 2:
                print("✗ 用法: pgl remove <游戏名>")
                print("   示例: pgl remove pychat")
                return
            if command == 'remove':
                self.cmd_remove(args[1])
            else:
                self.cmd_delete(args[1])
        
        elif command == 'secure-set':
            if len(args) < 3:
                print("✗ 用法: pgl secure-set <add|remove> <游戏名> [密码]")
                print("   添加: pgl secure-set add pychat mypassword")
                print("   移除: pgl secure-set remove pychat")
                return
            password = args[3] if len(args) > 3 else None
            self.cmd_secure_set(args[1], args[2], password)
        
        elif command == 'list':
            self.cmd_list()
        
        elif command == 'market':
            self.cmd_market()
        
        elif command == 'update':
            if len(args) < 2:
                print("✗ 用法: pgl update <游戏名>")
                print("   示例: pgl update pychat")
                return
            self.cmd_update(args[1])
        
        elif command == 'info':
            if len(args) < 2:
                print("✗ 用法: pgl info <游戏名>")
                print("   示例: pgl info pychat")
                return
            self.cmd_info(args[1])
        
        else:
            print(f"✗ 未知命令: {command}")
            print("   使用 'pgl help' 查看帮助")
    
    def _parse_command(self, user_input: str) -> List[str]:
        """解析命令，支持带引号的参数"""
        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(user_input):
            char = user_input[i]
            
            # 处理引号
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                i += 1
                continue
            
            if char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                i += 1
                continue
            
            # 处理空格分隔参数
            if char == ' ' and not in_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
                i += 1
                continue
            
            # 添加字符到当前参数
            current_arg += char
            i += 1
        
        # 添加最后一个参数
        if current_arg:
            args.append(current_arg)
        
        return args
    
    def interactive_mode(self):
        """交互式模式"""
        print("===PyGame Launcher CLI===")
        
        if self.safe_mode:
            print("[安全模式已启用] 仅允许运行已安装的游戏")
        
        if not self.downloader.git_available:
            print("[警告] Git 未安装或不可用，install 和 update 指令已禁用")
        
        print("输入 'help' 查看帮助 | 输入 'exit' 退出\n")
        
        while True:
            try:
                # 获取当前工作目录
                cwd = os.getcwd()
                # 获取驱动器和工作目录（如 I:\Github）
                drive = os.path.splitdrive(cwd)[0]
                path = cwd.split(os.sep)[-1] if os.sep in cwd else '.'
                
                # 构建提示符
                prompt = f"PGL [{drive}]-|> "
                
                # 获取用户输入
                user_input = input(prompt).strip()
                
                # 处理退出命令
                if user_input.lower() in ('exit', 'quit', 'q'):
                    print("再见！")
                    break
                
                # 处理空输入
                if not user_input:
                    continue
                
                # 解析命令
                args = self._parse_command(user_input)
                
                # 如果以 pgl 开头，则移除
                if args and args[0].lower() == 'pgl':
                    args = args[1:]
                
                # 执行命令
                self.execute(args)
                
            except KeyboardInterrupt:
                print("\n输入 'exit' 退出，或按 Ctrl+C 强制退出")
            except Exception as e:
                print(f"\n发生错误: {e}")


def main():
    """主函数"""
    import sys
    
    try:
        launcher = PyGameLauncherCLI()
        
        # 获取命令行参数，跳过脚本名和 "pgl" 前缀（如果存在）
        args = sys.argv[1:]
        
        if args and args[0].lower() == 'pgl':
            args = args[1:]
        
        launcher.execute(args)
        
    except KeyboardInterrupt:
        print("\n\n程序已终止")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
