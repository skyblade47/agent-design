"""
项目脚手架生成器 - Hermes Agent Framework
封装了专业的项目创建知识，快速生成标准化的项目结构
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str
    description: str
    project_type: str  # "web_app", "python_library", "full_stack", "cli"
    author: str
    use_docker: bool = True
    use_tests: bool = True
    use_ci: bool = True


class ProjectScaffoldGenerator:
    """
    项目脚手架生成器
    包含各种项目类型的标准结构和文件模板
    """
    
    def __init__(self, file_tools):
        """
        初始化生成器
        
        Args:
            file_tools: FileTools实例用于文件操作
        """
        self.file_tools = file_tools
        
    def get_project_template(self, project_type: str) -> Dict[str, Any]:
        """
        获取项目模板配置
        
        Args:
            project_type: 项目类型
            
        Returns:
            模板配置
        """
        templates = {
            "python_library": self._python_library_template(),
            "web_app": self._web_app_template(),
            "full_stack": self._full_stack_template(),
            "cli": self._cli_template(),
        }
        return templates.get(project_type, templates["web_app"])
        
    def _python_library_template(self) -> Dict[str, Any]:
        """Python库模板"""
        return {
            "directories": [
                "src/{{project_name}}",
                "tests",
                "docs",
                "examples",
            ],
            "files": [
                {
                    "path": "README.md",
                    "content": self._readme_template
                },
                {
                    "path": "pyproject.toml",
                    "content": self._pyproject_template
                },
                {
                    "path": "requirements.txt",
                    "content": self._python_requirements_template
                },
                {
                    "path": "tests/__init__.py",
                    "content": '"""Tests package."""\n'
                },
                {
                    "path": "src/{{project_name}}/__init__.py",
                    "content": self._package_init_template
                },
                {
                    "path": ".gitignore",
                    "content": self._python_gitignore_template
                },
            ]
        }
        
    def _web_app_template(self) -> Dict[str, Any]:
        """Web应用模板（React + FastAPI）"""
        return {
            "directories": [
                "frontend/src",
                "frontend/public",
                "backend/app",
                "backend/tests",
                "docs",
                "deployment",
            ],
            "files": [
                {
                    "path": "README.md",
                    "content": self._readme_template
                },
                {
                    "path": "docker-compose.yml",
                    "content": self._docker_compose_template
                },
                {
                    "path": "frontend/package.json",
                    "content": self._frontend_package_template
                },
                {
                    "path": "backend/requirements.txt",
                    "content": self._backend_requirements_template
                },
                {
                    "path": "backend/app/main.py",
                    "content": self._fastapi_main_template
                },
                {
                    "path": ".gitignore",
                    "content": self._full_stack_gitignore_template
                },
            ]
        }
        
    def _full_stack_template(self) -> Dict[str, Any]:
        """全栈模板"""
        return self._web_app_template()
        
    def _cli_template(self) -> Dict[str, Any]:
        """命令行工具模板"""
        return {
            "directories": [
                "src/{{project_name}}",
                "tests",
                "docs",
            ],
            "files": [
                {
                    "path": "README.md",
                    "content": self._readme_template
                },
                {
                    "path": "pyproject.toml",
                    "content": self._cli_pyproject_template
                },
                {
                    "path": "src/{{project_name}}/cli.py",
                    "content": self._cli_entrypoint_template
                },
                {
                    "path": ".gitignore",
                    "content": self._python_gitignore_template
                },
            ]
        }
        
    # 模板内容
    def _readme_template(self, config: ProjectConfig) -> str:
        """README模板"""
        return f"""# {config.name}

{config.description}

## 快速开始

### 安装

```bash
# 查看具体安装说明
```

## 使用

