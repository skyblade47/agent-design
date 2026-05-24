"""
Agent团队协作系统 - Hermes Agent Framework
处理多个Agent之间的协作和任务分配
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

from src.agents.base import ExtendedBaseAgent, AgentStatus, AgentMessage
from src.agents.roles import (
    TeamLeadAgent,
    DevLeadAgent,
    BackendDeveloperAgent,
    TechnicalArchitectAgent,
)
from src.tools import HermesToolkit


class AgentTeam:
    """
    Agent团队管理器
    负责Agent的注册、任务分配和协作协调
    """

    def __init__(self, name: str, toolkit: HermesToolkit):
        self.name = name
        self.toolkit = toolkit
        self.agents: Dict[str, ExtendedBaseAgent] = {}
        self.task_queue: List[Dict] = []
        self.task_history: List[Dict] = []

    def register_agent(self, agent: ExtendedBaseAgent):
        """注册Agent到团队"""
        self.agents[agent.name] = agent
        print(f"✅ Agent 已注册: {agent.name} ({agent.role.value})")

    def get_agent(self, name: str) -> Optional[ExtendedBaseAgent]:
        """获取Agent"""
        return self.agents.get(name)

    def get_agents_by_role(self, role) -> List[ExtendedBaseAgent]:
        """根据角色获取Agent"""
        return [agent for agent in self.agents.values() if agent.role == role]

    async def assign_task(
        self,
        task: Dict[str, Any],
        target_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分配任务
        
        Args:
            task: 任务描述
            target_agent: 目标Agent名称（可选，自动选择）
            
        Returns:
            执行结果
        """
        # 选择目标Agent
        agent = None
        
        if target_agent:
            agent = self.get_agent(target_agent)
        elif "target_role" in task:
            # 根据角色选择
            agents = self.get_agents_by_role(task["target_role"])
            if agents:
                agent = agents[0]  # 选择第一个
        
        if not agent:
            return {
                "success": False,
                "error": f"无法找到合适的Agent来执行任务: {task}"
            }
        
        print(f"📋 任务分配给: {agent.name}")
        
        # 执行任务
        result = await agent.execute_task(task)
        
        # 记录历史
        self.task_history.append({
            "task": task,
            "agent": agent.name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result

    async def run_workflow(self, workflow: List[Dict]) -> List[Dict]:
        """
        执行工作流（一系列任务）
        
        Args:
            workflow: 任务列表
            
        Returns:
            所有任务的结果
        """
        results = []
        
        for task in workflow:
            print(f"\n{'='*60}")
            print(f"执行任务: {task.get('type', 'unknown')}")
            print(f"{'='*60}")
            
            result = await self.assign_task(task)
            results.append(result)
            
            print(f"结果: {'✅ 成功' if result.get('success') else '❌ 失败'}")
            if "message" in result:
                print(f"消息: {result['message']}")
        
        return results

    def get_status(self) -> Dict[str, Any]:
        """获取团队状态"""
        agent_statuses = {}
        for name, agent in self.agents.items():
            agent_statuses[name] = agent.get_status()
        
        return {
            "team_name": self.name,
            "agent_count": len(self.agents),
            "agents": agent_statuses,
            "task_history_count": len(self.task_history)
        }


def create_default_team(
    team_name: str,
    toolkit: HermesToolkit,
    project_name: str = "default_project"
) -> AgentTeam:
    """
    创建默认Agent团队
    
    Args:
        team_name: 团队名称
        toolkit: 工具集
        project_name: 项目名称
        
    Returns:
        AgentTeam实例
    """
    team = AgentTeam(team_name, toolkit)
    
    # 创建核心Agent
    team_lead = TeamLeadAgent(
        name="Alice",
        toolkit=toolkit,
        description="负责整体项目规划和协调"
    )
    team.register_agent(team_lead)
    
    dev_lead = DevLeadAgent(
        name="Bob",
        toolkit=toolkit,
        project_name=project_name,
        description="负责项目技术管理和开发指导"
    )
    team.register_agent(dev_lead)
    
    backend_dev = BackendDeveloperAgent(
        name="Charlie",
        toolkit=toolkit,
        description="负责后端开发和API设计"
    )
    team.register_agent(backend_dev)
    
    architect = TechnicalArchitectAgent(
        name="Diana",
        toolkit=toolkit,
        description="负责技术架构和代码审查"
    )
    team.register_agent(architect)
    
    # 注册DevLead到TeamLead
    team_lead.register_dev_lead(dev_lead)
    
    return team

