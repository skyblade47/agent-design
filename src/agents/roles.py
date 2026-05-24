"""
Agent角色实现 - Hermes Agent Framework
包含TeamLead, DevLead等核心角色
"""

from typing import Dict, Any, List
from datetime import datetime
import uuid
import asyncio

from src.agents.base import (
    ExtendedBaseAgent,
    AgentRole,
    AgentStatus,
    AgentMessage,
)
from src.tools import HermesToolkit


class TeamLeadAgent(ExtendedBaseAgent):
    """
    团队负责人Agent
    负责任务分配、跨项目协调、整体进度管理
    """

    def __init__(
        self,
        name: str,
        toolkit: HermesToolkit,
        description: str = "负责整体项目规划、任务分配和团队协调",
    ):
        super().__init__(
            name=name,
            role=AgentRole.TEAM_LEAD,
            toolkit=toolkit,
            description=description
        )
        self.projects: Dict[str, Dict] = {}
        self.dev_leads: Dict[str, ExtendedBaseAgent] = {}

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行团队负责人任务"""
        self.status = AgentStatus.WORKING
        
        task_type = task.get("type", "")
        
        if task_type == "init_project":
            result = await self._init_project(task)
        elif task_type == "assign_task":
            result = await self._assign_task(task)
        elif task_type == "get_status":
            result = await self._get_team_status()
        else:
            result = await self._process_general_task(task)
        
        self.status = AgentStatus.IDLE
        return result

    async def _init_project(self, task: Dict) -> Dict:
        """初始化新项目"""
        project_name = task.get("project_name", "unnamed_project")
        project_type = task.get("project_type", "web_app")
        
        # 创建项目脚手架
        if "generate_project" in self.get_tools():
            result = self.use_tool(
                "generate_project",
                name=project_name,
                description=task.get("description", ""),
                project_type=project_type,
                author=self.name
            )
            
            if result["success"]:
                self.projects[project_name] = {
                    "name": project_name,
                    "type": project_type,
                    "created_at": datetime.now().isoformat(),
                    "status": "initialized",
                    "tasks": []
                }
                
                return {
                    "success": True,
                    "project": project_name,
                    "message": f"项目 {project_name} 初始化成功",
                    "details": result.get("result", {})
                }
        
        return {
            "success": False,
            "error": "项目初始化失败"
        }

    async def _assign_task(self, task: Dict) -> Dict:
        """分配任务"""
        project_name = task.get("project_name")
        target_role = task.get("target_role")
        task_description = task.get("description")
        
        return {
            "success": True,
            "message": f"任务已分配给 {target_role}",
            "task": task_description
        }

    async def _get_team_status(self) -> Dict:
        """获取团队状态"""
        status_report = {
            "team_lead": self.name,
            "projects": list(self.projects.keys()),
            "dev_leads": list(self.dev_leads.keys()),
            "status": self.status.value,
            "tool_usage": len(self.tool_usage_log)
        }
        return {
            "success": True,
            "status": status_report
        }

    async def _process_general_task(self, task: Dict) -> Dict:
        """处理通用任务"""
        return {
            "success": True,
            "message": f"TeamLead 收到任务: {task}",
            "status": "acknowledged"
        }

    def register_dev_lead(self, dev_lead: ExtendedBaseAgent):
        """注册DevLead"""
        self.dev_leads[dev_lead.name] = dev_lead


class DevLeadAgent(ExtendedBaseAgent):
    """
    开发负责人Agent
    负责具体项目的技术管理和任务执行
    """

    def __init__(
        self,
        name: str,
        toolkit: HermesToolkit,
        project_name: str = "",
        description: str = "负责项目技术管理、任务分解和开发指导",
    ):
        super().__init__(
            name=name,
            role=AgentRole.DEV_LEAD,
            toolkit=toolkit,
            description=description
        )
        self.project_name = project_name
        self.team_members: List[ExtendedBaseAgent] = []

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行开发负责人任务"""
        self.status = AgentStatus.WORKING
        
        task_type = task.get("type", "")
        
        if task_type == "analyze_requirements":
            result = await self._analyze_requirements(task)
        elif task_type == "create_file":
            result = await self._create_file(task)
        elif task_type == "list_files":
            result = await self._list_files(task)
        else:
            result = await self._process_general_task(task)
        
        self.status = AgentStatus.IDLE
        return result

    async def _analyze_requirements(self, task: Dict) -> Dict:
        """分析需求"""
        requirements = task.get("requirements", "")
        project_type = task.get("project_type", "web_app")
        
        analysis = {
            "project_type": project_type,
            "requirements_summary": requirements[:200] + "..." if len(requirements) > 200 else requirements,
            "suggested_architecture": "模块化设计",
            "tech_stack": self._suggest_tech_stack(project_type)
        }
        
        return {
            "success": True,
            "analysis": analysis
        }

    async def _create_file(self, task: Dict) -> Dict:
        """创建文件"""
        file_path = task.get("file_path")
        content = task.get("content", "")
        overwrite = task.get("overwrite", False)
        
        result = self.use_tool(
            "write_file",
            file_path=file_path,
            content=content,
            overwrite=overwrite
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"文件 {file_path} 创建成功",
                "file": file_path
            }
        return result

    async def _list_files(self, task: Dict) -> Dict:
        """列出文件"""
        dir_path = task.get("dir_path", ".")
        
        result = self.use_tool("list_directory", dir_path=dir_path)
        
        if result["success"]:
            return {
                "success": True,
                "files": result.get("result", {}).data if hasattr(result.get("result"), 'data') else [],
                "directory": dir_path
            }
        return result

    async def _process_general_task(self, task: Dict) -> Dict:
        """处理通用任务"""
        return {
            "success": True,
            "message": f"DevLead 收到任务: {task}",
            "project": self.project_name
        }

    def _suggest_tech_stack(self, project_type: str) -> List[str]:
        """建议技术栈"""
        stacks = {
            "web_app": ["React", "FastAPI", "PostgreSQL"],
            "python_library": ["Python", "pytest", "setuptools"],
            "full_stack": ["React", "FastAPI", "Docker", "PostgreSQL"],
            "cli": ["Python", "click", "rich"]
        }
        return stacks.get(project_type, ["Python"])


