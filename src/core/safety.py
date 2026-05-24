"""
Agent安全和行为边界控制 - Hermes Agent Framework
确保Agent在安全范围内操作，防止有害行为
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re


class RiskLevel(Enum):
    """风险等级"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SafetyRule:
    """安全规则"""
    name: str
    description: str
    risk_level: RiskLevel
    check_function: Callable[[str], bool]
    mitigation: str


@dataclass
class SafetyCheckResult:
    """安全检查结果"""
    passed: bool
    risk_level: RiskLevel
    message: str
    rule_name: Optional[str] = None


class SafetyGuard:
    """
    Agent安全卫士
    提供行为边界控制和安全检查
    """
    
    def __init__(self):
        self.rules: List[SafetyRule] = []
        self._init_default_rules()
        
    def _init_default_rules(self) -> None:
        """初始化默认安全规则"""
        
        # 禁止的命令模式
        forbidden_commands = [
            r"rm\s+(-rf?|--recursive)",  # 危险删除
            r"mkfs|format",  # 格式化
            r":\(\)\{:|:&}\;",  # fork炸弹
            r"chmod\s+777",  # 过度权限
            r">?\s*/dev/(sd|hd)",  # 直接磁盘操作
            r"dd\s+if=",  # dd命令
            r"wget\s+.*\|\s*(bash|sh)",  # 远程执行
            r"curl\s+.*\|\s*(bash|sh)",
            r"eval\s*\(",  # eval执行
        ]
        
        # 敏感文件模式
        sensitive_files = [
            r"\.ssh/id_rsa",
            r"\.ssh/id_dsa",
            r"\.env",
            r"\.bashrc",
            r"\/etc\/passwd",
            r"\/etc\/shadow",
            r"\/etc\/hosts",
        ]
        
        # 添加规则
        self.add_rule(
            SafetyRule(
                name="禁止危险命令",
                description="检测可能破坏系统的命令",
                risk_level=RiskLevel.CRITICAL,
                check_function=lambda x: any(re.search(p, x, re.IGNORECASE) for p in forbidden_commands),
                mitigation="该操作可能损坏系统，已被阻止"
            )
        )
        
        self.add_rule(
            SafetyRule(
                name="禁止敏感文件操作",
                description="保护敏感文件不被访问",
                risk_level=RiskLevel.HIGH,
                check_function=lambda x: any(re.search(p, x) for p in sensitive_files),
                mitigation="禁止访问敏感文件"
            )
        )
        
    def add_rule(self, rule: SafetyRule) -> None:
        """添加安全规则"""
        self.rules.append(rule)
        
    def check_content(self, content: str) -> SafetyCheckResult:
        """
        检查内容是否违反安全规则
        
        Args:
            content: 要检查的内容
            
        Returns:
            SafetyCheckResult
        """
        if not content:
            return SafetyCheckResult(
                passed=True,
                risk_level=RiskLevel.SAFE,
                message="内容为空，无需检查"
            )
            
        for rule in self.rules:
            try:
                if rule.check_function(content):
                    return SafetyCheckResult(
                        passed=False,
                        risk_level=rule.risk_level,
                        message=rule.mitigation,
                        rule_name=rule.name
                    )
            except:
                continue
                
        return SafetyCheckResult(
            passed=True,
            risk_level=RiskLevel.SAFE,
            message="内容通过安全检查"
        )
        
    def check_command(self, command: str) -> SafetyCheckResult:
        """
        检查命令是否安全
        
        Args:
            command: 要执行的命令
            
        Returns:
            SafetyCheckResult
        """
        return self.check_content(command)


class AgentBehaviorPolicy:
    """
    Agent行为策略
    定义Agent应该和不应该做的事情
    """
    
    def __init__(self):
        self.allowed_actions: List[str] = []
        self.forbidden_actions: List[str] = []
        self.required_human_approval: List[str] = []
        self._init_default_policy()
        
    def _init_default_policy(self) -> None:
        """初始化默认策略"""
        
        # 允许的操作
        self.allowed_actions = [
            "读取项目文件",
            "创建新文件",
            "修改代码文件",
            "运行单元测试",
            "生成文档",
            "代码审查",
            "架构设计",
        ]
        
        # 需要人工批准的操作
        self.required_human_approval = [
            "删除文件",
            "修改核心配置",
            "运行构建命令",
            "部署到生产环境",
            "安装依赖包",
        ]
        
    def is_allowed(self, action: str) -> tuple[bool, str]:
        """
        检查操作是否允许
        
        Args:
            action: 操作描述
            
        Returns:
            (是否允许, 原因)
        """
        if any(forbidden in action for forbidden in self.forbidden_actions):
            return False, "该操作被策略禁止"
            
        if any(required in action for required in self.required_human_approval):
            return False, "该操作需要人工批准"
            
        return True, "操作允许"
        
    def requires_approval(self, action: str) -> bool:
        """检查操作是否需要人工批准"""
        return any(required in action for required in self.required_human_approval)


class DevelopmentStandards:
    """
    开发规范
    封装专业的软件开发最佳实践
    """
    
    def __init__(self):
        # 代码规范
        self.code_standards = {
            "python": {
                "style": "PEP 8",
                "line_length": 100,
                "type_hints": "required",
                "docstrings": "Google style",
                "test_coverage": ">= 80%",
            },
            "javascript": {
                "style": "ESLint",
                "line_length": 100,
            },
            "typescript": {
                "style": "ESLint",
                "strict": True,
            }
        }
        
        # Git提交规范
        self.git_commit_types = [
            "feat", "fix", "docs", "style", 
            "refactor", "test", "chore", "perf"
        ]
        
    def get_file_naming_convention(self, file_type: str) -> Dict[str, str]:
        """
        获取文件命名规范
        
        Args:
            file_type: 文件类型
            
        Returns:
            命名规范
        """
        conventions = {
            "python": {"case": "snake_case", "suffix": ".py"},
            "react_component": {"case": "PascalCase", "suffix": ".tsx"},
            "react_hook": {"case": "camelCase", "suffix": ".ts", "prefix": "use"},
            "css": {"case": "kebab-case", "suffix": ".css"},
            "test": {"case": "snake_case", "suffix": "_test.py"},
        }
        return conventions.get(file_type, {"case": "snake_case"})
        
    def get_project_structure_guide(self, project_type: str) -> Dict[str, List[str]]:
        """
        获取项目结构指南
        
        Args:
            project_type: 项目类型
            
        Returns:
            目录结构建议
        """
        structures = {
            "python_library": {
                "dirs": ["src", "tests", "docs", "examples"],
                "files": ["README.md", "setup.py", "requirements.txt", ".gitignore"],
            },
            "web_app": {
                "dirs": ["src", "public", "tests", "docs", "scripts"],
                "files": ["README.md", "package.json", ".gitignore"],
            },
            "full_stack": {
                "dirs": ["frontend", "backend", "docs", "deployment"],
                "files": ["README.md", "docker-compose.yml"],
            }
        }
        return structures.get(project_type, structures["web_app"])

