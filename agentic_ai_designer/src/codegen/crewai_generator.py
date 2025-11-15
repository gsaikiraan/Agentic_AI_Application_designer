"""
CrewAI Code Generator
Generates production-ready CrewAI implementations with separate agent files.
"""

from typing import Dict, List
from ..designer import SystemArchitecture, AgentDefinition


class CrewAICodeGenerator:
    """
    Generates CrewAI-based multi-agent system code with separate agent files.
    Each agent gets its own file in the agents/ directory.
    """

    def generate(self, architecture: SystemArchitecture) -> Dict[str, str]:
        """
        Generate all CrewAI code files.

        Args:
            architecture: System architecture design

        Returns:
            Dictionary mapping file paths to code content
        """
        files = {}

        # Core files
        files["config.py"] = self._generate_config(architecture)
        files["tools.py"] = self._generate_tools(architecture)

        # Agent files - separate file for each agent
        files["agents/__init__.py"] = self._generate_agents_init(architecture)
        for agent in architecture.agents:
            agent_filename = agent.name.lower().replace(" ", "_") + ".py"
            files[f"agents/{agent_filename}"] = self._generate_individual_agent(agent, architecture)

        # Task definitions
        files["tasks.py"] = self._generate_tasks(architecture)

        # Crew orchestration
        files["crew.py"] = self._generate_crew(architecture)

        # Main entry point
        files["main.py"] = self._generate_main(architecture)

        # Documentation
        files["README.md"] = self._generate_readme(architecture)
        files["requirements.txt"] = self._generate_requirements()

        return files

    def _generate_config(self, architecture: SystemArchitecture) -> str:
        """Generate configuration file."""
        return '''"""
Configuration for the CrewAI multi-agent system.
"""

import os
from typing import Optional


class Config:
    """System configuration."""

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")  # For web search

    # Model configuration
    DEFAULT_MODEL: str = "gpt-4"
    DEFAULT_TEMPERATURE: float = 0.7

    # Agent configuration
    MAX_ITERATIONS: int = 15
    VERBOSE: bool = True

    # Tool configuration
    ENABLE_WEB_SEARCH: bool = True
    ENABLE_FILE_TOOLS: bool = True

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        return True


# Validate on import
Config.validate()
'''

    def _generate_tools(self, architecture: SystemArchitecture) -> str:
        """Generate tools module."""
        tools_code = '''"""
Tools for CrewAI agents.
"""

from crewai_tools import (
    SerperDevTool,
    FileReadTool,
    DirectoryReadTool,
    CodeInterpreterTool
)
from typing import List, Any


class ToolRegistry:
    """Registry of available tools for agents."""

    def __init__(self):
        self._tools = {}
        self._initialize_tools()

    def _initialize_tools(self):
        """Initialize all available tools."""
        # Web search tool
        self._tools["web_search"] = SerperDevTool()

        # File tools
        self._tools["file_read"] = FileReadTool()
        self._tools["directory_read"] = DirectoryReadTool()

        # Code analysis
        self._tools["code_interpreter"] = CodeInterpreterTool()

    def get_tools(self, tool_names: List[str]) -> List[Any]:
        """
        Get tools by name.

        Args:
            tool_names: List of tool names to retrieve

        Returns:
            List of tool instances
        """
        tools = []
        for name in tool_names:
            if name in self._tools:
                tools.append(self._tools[name])
            else:
                print(f"Warning: Tool '{name}' not found in registry")

        return tools

    def get_all_tools(self) -> List[Any]:
        """Get all available tools."""
        return list(self._tools.values())


# Global tool registry
tool_registry = ToolRegistry()
'''
        return tools_code

    def _generate_agents_init(self, architecture: SystemArchitecture) -> str:
        """Generate agents/__init__.py with imports."""
        imports = []
        for agent in architecture.agents:
            class_name = ''.join(word.capitalize() for word in agent.name.split())
            module_name = agent.name.lower().replace(" ", "_")
            imports.append(f"from .{module_name} import {class_name}")

        return f'''"""
Agent definitions for the CrewAI system.
"""

{chr(10).join(imports)}

__all__ = [
    {', '.join(f'"{word.capitalize() for word in agent.name.split()}"' for agent in architecture.agents)}
]
'''

    def _generate_individual_agent(self, agent: AgentDefinition, architecture: SystemArchitecture) -> str:
        """Generate code for an individual agent in its own file."""
        class_name = ''.join(word.capitalize() for word in agent.name.split())

        # Determine tools for this agent
        tool_names = []
        if any(comp.component_type.name == "TOOL_INTEGRATION" for comp in agent.components):
            tool_names = ["web_search", "file_read"]

        # Build backstory from components
        backstory_parts = [agent.description]
        for comp in agent.components:
            backstory_parts.append(f"Equipped with {comp.component_type.name.lower().replace('_', ' ')} capabilities.")

        backstory = " ".join(backstory_parts)

        code = f'''"""
{agent.name} agent implementation.
"""

from crewai import Agent
from config import Config
from tools import tool_registry


class {class_name}:
    """
    {agent.name} - {agent.description}

    Role: {agent.role.value if hasattr(agent, 'role') else 'Specialist'}

    Components:
{chr(10).join(f"    - {comp.component_type.name}: {comp.description}" for comp in agent.components)}
    """

    def __init__(self):
        """Initialize the {agent.name}."""
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """
        Create the CrewAI agent instance.

        Returns:
            Configured Agent instance
        """
        # Get tools for this agent
        tool_names = {tool_names}
        tools = tool_registry.get_tools(tool_names) if tool_names else []

        return Agent(
            role="{agent.name}",
            goal="""{self._get_goal(agent)}""",
            backstory="""{backstory}""",
            tools=tools,
            verbose=Config.VERBOSE,
            allow_delegation={'true' if 'master' in agent.name.lower() or 'planner' in agent.name.lower() else 'false'},
            max_iter=Config.MAX_ITERATIONS,
            llm=Config.DEFAULT_MODEL
        )

    def get_agent(self) -> Agent:
        """Get the agent instance."""
        return self.agent
'''

        return code

    def _get_goal(self, agent: AgentDefinition) -> str:
        """Generate goal statement for agent."""
        role_goals = {
            "MASTER_PLANNER": "Coordinate and optimize the overall workflow, delegating tasks to specialist agents and ensuring project success",
            "SPECIALIST": f"Execute specialized tasks in {agent.name.lower()} domain with high expertise and accuracy",
            "COMMUNICATION_FACILITATOR": "Facilitate communication between agents, resolve conflicts, and maintain workflow coherence",
            "REFLECTIVE_OBSERVER": "Monitor system performance, identify improvements, and provide strategic recommendations"
        }

        if hasattr(agent, 'role'):
            return role_goals.get(agent.role.name, agent.description)
        return agent.description

    def _generate_tasks(self, architecture: SystemArchitecture) -> str:
        """Generate tasks module."""
        task_definitions = []

        for i, agent in enumerate(architecture.agents):
            class_name = ''.join(word.capitalize() for word in agent.name.split())
            task_name = agent.name.lower().replace(" ", "_") + "_task"

            task_def = f'''
def create_{task_name}(agent: Agent, context: str = "") -> Task:
    """
    Create task for {agent.name}.

    Args:
        agent: Agent to execute the task
        context: Additional context for the task

    Returns:
        Task instance
    """
    return Task(
        description=f"""
        {{context}}

        Execute your role as {agent.name}:
        {agent.description}

        Focus on delivering high-quality results aligned with your specialization.
        """,
        agent=agent,
        expected_output="""
        Detailed output from {agent.name} including:
        - Analysis and findings
        - Recommendations
        - Next steps or deliverables
        """
    )
'''
            task_definitions.append(task_def)

        return f'''"""
Task definitions for CrewAI agents.
"""

from crewai import Task, Agent


{chr(10).join(task_definitions)}


def create_all_tasks(agents: dict, user_input: str = "") -> list:
    """
    Create all tasks for the crew.

    Args:
        agents: Dictionary mapping agent names to agent instances
        user_input: User input or project requirements

    Returns:
        List of Task instances
    """
    tasks = []
    context = user_input

    # Create tasks in execution order
{chr(10).join(f'    tasks.append(create_{agent.name.lower().replace(" ", "_")}_task(agents["{agent.name}"], context))' for agent in architecture.agents)}

    return tasks
'''

    def _generate_crew(self, architecture: SystemArchitecture) -> str:
        """Generate crew orchestration module."""
        agent_imports = []
        agent_inits = []

        for agent in architecture.agents:
            class_name = ''.join(word.capitalize() for word in agent.name.split())
            agent_imports.append(f"from agents import {class_name}")
            agent_var = agent.name.lower().replace(" ", "_")
            agent_inits.append(f'        {agent_var} = {class_name}()')
            agent_inits.append(f'        self.agents["{agent.name}"] = {agent_var}.get_agent()')

        return f'''"""
Crew orchestration for the multi-agent system.
"""

from crewai import Crew, Process
from config import Config
{chr(10).join(agent_imports)}
from tasks import create_all_tasks


class {architecture.project_name.replace(" ", "")}Crew:
    """
    Main crew orchestrator for {architecture.project_name}.

    Architecture:
    - {len(architecture.agents)} agents working collaboratively
    - Patterns: {', '.join(p.name for p in architecture.patterns)}
    """

    def __init__(self):
        """Initialize the crew."""
        self.agents = {{}}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all agents."""
{chr(10).join(agent_inits)}

    def create_crew(self, user_input: str = "") -> Crew:
        """
        Create the crew with all agents and tasks.

        Args:
            user_input: User requirements or project description

        Returns:
            Configured Crew instance
        """
        # Create tasks
        tasks = create_all_tasks(self.agents, user_input)

        # Create crew
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,  # Can be changed to Process.hierarchical
            verbose=Config.VERBOSE,
            memory=True,  # Enable memory for agent collaboration
            embedder={{
                "provider": "openai",
                "config": {{
                    "model": "text-embedding-3-small"
                }}
            }}
        )

        return crew

    def run(self, user_input: str = "") -> dict:
        """
        Run the crew on a task.

        Args:
            user_input: User requirements or task description

        Returns:
            Result dictionary with outputs
        """
        crew = self.create_crew(user_input)
        result = crew.kickoff()

        return {{
            "result": result,
            "agents": list(self.agents.keys()),
            "success": True
        }}
'''

    def _generate_main(self, architecture: SystemArchitecture) -> str:
        """Generate main entry point."""
        crew_class = architecture.project_name.replace(" ", "")

        return f'''"""
Main entry point for {architecture.project_name}.
"""

import sys
from crew import {crew_class}Crew
from config import Config


def main():
    """Main execution function."""
    print("=" * 80)
    print(f"  {architecture.project_name}")
    print("  CrewAI Multi-Agent System")
    print("=" * 80)
    print()

    # Get user input
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print("Enter your task or requirements:")
        user_input = input("> ").strip()

    if not user_input:
        print("No input provided. Exiting.")
        return

    print(f"\\nProcessing: {{user_input}}\\n")
    print("-" * 80)

    # Create and run crew
    crew_system = {crew_class}Crew()
    result = crew_system.run(user_input)

    # Display results
    print("\\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(result["result"])
    print()
    print(f"Agents involved: {{', '.join(result['agents'])}}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\nInterrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\\nError: {{e}}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
'''

    def _generate_readme(self, architecture: SystemArchitecture) -> str:
        """Generate README documentation."""
        agents_list = '\n'.join(f"- **{agent.name}**: {agent.description}" for agent in architecture.agents)
        tools_list = '\n'.join(f"- {tool}" for tool in ["Web Search", "File Operations", "Code Interpreter"])

        return f'''# {architecture.project_name}

CrewAI-based multi-agent system for {architecture.description}.

## Architecture

### Agents

{agents_list}

### Design Patterns

{chr(10).join(f"- **{p.name}**: {p.description}" for p in architecture.patterns)}

### Tools

{tools_list}

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export SERPER_API_KEY="your-serper-key"  # Optional, for web search
```

## Usage

Run the system:
```bash
python main.py "Your task description here"
```

Or run interactively:
```bash
python main.py
```

## Project Structure

```
.
├── agents/           # Individual agent definitions
│   ├── __init__.py
{chr(10).join(f"│   ├── {agent.name.lower().replace(' ', '_')}.py" for agent in architecture.agents)}
├── config.py        # Configuration
├── tools.py         # Tool definitions
├── tasks.py         # Task definitions
├── crew.py          # Crew orchestration
├── main.py          # Entry point
└── README.md        # This file
```

## Key Features

- **Separate Agent Files**: Each agent has its own module for better organization
- **Tool Integration**: Built-in tools for web search, file operations, and code analysis
- **Memory & Collaboration**: Agents share context and collaborate effectively
- **Configurable Process**: Sequential or hierarchical execution
- **Production Ready**: Proper error handling, logging, and configuration

## Customization

### Adding New Agents

1. Create new agent file in `agents/` directory
2. Define agent with role, goal, backstory, and tools
3. Add to `crew.py` initialization
4. Create corresponding task in `tasks.py`

### Adding New Tools

1. Import tool from `crewai_tools` in `tools.py`
2. Add to `ToolRegistry._initialize_tools()`
3. Assign to agents in their definition files

## Development

Built with CrewAI framework following best practices for multi-agent systems.

Generated by Agentic AI Application Designer.
'''

    def _generate_requirements(self) -> str:
        """Generate requirements.txt."""
        return '''# CrewAI and dependencies
crewai>=0.28.0
crewai-tools>=0.2.0

# LLM providers
langchain>=0.1.0
langchain-openai>=0.0.5

# Tools
serper>=0.1.0

# Utilities
python-dotenv>=1.0.0
'''


def generate_crewai_code(architecture: SystemArchitecture) -> Dict[str, str]:
    """
    Generate CrewAI code for the given architecture.

    Args:
        architecture: System architecture design

    Returns:
        Dictionary mapping file paths to code content
    """
    generator = CrewAICodeGenerator()
    return generator.generate(architecture)
