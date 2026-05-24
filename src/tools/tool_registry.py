"""
工具注册表 - Hermes Agent Framework
统一管理所有可用工具
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from enum import Enum
import json

from .file_tools import FileTools, FileOperationResult
from .file_editor import EnhancedFileEditor
from .powershell_tool import (
    PowerShellExecutor, PowerShellSecurityPolicy, CommandExecutionResult, CommandRiskLevel
)
from .preview_server import ProjectPreviewManager
from ..scaffold.project_generator import ProjectScaffoldGenerator, ProjectConfig


class ToolCategory(Enum):
    """工具分类"""
    FILE_OPERATION = "file_operation"
    CODE_EDITING = "code_editing"
    COMMAND_EXECUTION = "command_execution"
    PROJECT_SCAFFOLD = "project_scaffold"
    PREVIEW = "preview"
    SECURITY = "security"


@dataclass
class ToolDefinition:
    """工具定义"""
    name: str
    category: ToolCategory
    description: str
    callable: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    required_permission_level: str = "user"  # "user", "sudo", "admin"
    risk_level: str = "low"  # "low", "medium", "high", "critical"


class HermesToolkit:
    """
    Hermes工具集
    统一管理所有工具
    """
    
    def __init__(
        self,
        base_directory: Optional[str] = None,
        enable_preview: bool = True,
        strict_security: bool = True
    ):
        self.base_directory = base_directory
        self.strict_security = strict_security
        
        # 初始化各个工具
        self.file_tools = FileTools(base_directory)
        self.file_editor = EnhancedFileEditor(self.file_tools)
        self.powershell = PowerShellExecutor(
            working_dir=base_directory,
            require_approval_for_medium_risk=strict_security
        )
        self.scaffold_generator = ProjectScaffoldGenerator(self.file_tools)
        
        self.preview_manager = ProjectPreviewManager() if enable_preview else None
        
        # 工具注册表
        self._tools: Dict[str, ToolDefinition] = {}
        self._register_tools()
        
        # 工具使用历史
        self.usage_history: List[Dict[str, Any]] = []
    
    def _register_tools(self):
        """注册所有工具"""
        
        # 文件操作工具
        self._tools["read_file"] = ToolDefinition(
            name="read_file",
            category=ToolCategory.FILE_OPERATION,
            description="读取文件内容",
            callable=self.file_tools.read_file,
            parameters={"file_path": "str"},
            required_permission_level="user",
            risk_level="low"
        )
        
        self._tools["write_file"] = ToolDefinition(
            name="write_file",
            category=ToolCategory.FILE_OPERATION,
            description="写入文件内容",
            callable=self.file_tools.write_file,
            parameters={"file_path": "str", "content": "str", "overwrite": "bool=False"},
            required_permission_level="user",
            risk_level="medium"
        )
        
        self._tools["list_directory"] = ToolDefinition(
            name="list_directory",
            category=ToolCategory.FILE_OPERATION,
            description="列出目录内容",
            callable=self.file_tools.list_directory,
            parameters={"dir_path": "str", "include_hidden": "bool=False"},
            required_permission_level="user",
            risk_level="low"
        )
        
        self._tools["create_directory"] = ToolDefinition(
            name="create_directory",
            category=ToolCategory.FILE_OPERATION,
            description="创建目录",
            callable=self.file_tools.create_directory,
            parameters={"dir_path": "str"},
            required_permission_level="user",
            risk_level="low"
        )
        
        # 增强的文件编辑工具
        self._tools["read_with_lines"] = ToolDefinition(
            name="read_with_lines",
            category=ToolCategory.CODE_EDITING,
            description="读取文件并显示行号",
            callable=self.file_editor.read_with_line_numbers,
            parameters={"file_path": "str"},
            required_permission_level="user",
            risk_level="low"
        )
        
        self._tools["insert_text"] = ToolDefinition(
            name="insert_text",
            category=ToolCategory.CODE_EDITING,
            description="在指定位置插入文本",
            callable=self.file_editor.insert_text,
            parameters={"file_path": "str", "text": "str", "line_number": "int"},
            required_permission_level="user",
            risk_level="medium"
        )
        
        self._tools["replace_text"] = ToolDefinition(
            name="replace_text",
            category=ToolCategory.CODE_EDITING,
            description="替换文本",
            callable=self.file_editor.replace_text,
            parameters={"file_path": "str", "old_text": "str", "new_text": "str"},
            required_permission_level="user",
            risk_level="medium"
        )
        
        self._tools["search_text"] = ToolDefinition(
            name="search_text",
            category=ToolCategory.CODE_EDITING,
            description="在文件中搜索文本",
            callable=self.file_editor.search_text,
            parameters={"file_path": "str", "search_pattern": "str"},
            required_permission_level="user",
            risk_level="low"
        )
        
        # PowerShell工具
        self._tools["execute_powershell"] = ToolDefinition(
            name="execute_powershell",
            category=ToolCategory.COMMAND_EXECUTION,
            description="执行PowerShell命令（带安全检查）",
            callable=self._execute_powershell_safe,
            parameters={"command": "str"},
            required_permission_level="user",
            risk_level="medium"
        )
        
        # 项目脚手架工具
        self._tools["generate_project"] = ToolDefinition(
            name="generate_project",
            category=ToolCategory.PROJECT_SCAFFOLD,
            description="生成标准项目结构",
            callable=self._generate_project_safe,
            parameters={"name": "str", "description": "str", "project_type": "str", "author": "str"},
            required_permission_level="user",
            risk_level="low"
        )
        
        # 预览工具
        if self.preview_manager:
            self._tools["start_preview"] = ToolDefinition(
                name="start_preview",
                category=ToolCategory.PREVIEW,
                description="启动项目预览",
                callable=self.preview_manager.start_preview,
                parameters={"project_name": "str", "directory": "str"},
                required_permission_level="user",
                risk_level="low"
            )
            
            self._tools["stop_preview"] = ToolDefinition(
                name="stop_preview",
                category=ToolCategory.PREVIEW,
                description="停止项目预览",
                callable=self.preview_manager.stop_preview,
                parameters={"project_name": "str"},
                required_permission_level="user",
                risk_level="low"
            )
    
    def _execute_powershell_safe(self, command: str, **kwargs) -> CommandExecutionResult:
        """安全执行PowerShell命令的包装器"""
        result = self.powershell.execute(command, **kwargs)
        self.usage_history.append({
            "tool": "execute_powershell",
            "command": command,
            "success": result.success,
            "risk_level": result.risk_level.value,
            "timestamp": __import__("time").time()
        })
        return result
    
    def _generate_project_safe(
        self,
        name: str,
        description: str,
        project_type: str,
        author: str,
        **kwargs
    ) -> Dict[str, Any]:
        """安全生成项目的包装器"""
        config = ProjectConfig(
            name=name,
            description=description,
            project_type=project_type,
            author=author
        )
        result = self.scaffold_generator.generate_project(config)
        self.usage_history.append({
            "tool": "generate_project",
            "name": name,
            "type": project_type,
            "success": result.get("success", False),
            "timestamp": __import__("time").time()
        })
        return result
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """获取工具定义"""
        return self._tools.get(name)
    
    def list_tools(self, category: Optional[ToolCategory] = None) -> List[ToolDefinition]:
        """列出所有可用工具"""
        tools = list(self._tools.values())
        if category:
            tools = [t for t in tools if t.category == category]
        return tools
    
    def get_security_summary(self) -> Dict[str, Any]:
        """获取安全摘要"""
        return {
            "strict_mode": self.strict_security,
            "base_directory": self.base_directory,
            "total_tools": len(self._tools),
            "high_risk_tools": len([t for t in self._tools.values() if t.risk_level in ["high", "critical"]]),
            "usage_count": len(self.usage_history)
        }

