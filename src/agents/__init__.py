"""
Agent角色和团队协作 - Hermes Agent Framework
"""

from src.agents.base import (
    ExtendedBaseAgent,
    AgentRole,
    AgentStatus,
    AgentMessage,
    AgentMemory,
)

from src.agents.roles import (
    TeamLeadAgent,
    DevLeadAgent,
    BackendDeveloperAgent,
    TechnicalArchitectAgent,
    create_message,
)

from src.agents.team import AgentTeam, create_default_team

__all__ = [
    # 基础类
    "ExtendedBaseAgent",
    "AgentRole",
    "AgentStatus",
    "AgentMessage",
    "AgentMemory",
    # 角色类
    "TeamLeadAgent",
    "DevLeadAgent",
    "BackendDeveloperAgent",
    "TechnicalArchitectAgent",
    "create_message",
    # 团队管理
    "AgentTeam",
    "create_default_team",
]