```python
# 示例代码
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 作者

{config.author}

## 许可证

MIT License
"""
        
    def _pyproject_template(self, config: ProjectConfig) -> str:
        """pyproject.toml模板"""
        return f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{config.name}"
description = "{config.description}"
version = "0.1.0"
authors = [
  {{ name = "{config.author}" }}
]
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = [
  "pytest>=7.0",
  "pytest-cov>=4.0",
  "black>=23.0",
  "isort>=5.12",
  "mypy>=1.0",
]
"""
        
    def _python_requirements_template(self, config: ProjectConfig) -> str:
        """Python requirements模板"""
        return """# Core dependencies
# Add your dependencies here

# Development dependencies
pytest>=7.0
pytest-cov>=4.0
black>=23.0
isort>=5.12
mypy>=1.0
"""
        
    def _package_init_template(self, config: ProjectConfig) -> str:
        """包初始化模板"""
        return f'''"""
{config.name}

{config.description}
"""

__version__ = "0.1.0"
__author__ = "{config.author}"
'''
        
    def _python_gitignore_template(self, config: ProjectConfig) -> str:
        """Python .gitignore模板"""
        return """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
ENV/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.dmypy.json
dmypy.json
"""
        
    def _docker_compose_template(self, config: ProjectConfig) -> str:
        """Docker Compose模板"""
        return f"""version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=True

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
"""
        
    def _frontend_package_template(self, config: ProjectConfig) -> str:
        """前端package.json模板"""
        return f'{{\n  "name": "{config.name}-frontend",\n  "version": "0.1.0",\n  "private": true,\n  "dependencies": {{\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0"\n  }},\n  "scripts": {{\n    "dev": "vite",\n    "build": "vite build",\n    "preview": "vite preview"\n  }}\n}}\n'
        
    def _backend_requirements_template(self, config: ProjectConfig) -> str:
        """后端requirements模板"""
        return """fastapi>=0.100.0
uvicorn[standard]>=0.20.0
pydantic>=2.0.0
python-multipart>=0.0.6

# Development
pytest>=7.0
httpx>=0.24.0
"""
        
    def _fastapi_main_template(self, config: ProjectConfig) -> str:
        """FastAPI主文件模板"""
        return f'''"""
{config.name} Backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{config.name}",
    description="{config.description}",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {{"message": "Welcome to {config.name}!"}}


@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
    def _full_stack_gitignore_template(self, config: ProjectConfig) -> str:
        """全栈.gitignore模板"""
        return self._python_gitignore_template(config) + """
# Frontend
node_modules/
dist/
.next/
.vite/

# Docker
.dockerignore
"""
        
    def _cli_pyproject_template(self, config: ProjectConfig) -> str:
        """CLI项目pyproject模板"""
        return f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{config.name}"
description = "{config.description}"
version = "0.1.0"
authors = [
  {{ name = "{config.author}" }}
]
requires-python = ">=3.9"
dependencies = [
  "click>=8.0",
]

[project.scripts]
{config.name.replace('-', '_')} = "{config.name.replace('-', '_')}.cli:cli"

[project.optional-dependencies]
dev = [
  "pytest>=7.0",
  "black>=23.0",
]
"""
        
    def _cli_entrypoint_template(self, config: ProjectConfig) -> str:
        """CLI入口点模板"""
        return f'''"""
{config.name} CLI
"""

import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """{config.description}"""
    pass


@cli.command()
@click.option("--name", default="World", help="Name to greet")
def hello(name: str):
    """Say hello"""
    click.echo(f"Hello, {{name}}!")


if __name__ == "__main__":
    cli()
'''
        
    def generate_project(self, config: ProjectConfig) -> Dict[str, Any]:
        """
        生成完整项目结构
        
        Args:
            config: 项目配置
            
        Returns:
            生成结果
        """
        results = {
            "success": True,
            "files_created": [],
            "errors": [],
        }
        
        try:
            # 创建项目基础目录
            project_dir = config.name
            self.file_tools.create_directory(project_dir)
            
            # 获取模板
            template = self.get_project_template(config.project_type)
            
            # 创建目录
            for dir_path in template["directories"]:
                # 替换模板变量
                processed_path = dir_path.replace("{{project_name}}", config.name)
                full_path = f"{project_dir}/{processed_path}"
                result = self.file_tools.create_directory(full_path)
                if not result.success:
                    results["errors"].append(result.message)
                    
            # 创建文件
            for file_info in template["files"]:
                try:
                    # 替换模板变量
                    file_path = file_info["path"].replace("{{project_name}}", config.name)
                    full_path = f"{project_dir}/{file_path}"
                    
                    # 生成内容
                    content_generator = file_info["content"]
                    content = content_generator(config) if callable(content_generator) else content_generator
                    
                    # 写入文件
                    result = self.file_tools.write_file(full_path, content, overwrite=False)
                    
                    if result.success:
                        results["files_created"].append(full_path)
                    else:
                        results["errors"].append(result.message)
                        
                except Exception as e:
                    results["errors"].append(f"Error creating {file_info['path']}: {str(e)}")
                    
            # 创建HERMES项目配置文件
            hermes_config = {
                "project_name": config.name,
                "project_type": config.project_type,
                "created_at": datetime.now().isoformat(),
                "agents": {
                    "backend_developer": {"enabled": True},
                    "frontend_developer": {"enabled": config.project_type in ["web_app", "full_stack"]},
                    "devops": {"enabled": config.use_docker},
                }
            }
            
            config_result = self.file_tools.write_file(
                f"{project_dir}/.hermes/config.json",
                json.dumps(hermes_config, indent=2)
            )
            
            if config_result.success:
                results["files_created"].append(f"{project_dir}/.hermes/config.json")
                
        except Exception as e:
            results["success"] = False
            results["errors"].append(str(e))
            
        return results

