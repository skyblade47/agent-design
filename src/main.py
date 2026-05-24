"""
Hermes Agent Framework - 主入口
简单示例：如何使用框架
"""

import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.core.agent_base import AgentConfig, BaseAgent
from src.core.orchestrator import Orchestrator, OrchestratorConfig


# 加载环境变量
load_dotenv()


class SimpleDevLead(BaseAgent):
    """简单的Dev Lead示例"""
    
    async def execute(self, input_data, **kwargs):
        print(f"[SimpleDevLead] Received task: {input_data.content}")
        
        # 简单响应
        return {
            "status": "completed",
            "message": "Task processed by SimpleDevLead",
            "output": f"Processed: {input_data.content}",
        }


async def main():
    """主函数 - 简单示例"""
    print("=" * 60)
    print("Hermes Agent Framework - 简单示例")
    print("=" * 60)
    
    # 1. 初始化LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # 2. 创建Orchestrator配置
    orchestrator_config = AgentConfig(
        name="Team-Lead",
        role="Orchestrator",
        system_prompt="""
        你是一个团队负责人（Team Lead），负责协调多个项目和Agent。
        你的职责是：
        1. 分析任务并路由到合适的Dev Lead
        2. 跨项目资源协调
        3. 全局决策和审批
        4. 汇总汇报
        """,
        description="主编排器",
    )
    
    # 3. 创建Orchestrator
    orchestrator = Orchestrator(
        config=orchestrator_config,
        llm=llm,
        orchestrator_config=OrchestratorConfig(
            enable_batch_reporting=True,
            enable_spawn_approval=True,
        ),
    )
    
    # 4. 创建并注册Dev Lead
    dev_lead_config = AgentConfig(
        name="Dev-Lead-1",
        role="Dev Lead",
        system_prompt="你是一个项目开发负责人，负责管理具体项目的执行。",
    )
    
    dev_lead = SimpleDevLead(config=dev_lead_config, llm=llm)
    orchestrator.register_dev_lead("project-1", dev_lead)
    
    print("\n✅ 框架初始化完成")
    print(f"  - Orchestrator: {orchestrator.name}")
    print(f"  - 已注册项目: {list(orchestrator.dev_leads.keys())}")
    
    # 5. 示例任务
    print("\n" + "=" * 60)
    print("📝 执行示例任务")
    print("=" * 60)
    
    task_input = {
        "project_id": "project-1",
        "task": "开发一个简单的待办事项Web应用",
        "requirements": {
            "features": ["添加任务", "标记完成", "删除任务"],
            "tech_stack": "React + FastAPI",
        },
    }
    
    print(f"\n任务: {task_input['task']}")
    print(f"项目: {task_input['project_id']}")
    
    # 6. 执行任务
    result = await orchestrator.execute(task_input)
    
    print("\n" + "=" * 60)
    print("📋 执行结果")
    print("=" * 60)
    print(f"状态: {result.get('status')}")
    print(f"消息: {result.get('message')}")
    
    # 7. 获取批量汇报
    print("\n" + "=" * 60)
    print("📊 批量汇报")
    print("=" * 60)
    report = orchestrator.get_batch_report("project-1")
    print(f"摘要: {report['summary']}")
    print(f"任务数: {len(report['tasks'])}")


if __name__ == "__main__":
    asyncio.run(main())

