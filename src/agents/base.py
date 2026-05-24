"""
Agent基础类 - Hermes Agent Framework
包含扩展的Agent基类、工具集成和记忆管理
"""

from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
import json

from src.tools import (
    HermesToolkit,
    FileTools,
    EnhancedFileEditor,
    PowerShellExecutor,
)
from src.scaffold import ProjectScaffoldGenerator
from src.core.safety import DevelopmentStandards


class AgentRole(str, Enum):
    """Agent角色类型"""
    TEAM_LEAD = "team_lead"
    DEV_LEAD = "dev_lead"
    PRODUCT_MANAGER = "product_manager"
    TECHNICAL_ARCHITECT = "technical_architect"
    FRONTEND_DEVELOPER = "frontend_developer"
    BACKEND_DEVELOPER = "backend_developer"
    DEV_OPS = "dev_ops"
    QA_TESTER = "qa_tester"
    CODE_REVIEWER = "code_reviewer"
    UX_DESIGNER = "ux_designer"
    TECH_WRITER = "tech_writer"
    REFLECTION_AGENT = "reflection_agent"
    EVALUATION_AGENT = "evaluation_agent"


class AgentStatus(str, Enum):
    """Agent状态"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class AgentMessage:
    """Agent间消息"""
    message_id: str
    sender_agent: str
    recipient_agent: Optional[str]
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    message_type: str = "text"
    attachments: List[Dict] = field(default_factory=list)
    requires_response: bool = False

    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "sender_agent": self.sender_agent,
            "recipient_agent": self.recipient_agent,
            "content": self.content,
            "timestamp": self.timestamp,
            "message_type": self.message_type,
            "attachments": self.attachments,
            "requires_response": self.requires_response
        }


@dataclass
class AgentMemory:
    """Agent记忆系统"""
    short_term: List[AgentMessage] = field(default_factory=list)
    medium_term: List[Dict] = field(default_factory=list)
    long_term: List[Dict] = field(default_factory=list)
    max_short_term: int = 50
    max_medium_term: int = 100

    def add_message(self, message: AgentMessage):
        """添加消息到短期记忆"""
        self.short_term.append(message)
        if len(self.short_term) > self.max_short_term:
            # 归档旧消息到中期记忆
            archived = self.short_term.pop(0)
            self.medium_term.append({
                "type": "message",
                "content": archived.to_dict(),
                "archived_at": datetime.now().isoformat()
            })

    def get_context(self, limit: int = 10) -> str:
        """获取上下文"""
        recent = self.short_term[-limit:]
        context = "\n".join([f"[{msg.timestamp}] {msg.sender_agent}: {msg.content}" for msg in recent])
        return context

    def get_all_messages(self) -> List[AgentMessage]:
        """获取所有消息"""
        return self.short_term


class ExtendedBaseAgent(ABC):
    """
    扩展的Agent基类
    包含工具集成、记忆管理和安全控制
    """

    def __init__(
        self,
        name: str,
        role: AgentRole,
        toolkit: Optional[HermesToolkit] = None,
        description: str = "",
        system_prompt: Optional[str] = None,
    ):
        self.name = name
        self.role = role
        self.description = description
        self.toolkit = toolkit
        self.memory = AgentMemory()
        self.status = AgentStatus.IDLE
        self.created_at = datetime.now().isoformat()
        
        # 开发规范
        self.standards = DevelopmentStandards()
        
        # 系统提示词
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
        # 工具调用记录
        self.tool_usage_log = []
        
        # 等待审批的操作
        self.pending_approvals = []

    def _get_default_system_prompt(self) -> str:
        """获取默认系统提示词"""
        return f"""你是一位 {self.role.value}，名字叫 {self.name}。
你的职责是：{self.description}
你必须在安全限制下工作，不要执行高风险操作。
"""

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行任务（子类必须实现）
        
        Args:
            task: 任务描述
            
        Returns:
            执行结果
        """
        pass

    def send_message(self, message: AgentMessage):
        """发送消息"""
        self.memory.add_message(message)

    def receive_message(self, message: AgentMessage):
        """接收消息"""
        self.memory.add_message(message)

    def get_tools(self) -> Dict[str, Any]:
        """获取可用工具"""
        if not self.toolkit:
            return {}
            
        tools = {}
        
        # 基础文件操作（安全）
        tools["read_file"] = self.toolkit.file_tools.read_file
        tools["list_directory"] = self.toolkit.file_tools.list_directory
        
        # 文件编辑（需要注意）
        tools["write_file"] = self.toolkit.file_tools.write_file
        tools["read_with_lines"] = self.toolkit.file_editor.read_with_line_numbers
        
        # 项目生成
        if self.role in [AgentRole.TEAM_LEAD, AgentRole.DEV_LEAD, AgentRole.TECHNICAL_ARCHITECT]:
            tools["generate_project"] = self.toolkit._generate_project_safe
        
        return tools

    def use_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """
        使用工具（带安全检查）
        
        Args:
            tool_name: 工具名称
            *args: 参数
            **kwargs: 关键字参数
            
        Returns:
            工具执行结果
        """
        tools = self.get_tools()
        
        if tool_name not in tools:
            return {
                "success": False,
                "error": f"工具不存在或不允许使用: {tool_name}"
            }
        
        # 记录使用
        self.tool_usage_log.append({
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "args": args,
            "kwargs": kwargs
        })
        
        # 执行工具
        try:
            tool = tools[tool_name]
            result = tool(*args, **kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_workspace_info(self) -> Dict[str, Any]:
        """获取工作空间信息"""
        if not self.toolkit:
            return {"status": "no_toolkits"}
        
        try:
            result = self.toolkit.file_tools.get_project_tree()
            if result.success:
                return {
                    "status": "success",
                    "tree": result.data,
                    "base_dir": self.toolkit.base_directory
                }
            return {"status": "error", "error": result.message}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """获取Agent状态"""
        return {
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "message_count": len(self.memory.short_term),
            "tool_usage_count": len(self.tool_usage_log)
        }

    def __str__(self) -> str:
        return f"[{self.name} ({self.role.value}) - {self.status.value}]"

