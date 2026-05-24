"""
PowerShell执行工具 - Hermes Agent Framework
提供安全的PowerShell命令执行，带有严格的安全限制
"""

import subprocess
import threading
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum


class CommandRiskLevel(Enum):
    """命令风险等级"""
    SAFE = "safe"  # 完全安全
    LOW = "low"    # 低风险
    MEDIUM = "medium"  # 中等风险，需要审批
    HIGH = "high"  # 高风险，禁止
    CRITICAL = "critical"  # 严重风险，立即阻止


@dataclass
class CommandExecutionResult:
    """命令执行结果"""
    success: bool
    command: str
    stdout: str
    stderr: str
    return_code: int
    execution_time: float
    risk_level: CommandRiskLevel
    was_allowed: bool
    blocked_reason: Optional[str] = None


class PowerShellSecurityPolicy:
    """
    PowerShell安全策略
    定义哪些命令可以执行，哪些需要审批，哪些禁止
    """
    
    # 完全安全的命令（白名单）
    SAFE_COMMANDS = [
        "Get-ChildItem", "ls", "dir",
        "Get-Content", "cat", "type",
        "Select-String",
        "Write-Host", "echo",
        "Get-Date",
        "Get-Location", "pwd",
        "Test-Path",
        "Get-Command",
        "Get-Help",
    ]
    
    # 低风险命令（允许执行）
    LOW_RISK_COMMANDS = [
        "python", "pip",
        "node", "npm",
        "git",
        "docker-compose",
    ]
    
    # 需要审批的中等风险命令
    MEDIUM_RISK_COMMANDS = [
        "Remove-Item", "del", "rm",
        "New-Item", "mkdir",
        "Set-Content",
        "Copy-Item", "cp",
        "Move-Item", "mv",
        "Rename-Item", "ren",
        "docker",
    ]
    
    # 禁止的高危命令模式
    DANGEROUS_PATTERNS = [
        r"Format-\w+",  # 格式化命令
        r"Remove-Item.*-Recurse.*-Force",  # 强制递归删除
        r"Clear-Disk",  # 清空磁盘
        r"Set-Partition",  # 分区操作
        r"Invoke-Expression", "iex",  # 表达式执行
        r"Invoke-Command.*-ComputerName",  # 远程命令
        r"Start-Process",  # 启动进程
        r"netsh",  # 网络配置
        r"reg",  # 注册表操作
        r"powershell.*-ExecutionPolicy",  # 修改执行策略
        r"Add-Type",  # 编译C#代码
        r"[System.Diagnostics.Process]::Start",  # 启动进程
    ]
    
    # 禁止的参数
    FORBIDDEN_PARAMETERS = [
        "-Recurse", "-Force",
        "/F", "/Q", "/R",
    ]
    
    @classmethod
    def assess_risk(cls, command: str) -> tuple[CommandRiskLevel, Optional[str]]:
        """
        评估命令的风险等级
        
        Args:
            command: PowerShell命令
            
        Returns:
            (风险等级, 阻止原因（如果有）)
        """
        cmd_lower = command.lower()
        
        # 检查危险模式
        for pattern in cls.DANGEROUS_PATTERNS:
            if cls._matches_pattern(cmd_lower, pattern):
                return CommandRiskLevel.CRITICAL, f"命令匹配危险模式: {pattern}"
        
        # 检查禁止的参数
        for param in cls.FORBIDDEN_PARAMETERS:
            if param.lower() in cmd_lower:
                return CommandRiskLevel.HIGH, f"包含禁止的参数: {param}"
        
        # 检查安全命令
        if cls._is_safe_command(command):
            return CommandRiskLevel.SAFE, None
            
        # 检查低风险命令
        if cls._is_low_risk_command(command):
            return CommandRiskLevel.LOW, None
            
        # 检查中等风险命令
        if cls._is_medium_risk_command(command):
            return CommandRiskLevel.MEDIUM, None
            
        # 默认：中等风险（谨慎处理）
        return CommandRiskLevel.MEDIUM, "未识别的命令"
    
    @classmethod
    def _matches_pattern(cls, cmd_lower: str, pattern: str) -> bool:
        """检查命令是否匹配模式"""
        import re
        try:
            return bool(re.search(pattern, cmd_lower))
        except:
            return pattern.lower() in cmd_lower
    
    @classmethod
    def _is_safe_command(cls, command: str) -> bool:
        """检查是否是安全命令"""
        cmd_base = command.strip().split()[0] if command.strip() else ""
        return cmd_base.lower() in [safe.lower() for safe in cls.SAFE_COMMANDS]
    
    @classmethod
    def _is_low_risk_command(cls, command: str) -> bool:
        """检查是否是低风险命令"""
        cmd_base = command.strip().split()[0] if command.strip() else ""
        return cmd_base.lower() in [low.lower() for low in cls.LOW_RISK_COMMANDS]
    
    @classmethod
    def _is_medium_risk_command(cls, command: str) -> bool:
        """检查是否是中等风险命令"""
        cmd_base = command.strip().split()[0] if command.strip() else ""
        return cmd_base.lower() in [med.lower() for med in cls.MEDIUM_RISK_COMMANDS]


