"""
增强的文件编辑工具 - Hermes Agent Framework
提供专业的文件编辑功能，支持行级编辑、插入、替换等操作
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from .file_tools import FileTools, FileOperationResult


@dataclass
class LineRange:
    """行范围"""
    start: int
    end: int  # 包含此行


class EnhancedFileEditor:
    """
    增强的文件编辑器
    提供行级编辑、安全检查等高级功能
    """
    
    def __init__(self, file_tools: FileTools):
        self.file_tools = file_tools
    
    def read_with_line_numbers(self, file_path: str) -> FileOperationResult:
        """
        读取文件并显示行号
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含行号的内容
        """
        result = self.file_tools.read_file(file_path)
        if not result.success:
            return result
            
        lines = result.data.splitlines()
        numbered_content = []
        for i, line in enumerate(lines, 1):
            numbered_content.append(f"{i:4d}: {line}")
            
        result.data = {
            "raw_content": result.data,
            "lines": lines,
            "numbered_content": "\n".join(numbered_content)
        }
        return result
    
    def insert_text(
        self,
        file_path: str,
        text: str,
        line_number: int,  # 在第line_number行之前插入
        create_missing: bool = False
    ) -> FileOperationResult:
        """
        在指定位置插入文本
        
        Args:
            file_path: 文件路径
            text: 要插入的文本
            line_number: 行号（从1开始）
            create_missing: 如果文件不存在是否创建
            
        Returns:
            操作结果
        """
        # 读取现有内容
        if self.file_tools.file_exists(file_path):
            read_result = self.file_tools.read_file(file_path)
            if not read_result.success:
                return read_result
            lines = read_result.data.splitlines(keepends=True)
        elif create_missing:
            lines = []
        else:
            return FileOperationResult(False, f"文件不存在: {file_path}")
            
        # 验证行号
        if line_number < 1 or line_number > len(lines) + 1:
            return FileOperationResult(
                False,
                f"行号超出范围: {line_number} (文件共 {len(lines)} 行)"
            )
            
        # 插入
        insert_lines = text.splitlines(keepends=True)
        if insert_lines and not insert_lines[-1].endswith('\n'):
            insert_lines[-1] += '\n'
            
        lines[line_number-1:line_number-1] = insert_lines
        
        # 写回
        content = ''.join(lines)
        return self.file_tools.write_file(file_path, content, overwrite=True)
    
    def replace_text(
        self,
        file_path: str,
        old_text: str,
        new_text: str,
        count: int = -1  # -1表示替换所有
    ) -> FileOperationResult:
        """
        替换文本
        
        Args:
            file_path: 文件路径
            old_text: 要替换的文本
            new_text: 新文本
            count: 替换次数
            
        Returns:
            操作结果
        """
        read_result = self.file_tools.read_file(file_path)
        if not read_result.success:
            return read_result
            
        content = read_result.data
        
        if old_text not in content:
            return FileOperationResult(
                False,
                f"未找到要替换的文本"
            )
            
        # 执行替换
        if count == -1:
            new_content = content.replace(old_text, new_text)
        else:
            new_content = content.replace(old_text, new_text, count)
            
        return self.file_tools.write_file(file_path, new_content, overwrite=True)
    
    def replace_lines(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        new_text: str
    ) -> FileOperationResult:
        """
        替换指定行数范围的内容
        
        Args:
            file_path: 文件路径
            start_line: 起始行
            end_line: 结束行
            new_text: 新文本
            
        Returns:
            操作结果
        """
        read_result = self.file_tools.read_file(file_path)
        if not read_result.success:
            return read_result
            
        lines = read_result.data.splitlines(keepends=True)
        
        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            return FileOperationResult(
                False,
                f"行范围无效: {start_line}-{end_line} (文件共 {len(lines)} 行)"
            )
            
        # 替换
        new_lines = new_text.splitlines(keepends=True)
        if new_lines and not new_lines[-1].endswith('\n'):
            new_lines[-1] += '\n'
            
        lines[start_line-1:end_line] = new_lines
        content = ''.join(lines)
        
        return self.file_tools.write_file(file_path, content, overwrite=True)
    
    def append_text(
        self,
        file_path: str,
        text: str,
        create_missing: bool = True
    ) -> FileOperationResult:
        """
        在文件末尾追加文本
        
        Args:
            file_path: 文件路径
            text: 要追加的文本
            create_missing: 是否创建不存在的文件
            
        Returns:
            操作结果
        """
        if self.file_tools.file_exists(file_path):
            read_result = self.file_tools.read_file(file_path)
            if not read_result.success:
                return read_result
            content = read_result.data
        elif create_missing:
            content = ""
        else:
            return FileOperationResult(False, f"文件不存在: {file_path}")
            
        if not content.endswith('\n') and content:
            content += '\n'
            
        content += text
        
        return self.file_tools.write_file(file_path, content, overwrite=True)
    
    def search_text(
        self,
        file_path: str,
        search_pattern: str,
        case_sensitive: bool = False
    ) -> FileOperationResult:
        """
        在文件中搜索文本
        
        Args:
            file_path: 文件路径
            search_pattern: 搜索模式
            case_sensitive: 是否区分大小写
            
        Returns:
            匹配结果
        """
        read_result = self.file_tools.read_file(file_path)
        if not read_result.success:
            return read_result
            
        lines = read_result.data.splitlines()
        matches = []
        
        for i, line in enumerate(lines, 1):
            line_to_check = line
            pattern_to_check = search_pattern
            
            if not case_sensitive:
                line_to_check = line.lower()
                pattern_to_check = search_pattern.lower()
                
            if pattern_to_check in line_to_check:
                matches.append({
                    "line_number": i,
                    "content": line,
                    "index": line_to_check.find(pattern_to_check)
                })
                
        return FileOperationResult(
            True,
            f"找到 {len(matches)} 个匹配",
            data={
                "matches": matches,
                "total": len(matches)
            }
        )

