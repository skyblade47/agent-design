"""
文件操作工具 - Hermes Agent Framework
提供安全的文件读写、目录操作功能
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class FileOperationResult:
    """文件操作结果"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None


class FileTools:
    """
    安全的文件操作工具
    包含行为边界控制，防止危险操作
    """
    
    def __init__(self, base_directory: Optional[str] = None):
        """
        初始化文件工具
        
        Args:
            base_directory: 基础工作目录，所有操作限制在此目录下
        """
        if base_directory is None:
            # 默认使用当前目录下的workspace
            base_directory = os.path.join(os.getcwd(), "workspace")
        
        self.base_directory = Path(base_directory).resolve()
        self._ensure_base_directory()
        
    def _ensure_base_directory(self) -> None:
        """确保基础目录存在"""
        self.base_directory.mkdir(parents=True, exist_ok=True)
        
    def _resolve_path(self, relative_path: str) -> Path:
        """
        解析相对路径为绝对路径，并验证安全性
        
        Args:
            relative_path: 相对基础目录的路径
            
        Returns:
            解析后的绝对路径
            
        Raises:
            ValueError: 如果路径尝试逃出基础目录
        """
        full_path = (self.base_directory / relative_path).resolve()
        
        # 检查是否在基础目录内
        if not str(full_path).startswith(str(self.base_directory)):
            raise ValueError(
                f"路径 '{relative_path}' 尝试逃出基础目录，操作被拒绝！"
            )
            
        return full_path
        
    def read_file(self, file_path: str) -> FileOperationResult:
        """
        读取文件内容
        
        Args:
            file_path: 相对基础目录的文件路径
            
        Returns:
            FileOperationResult
        """
        try:
            full_path = self._resolve_path(file_path)
            
            if not full_path.exists():
                return FileOperationResult(
                    success=False,
                    message=f"文件不存在: {file_path}",
                    error="File not found"
                )
                
            if not full_path.is_file():
                return FileOperationResult(
                    success=False,
                    message=f"不是文件: {file_path}",
                    error="Not a file"
                )
                
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return FileOperationResult(
                success=True,
                message=f"成功读取文件: {file_path}",
                data=content
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"读取文件失败: {str(e)}",
                error=str(e)
            )
            
    def write_file(self, file_path: str, content: str, overwrite: bool = False) -> FileOperationResult:
        """
        写入文件内容
        
        Args:
            file_path: 相对基础目录的文件路径
            content: 要写入的内容
            overwrite: 是否允许覆盖已有文件
            
        Returns:
            FileOperationResult
        """
        try:
            full_path = self._resolve_path(file_path)
            
            # 检查是否已存在
            if full_path.exists() and not overwrite:
                return FileOperationResult(
                    success=False,
                    message=f"文件已存在且不允许覆盖: {file_path}",
                    error="File exists"
                )
                
            # 确保目录存在
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return FileOperationResult(
                success=True,
                message=f"成功写入文件: {file_path}"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"写入文件失败: {str(e)}",
                error=str(e)
            )
            
    def list_directory(self, dir_path: str = ".", include_hidden: bool = False) -> FileOperationResult:
        """
        列出目录内容
        
        Args:
            dir_path: 相对基础目录的目录路径
            include_hidden: 是否包含隐藏文件
            
        Returns:
            FileOperationResult
        """
        try:
            full_path = self._resolve_path(dir_path)
            
            if not full_path.exists():
                return FileOperationResult(
                    success=False,
                    message=f"目录不存在: {dir_path}",
                    error="Directory not found"
                )
                
            if not full_path.is_dir():
                return FileOperationResult(
                    success=False,
                    message=f"不是目录: {dir_path}",
                    error="Not a directory"
                )
                
            contents = []
            for item in full_path.iterdir():
                if not include_hidden and item.name.startswith('.'):
                    continue
                    
                item_info = {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "path": str(item.relative_to(self.base_directory))
                }
                contents.append(item_info)
                
            # 按类型和名称排序
            contents.sort(key=lambda x: (x["type"] != "directory", x["name"]))
                
            return FileOperationResult(
                success=True,
                message=f"成功列出目录: {dir_path}",
                data=contents
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"列出目录失败: {str(e)}",
                error=str(e)
            )
            
    def create_directory(self, dir_path: str) -> FileOperationResult:
        """
        创建目录
        
        Args:
            dir_path: 相对基础目录的目录路径
            
        Returns:
            FileOperationResult
        """
        try:
            full_path = self._resolve_path(dir_path)
            full_path.mkdir(parents=True, exist_ok=True)
            
            return FileOperationResult(
                success=True,
                message=f"成功创建目录: {dir_path}"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"创建目录失败: {str(e)}",
                error=str(e)
            )
            
    def file_exists(self, file_path: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            file_path: 相对基础目录的文件路径
            
        Returns:
            bool
        """
        try:
            full_path = self._resolve_path(file_path)
            return full_path.exists() and full_path.is_file()
        except:
            return False
            
    def get_project_tree(self, max_depth: int = 3) -> FileOperationResult:
        """
        获取项目目录树
        
        Args:
            max_depth: 最大深度
            
        Returns:
            FileOperationResult
        """
        
        def _build_tree(path: Path, current_depth: int) -> Dict[str, Any]:
            """递归构建目录树"""
            if current_depth > max_depth:
                return {}
                
            result = {
                "name": path.name,
                "type": "directory" if path.is_dir() else "file",
                "children": []
            }
            
            if path.is_dir():
                for item in path.iterdir():
                    if item.name.startswith('.'):
                        continue
                        
                    child = _build_tree(item, current_depth + 1)
                    if child:
                        result["children"].append(child)
                        
            return result
        
        try:
            tree = _build_tree(self.base_directory, 0)
            return FileOperationResult(
                success=True,
                message="成功获取项目目录树",
                data=tree
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"获取项目目录树失败: {str(e)}",
                error=str(e)
            )

