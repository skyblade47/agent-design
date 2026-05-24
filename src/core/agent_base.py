"""
Base Agent class for Hermes Agent Framework.
所有Agent的基类，提供通用功能。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Agent配置"""
    name: str = Field(..., description="Agent名称")
    role: str = Field(..., description="Agent角色")
    system_prompt: str = Field(..., description="系统提示词")
    description: Optional[str] = Field(None, description="Agent描述")
    tools: Optional[List[Any]] = Field(default_factory=list, description="可用工具")


class AgentMessage(BaseModel):
    """Agent间消息"""
    message_id: str = Field(..., description="消息ID")
    from_agent: str = Field(..., description="发送者")
    to_agent: Optional[str] = Field(None, description="接收者")
    content: str = Field(..., description="消息内容")
    timestamp: str = Field(..., description="时间戳")
    message_type: str = Field(default="text", description="消息类型")
    artifacts: Optional[List[Dict]] = Field(default_factory=list, description="附件")


class BaseAgent(ABC):
    """
    基础Agent类，所有具体Agent的基类
    """
    
    def __init__(
        self,
        config: AgentConfig,
        llm: BaseLanguageModel,
    ):
        self.config = config
        self.llm = llm
        self.name = config.name
        self.role = config.role
        self.memory: List[AgentMessage] = []
        
    @abstractmethod
    async def execute(self, input_data: Any, **kwargs) -> Any:
        """
        执行Agent的核心逻辑，子类必须实现
        
        Args:
            input_data: 输入数据
            **kwargs: 其他参数
            
        Returns:
            执行结果
        """
        pass
        
    def add_to_memory(self, message: AgentMessage) -> None:
        """
        添加消息到记忆
        
        Args:
            message: 要添加的消息
        """
        self.memory.append(message)
        
    def get_memory(self, limit: Optional[int] = None) -> List[AgentMessage]:
        """
        获取记忆
        
        Args:
            limit: 返回消息数量限制
            
        Returns:
            记忆列表
        """
        if limit:
            return self.memory[-limit:]
        return self.memory
        
    def clear_memory(self) -> None:
        """清空记忆"""
        self.memory = []
        
    async def _call_llm(self, prompt: str, **kwargs) -> str:
        """
        内部方法：调用LLM
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            LLM响应
        """
        messages = ChatPromptTemplate.from_messages([
            ("system", self.config.system_prompt),
            ("human", prompt)
        ])
        
        chain = messages | self.llm
        response = await chain.ainvoke({})
        return str(response.content)
        
    def __repr__(self) -> str:
        return f"<BaseAgent {self.name} ({self.role})>"

