"""
Team Lead / Orchestrator - 主编排器
基于agent-design v2.0双层架构的核心编排器
"""

from typing import Any, Dict, List, Optional
from langchain_core.language_models import BaseLanguageModel
from .agent_base import BaseAgent, AgentConfig, AgentMessage
from datetime import datetime
import uuid


class OrchestratorConfig:
    """编排器配置"""
    def __init__(
        self,
        enable_batch_reporting: bool = True,
        batch_reporting_timeout: int = 300,  # 5分钟
        enable_spawn_approval: bool = True,
        enable_async_sorting: bool = True,
    ):
        self.enable_batch_reporting = enable_batch_reporting
        self.batch_reporting_timeout = batch_reporting_timeout
        self.enable_spawn_approval = enable_spawn_approval
        self.enable_async_sorting = enable_async_sorting


class Orchestrator(BaseAgent):
    """
    Team Lead 编排器
    负责跨项目协调、资源分配、全局决策
    """
    
    def __init__(
        self,
        config: AgentConfig,
        llm: BaseLanguageModel,
        orchestrator_config: Optional[OrchestratorConfig] = None,
    ):
        super().__init__(config, llm)
        self.orchestrator_config = orchestrator_config or OrchestratorConfig()
        self.dev_leads: Dict[str, BaseAgent] = {}  # Dev Lead映射
        self.pending_tasks: List[Dict] = []
        self.completed_tasks: List[Dict] = []
        
    def register_dev_lead(self, project_id: str, dev_lead: BaseAgent) -> None:
        """
        注册Dev Lead到项目
        
        Args:
            project_id: 项目ID
            dev_lead: Dev Lead Agent
        """
        self.dev_leads[project_id] = dev_lead
        self._log(f"Registered Dev Lead for project {project_id}: {dev_lead.name}")
        
    async def execute(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        执行编排逻辑
        
        Args:
            input_data: 包含任务信息的字典
                - project_id: 项目ID
                - task: 任务描述
                - requirements: 需求详情
                
        Returns:
            执行结果
        """
        project_id = input_data.get("project_id")
        task_description = input_data.get("task", "")
        
        self._log(f"Received task for project {project_id}: {task_description}")
        
        # 1. 分析任务并决定如何处理
        analysis_result = await self._analyze_task(input_data)
        
        # 2. 路由到对应Dev Lead
        if project_id in self.dev_leads:
            dev_lead = self.dev_leads[project_id]
            result = await self._route_to_dev_lead(dev_lead, input_data)
            return result
        else:
            # 新项目，需要创建Dev Lead
            if self.orchestrator_config.enable_spawn_approval:
                # 等待用户审批
                return {
                    "status": "approval_required",
                    "message": f"Need approval to spawn Dev Lead for new project: {project_id}",
                    "project_id": project_id,
                }
            else:
                # 自动创建（不推荐）
                return {"status": "error", "message": "Auto-spawn not implemented yet"}
    
    async def _analyze_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析任务
        
        Args:
            input_data: 输入数据
            
        Returns:
            分析结果
        """
        prompt = f"""
        分析以下任务，决定如何处理：
        
        任务描述: {input_data.get('task', '')}
        项目ID: {input_data.get('project_id')}
        需求详情: {input_data.get('requirements', '')}
        
        请提供：
        1. 任务优先级
        2. 建议的处理策略
        3. 可能需要的Agent类型
        """
        
        response = await self._call_llm(prompt)
        return {
            "analysis": response,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _route_to_dev_lead(
        self,
        dev_lead: BaseAgent,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        路由任务到Dev Lead
        
        Args:
            dev_lead: Dev Lead Agent
            input_data: 输入数据
            
        Returns:
            处理结果
        """
        self._log(f"Routing task to Dev Lead: {dev_lead.name}")
        
        # 创建任务消息
        task_message = AgentMessage(
            message_id=str(uuid.uuid4()),
            from_agent=self.name,
            to_agent=dev_lead.name,
            content=input_data.get("task", ""),
            timestamp=datetime.now().isoformat(),
            message_type="task_assignment",
            artifacts=[{"type": "requirements", "data": input_data.get("requirements", {})}]
        )
        
        # 发送给Dev Lead
        result = await dev_lead.execute(task_message)
        
        # 记录结果
        self.completed_tasks.append({
            "task_id": task_message.message_id,
            "project_id": input_data.get("project_id"),
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def get_batch_report(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        生成批量汇报
        
        Args:
            project_id: 项目ID（可选，None表示所有项目）
            
        Returns:
            批量汇报
        """
        # 简单实现：返回已完成任务
        if project_id:
            project_tasks = [t for t in self.completed_tasks if t["project_id"] == project_id]
        else:
            project_tasks = self.completed_tasks
            
        return {
            "summary": f"Completed {len(project_tasks)} tasks",
            "tasks": project_tasks,
            "generated_at": datetime.now().isoformat()
        }
    
    def _log(self, message: str) -> None:
        """内部日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [Orchestrator] {message}")