class BackendDeveloperAgent(ExtendedBaseAgent):
    """
    后端开发Agent
    负责后端API和业务逻辑开发
    """

    def __init__(
        self,
        name: str,
        toolkit: HermesToolkit,
        description: str = "负责后端开发、API设计、数据库管理",
    ):
        super().__init__(
            name=name,
            role=AgentRole.BACKEND_DEVELOPER,
            toolkit=toolkit,
            description=description
        )

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行后端开发任务"""
        self.status = AgentStatus.WORKING
        
        task_type = task.get("type", "")
        
        if task_type == "create_endpoint":
            result = await self._create_endpoint(task)
        elif task_type == "create_model":
            result = await self._create_model(task)
        else:
            result = await self._process_general_task(task)
        
        self.status = AgentStatus.IDLE
        return result

    async def _create_endpoint(self, task: Dict) -> Dict:
        """创建API端点"""
        endpoint_name = task.get("endpoint_name", "default")
        file_path = task.get("file_path", f"api/{endpoint_name}.py")
        
        code = f'''"""
{endpoint_name} API Endpoint
"""
from fastapi import APIRouter

router = APIRouter(prefix="/{endpoint_name}")

@router.get("/")
async def get_{endpoint_name}():
    return {{\"message\": \"{endpoint_name} endpoint working\"}}
'''
        
        result = self.use_tool(
            "write_file",
            file_path=file_path,
            content=code
        )
        
        return {
            "success": result.get("success", False),
            "message": f"创建端点 {endpoint_name}",
            "file": file_path,
            "result": result
        }

    async def _create_model(self, task: Dict) -> Dict:
        """创建数据模型"""
        model_name = task.get("model_name", "DefaultModel")
        file_path = task.get("file_path", f"models/{model_name.lower()}.py")
        
        code = f'''"""
{model_name} Data Model
"""
from pydantic import BaseModel
from typing import Optional

class {model_name}(BaseModel):
    id: Optional[int] = None
    name: str
    # 在此添加更多字段
'''
        
        result = self.use_tool(
            "write_file",
            file_path=file_path,
            content=code
        )
        
        return {
            "success": result.get("success", False),
            "message": f"创建模型 {model_name}",
            "file": file_path,
            "result": result
        }

    async def _process_general_task(self, task: Dict) -> Dict:
        """处理通用任务"""
        return {
            "success": True,
            "message": f"Backend Developer 收到任务: {task}"
        }


class TechnicalArchitectAgent(ExtendedBaseAgent):
    """
    技术架构师Agent
    负责架构设计、技术选型、代码审查
    """

    def __init__(
        self,
        name: str,
        toolkit: HermesToolkit,
        description: str = "负责技术架构设计、技术选型和代码审查",
    ):
        super().__init__(
            name=name,
            role=AgentRole.TECHNICAL_ARCHITECT,
            toolkit=toolkit,
            description=description
        )

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行架构师任务"""
        self.status = AgentStatus.WORKING
        
        task_type = task.get("type", "")
        
        if task_type == "design_architecture":
            result = await self._design_architecture(task)
        elif task_type == "code_review":
            result = await self._code_review(task)
        else:
            result = await self._process_general_task(task)
        
        self.status = AgentStatus.IDLE
        return result

    async def _design_architecture(self, task: Dict) -> Dict:
        """设计架构"""
        project_type = task.get("project_type", "web_app")
        
        architecture = {
            "project_type": project_type,
            "layers": ["API", "Service", "Repository", "Database"],
            "recommendations": self._get_architecture_recommendations(project_type),
            "file_structure": self._suggest_file_structure(project_type)
        }
        
        return {
            "success": True,
            "architecture": architecture
        }

    async def _code_review(self, task: Dict) -> Dict:
        """代码审查"""
        file_path = task.get("file_path")
        
        if not file_path:
            return {"success": False, "error": "未指定文件"}
        
        result = self.use_tool("read_file", file_path=file_path)
        
        if result.get("success"):
            # 简单的代码审查
            review = {
                "file": file_path,
                "checked_at": datetime.now().isoformat(),
                "status": "reviewed",
                "comments": ["代码风格良好", "建议添加更多注释", "考虑添加错误处理"]
            }
            return {"success": True, "review": review}
        
        return result

    async def _process_general_task(self, task: Dict) -> Dict:
        return {
            "success": True,
            "message": f"Architect 收到任务: {task}"
        }

    def _get_architecture_recommendations(self, project_type: str) -> List[str]:
        """获取架构建议"""
        if project_type == "web_app":
            return [
                "采用分层架构",
                "RESTful API设计",
                "依赖注入模式",
                "单元测试覆盖核心功能"
            ]
        return ["模块化设计", "清晰的接口定义"]

    def _suggest_file_structure(self, project_type: str) -> List[str]:
        """建议文件结构"""
        if project_type == "web_app":
            return [
                "src/main.py",
                "src/api/",
                "src/models/",
                "src/services/",
                "tests/"
            ]
        return ["src/", "tests/", "docs/"]


def create_message(
    from_agent: str,
    to_agent: str,
    content: str,
    requires_response: bool = False
) -> AgentMessage:
    """创建Agent消息"""
    return AgentMessage(
        message_id=str(uuid.uuid4()),
        sender_agent=from_agent,
        recipient_agent=to_agent,
        content=content,
        requires_response=requires_response
    )