class PowerShellExecutor:
    """
    PowerShell执行器
    提供安全的PowerShell命令执行功能
    """
    
    def __init__(
        self,
        working_dir: Optional[str] = None,
        timeout: int = 30,  # 超时时间（秒）
        require_approval_for_medium_risk: bool = True
    ):
        self.working_dir = working_dir
        self.timeout = timeout
        self.require_approval_for_medium_risk = require_approval_for_medium_risk
        self.security_policy = PowerShellSecurityPolicy()
        self.execution_history: List[CommandExecutionResult] = []
    
    def execute(
        self,
        command: str,
        require_approval: Optional[bool] = None,
        approval_callback: Optional[Callable[[str], bool]] = None
    ) -> CommandExecutionResult:
        """
        执行PowerShell命令
        
        Args:
            command: 要执行的命令
            require_approval: 是否需要审批（覆盖默认设置）
            approval_callback: 审批回调函数
            
        Returns:
            执行结果
        """
        start_time = time.time()
        
        # 评估风险
        risk_level, block_reason = self.security_policy.assess_risk(command)
        
        # 决定是否需要审批
        needs_approval = require_approval
        if needs_approval is None:
            if risk_level == CommandRiskLevel.MEDIUM and self.require_approval_for_medium_risk:
                needs_approval = True
            elif risk_level in [CommandRiskLevel.HIGH, CommandRiskLevel.CRITICAL]:
                needs_approval = True
            else:
                needs_approval = False
        
        # 检查是否被阻止
        if risk_level in [CommandRiskLevel.HIGH, CommandRiskLevel.CRITICAL]:
            result = CommandExecutionResult(
                success=False,
                command=command,
                stdout="",
                stderr=block_reason or "命令被安全策略阻止",
                return_code=-1,
                execution_time=time.time() - start_time,
                risk_level=risk_level,
                was_allowed=False,
                blocked_reason=block_reason
            )
            self.execution_history.append(result)
            return result
        
        # 审批流程
        if needs_approval:
            if approval_callback is None or not approval_callback(command):
                result = CommandExecutionResult(
                    success=False,
                    command=command,
                    stdout="",
                    stderr=f"需要人工审批: {command}",
                    return_code=-1,
                    execution_time=time.time() - start_time,
                    risk_level=risk_level,
                    was_allowed=False,
                    blocked_reason="需要人工审批"
                )
                self.execution_history.append(result)
                return result
        
        # 执行命令
        return self._execute_command(command, risk_level, start_time)
    
    def _execute_command(
        self,
        command: str,
        risk_level: CommandRiskLevel,
        start_time: float
    ) -> CommandExecutionResult:
        """实际执行命令"""
        try:
            # 构建PowerShell命令
            full_command = ["powershell", "-Command", command]
            
            # 执行
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=self.working_dir,
                timeout=self.timeout
            )
            
            execution_result = CommandExecutionResult(
                success=result.returncode == 0,
                command=command,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                execution_time=time.time() - start_time,
                risk_level=risk_level,
                was_allowed=True
            )
            
            self.execution_history.append(execution_result)
            return execution_result
            
        except subprocess.TimeoutExpired:
            return CommandExecutionResult(
                success=False,
                command=command,
                stdout="",
                stderr=f"命令执行超时 ({self.timeout}秒)",
                return_code=-1,
                execution_time=time.time() - start_time,
                risk_level=risk_level,
                was_allowed=True,
                blocked_reason="执行超时"
            )
        except Exception as e:
            return CommandExecutionResult(
                success=False,
                command=command,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=time.time() - start_time,
                risk_level=risk_level,
                was_allowed=True,
                blocked_reason=str(e)
            )
    
    def get_history(self, limit: int = 10) -> List[CommandExecutionResult]:
        """获取执行历史"""
        return self.execution_history[-limit:]

