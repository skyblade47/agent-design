"""
项目预览服务器 - Hermes Agent Framework
提供本地预览功能，用于查看生成的项目
"""

import http.server
import socketserver
import threading
import os
import webbrowser
from typing import Optional, Dict, Any, Callable
from pathlib import Path
import socket


class PreviewServer:
    """
    本地预览服务器
    用于预览项目文件
    """
    
    def __init__(
        self,
        directory: str,
        port: int = 8000,
        host: str = "127.0.0.1",
        auto_open: bool = True
    ):
        self.directory = directory
        self.port = port
        self.host = host
        self.auto_open = auto_open
        self.server_thread: Optional[threading.Thread] = None
        self.httpd: Optional[socketserver.TCPServer] = None
        self.is_running = False
        
    def _find_free_port(self, start_port: int = 8000, max_tries: int = 100) -> int:
        """找到一个可用的端口"""
        for port in range(start_port, start_port + max_tries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.host, port))
                    return port
            except OSError:
                continue
        raise RuntimeError(f"无法在 {start_port}-{start_port+max_tries-1} 范围内找到可用端口")
    
    def start(self) -> str:
        """
        启动预览服务器
        
        Returns:
            服务器URL
        """
        if self.is_running:
            return self.get_url()
        
        # 查找可用端口
        if self.port == 0:
            self.port = self._find_free_port()
        else:
            try:
                # 测试端口是否可用
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.host, self.port))
            except OSError:
                # 端口不可用，找新的
                self.port = self._find_free_port(8000)
        
        # 创建处理器
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=self.directory, **kwargs)
        
        # 启动服务器
        self.httpd = socketserver.TCPServer((self.host, self.port), Handler)
        self.is_running = True
        
        # 后台线程运行
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        
        url = self.get_url()
        
        # 自动打开浏览器
        if self.auto_open:
            webbrowser.open(url)
        
        return url
    
    def _run_server(self):
        """在后台线程中运行服务器"""
        if self.httpd:
            self.httpd.serve_forever()
    
    def stop(self):
        """停止服务器"""
        if self.httpd and self.is_running:
            self.is_running = False
            self.httpd.shutdown()
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=2)
    
    def get_url(self) -> str:
        """获取服务器URL"""
        return f"http://{self.host}:{self.port}"
    
    def is_available(self) -> bool:
        """检查服务器是否正在运行"""
        return self.is_running


class ProjectPreviewManager:
    """
    项目预览管理器
    管理多个项目的预览
    """
    
    def __init__(self):
        self.servers: Dict[str, PreviewServer] = {}
        
    def start_preview(
        self,
        project_name: str,
        directory: str,
        port: int = 0,
        auto_open: bool = True
    ) -> tuple[bool, str, Optional[str]]:
        """
        启动项目预览
        
        Args:
            project_name: 项目名称
            directory: 项目目录
            port: 端口（0表示自动选择）
            auto_open: 是否自动打开浏览器
            
        Returns:
            (成功, 消息, URL)
        """
        if not os.path.exists(directory):
            return False, f"目录不存在: {directory}", None
        
        # 停止已存在的
        if project_name in self.servers:
            self.stop_preview(project_name)
        
        try:
            server = PreviewServer(
                directory=directory,
                port=port,
                auto_open=auto_open
            )
            url = server.start()
            self.servers[project_name] = server
            return True, f"预览已启动: {url}", url
        except Exception as e:
            return False, f"启动预览失败: {str(e)}", None
    
    def stop_preview(self, project_name: str) -> tuple[bool, str]:
        """
        停止项目预览
        
        Args:
            project_name: 项目名称
            
        Returns:
            (成功, 消息)
        """
        if project_name not in self.servers:
            return False, f"没有找到项目预览: {project_name}"
        
        try:
            self.servers[project_name].stop()
            del self.servers[project_name]
            return True, f"预览已停止: {project_name}"
        except Exception as e:
            return False, f"停止预览失败: {str(e)}"
    
    def get_running_previews(self) -> Dict[str, str]:
        """
        获取正在运行的预览列表
        
        Returns:
            {项目名: URL}
        """
        result = {}
        for name, server in self.servers.items():
            if server.is_available():
                result[name] = server.get_url()
        return result
    
    def stop_all(self):
        """停止所有预览"""
        for name in list(self.servers.keys()):
            self.stop_preview(name)
    
    def __del__(self):
        """清理"""
        self.stop_all()

