"""
Enhanced LangGraph code generator with separate files for each agent.
"""

from typing import Dict
from ..designer import SystemArchitecture
from ..framework import ComponentType, AgentRole


class EnhancedLangGraphGenerator:
    """Generates LangGraph code with separate agent files."""

    def generate(self, architecture: SystemArchitecture) -> Dict[str, str]:
        """
        Generate complete LangGraph implementation with separate agent files.

        Returns:
            Dictionary of filename -> code content
        """
        files = {}

        # Core files
        files["state.py"] = self._generate_state(architecture)
        files["tools.py"] = self._generate_tools(architecture)
        files["config.py"] = self._generate_config(architecture)

        # Base agent class
        files["agents/__init__.py"] = self._generate_base_agent()

        # Individual agent files
        for agent in architecture.agents:
            agent_filename = agent.name.lower().replace(" ", "_") + "_agent.py"
            files[f"agents/{agent_filename}"] = self._generate_individual_agent(agent, architecture)

        # Graph with imports from individual files
        files["graph.py"] = self._generate_graph(architecture)

        # Main entry point
        files["main.py"] = self._generate_main(architecture)

        # README for the generated project
        files["README.md"] = self._generate_readme(architecture)

        return files

    def _generate_state(self, architecture: SystemArchitecture) -> str:
        """Generate state definitions."""
        code = []
        code.append('"""')
        code.append(f"State definitions for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from typing import TypedDict, Annotated, List, Dict")
        code.append("from langgraph.graph.message import add_messages")
        code.append("")
        code.append("")
        code.append("class AgentState(TypedDict):")
        code.append('    """Shared state for all agents."""')
        code.append("    messages: Annotated[List, add_messages]")
        code.append("    current_task: str")
        code.append("    task_status: str")
        code.append("    completed_tasks: List[str]")
        code.append("    next_agent: str")
        code.append("    tool_results: Dict")

        if any(ComponentType.REFLECTION in agent.components for agent in architecture.agents):
            code.append("    reflection_results: List[Dict]")
            code.append("    performance_metrics: Dict")

        if any(ComponentType.PLANNING in agent.components for agent in architecture.agents):
            code.append("    current_plan: List[Dict]")
            code.append("    plan_status: str")

        code.append("")
        return "\n".join(code)

    def _generate_base_agent(self) -> str:
        """Generate base agent class."""
        code = []
        code.append('"""')
        code.append("Base agent class for all agents.")
        code.append('"""')
        code.append("")
        code.append("from langchain_core.messages import SystemMessage")
        code.append("from langchain_openai import ChatOpenAI")
        code.append("from typing import Dict")
        code.append("from ..state import AgentState")
        code.append("from ..tools import get_tools_for_agent")
        code.append("")
        code.append("")
        code.append("class BaseAgent:")
        code.append('    """Base class for all agents."""')
        code.append("")
        code.append("    def __init__(self, name: str, role: str, model: str = 'gpt-4'):")
        code.append("        self.name = name")
        code.append("        self.role = role")
        code.append("        self.llm = ChatOpenAI(model=model, temperature=0)")
        code.append("        self.tools = get_tools_for_agent(role)")
        code.append("")
        code.append("        if self.tools:")
        code.append("            self.llm = self.llm.bind_tools(self.tools)")
        code.append("")
        code.append("    def get_system_prompt(self) -> str:")
        code.append('        """Override this in subclasses."""')
        code.append("        return f\"You are {self.name}, a {self.role} agent.\"")
        code.append("")
        code.append("    def invoke(self, state: AgentState) -> Dict:")
        code.append('        """Main execution method called by LangGraph."""')
        code.append("        messages = [")
        code.append("            SystemMessage(content=self.get_system_prompt()),")
        code.append("            *state['messages']")
        code.append("        ]")
        code.append("")
        code.append("        response = self.llm.invoke(messages)")
        code.append("")
        code.append("        return {")
        code.append("            'messages': [response],")
        code.append("            'next_agent': self.determine_next_agent(state, response)")
        code.append("        }")
        code.append("")
        code.append("    def determine_next_agent(self, state: AgentState, response) -> str:")
        code.append('        """Override to implement routing logic."""')
        code.append("        return 'END'")
        code.append("")
        return "\n".join(code)

    def _generate_individual_agent(self, agent, architecture: SystemArchitecture) -> str:
        """Generate code for an individual agent in its own file."""
        code = []
        agent_class = agent.name.replace(" ", "")

        code.append('"""')
        code.append(f"{agent.name} implementation.")
        code.append('"""')
        code.append("")
        code.append("from typing import Dict")
        code.append("from . import BaseAgent")
        code.append("from ..state import AgentState")
        code.append("")
        code.append("")
        code.append(f"class {agent_class}(BaseAgent):")
        code.append(f'    """{agent.name} - {agent.role.value}."""')
        code.append("")
        code.append("    def __init__(self):")
        code.append("        super().__init__(")
        code.append(f"            name='{agent.name}',")
        code.append(f"            role='{agent.role.value}'")
        code.append("        )")
        code.append("")
        code.append("    def get_system_prompt(self) -> str:")
        code.append(f'        """System prompt for {agent.name}."""')
        code.append("        return \"\"\"You are " + agent.name + ".")
        code.append("")
        code.append("Your responsibilities:")
        for resp in agent.responsibilities[:5]:
            code.append(f"- {resp}")
        code.append("")

        if agent.tools:
            code.append("You have access to these tools:")
            for tool in agent.tools[:3]:
                code.append(f"- {tool}")
            code.append("")

        code.append("Work diligently and coordinate with other agents as needed.")
        code.append('"""')
        code.append("")

        # Add routing logic based on role
        if agent.role == AgentRole.MASTER_PLANNER:
            code.append("    def determine_next_agent(self, state: AgentState, response) -> str:")
            code.append('        """Route to appropriate specialist based on task."""')
            code.append("        task = state.get('current_task', '').lower()")
            code.append("        ")
            code.append("        # Simple routing logic - customize as needed")
            code.append("        if state.get('task_status') == 'completed':")
            code.append("            return 'END'")
            code.append("        ")
            code.append("        # Route to first specialist by default")
            code.append("        return 'specialist'")
            code.append("")
        elif agent.role == AgentRole.SPECIALIST:
            code.append("    def determine_next_agent(self, state: AgentState, response) -> str:")
            code.append('        """Return to master planner after completing work."""')
            code.append("        return 'master_planner'")
            code.append("")

        return "\n".join(code)

    def _generate_tools(self, architecture: SystemArchitecture) -> str:
        """Generate tools module."""
        code = []
        code.append('"""')
        code.append("Tools for the multi-agent system.")
        code.append('"""')
        code.append("")
        code.append("from langchain_core.tools import tool")
        code.append("from langchain_community.tools.tavily_search import TavilySearchResults")
        code.append("from typing import List")
        code.append("")
        code.append("")
        code.append("@tool")
        code.append("def search_web(query: str) -> str:")
        code.append('    """Search the web for information."""')
        code.append("    try:")
        code.append("        search = TavilySearchResults(max_results=3)")
        code.append("        results = search.invoke(query)")
        code.append("        return str(results)")
        code.append("    except Exception as e:")
        code.append("        return f\"Search failed: {e}\"")
        code.append("")
        code.append("")
        code.append("@tool")
        code.append("def analyze_data(data: str) -> str:")
        code.append('    """Analyze data and return insights."""')
        code.append("    return f\"Analysis complete for: {data[:100]}...\"")
        code.append("")
        code.append("")
        code.append("def get_tools_for_agent(role: str) -> List:")
        code.append('    """Get tools based on agent role."""')
        code.append("    tool_mapping = {")
        code.append("        'master_planner': [],")
        code.append("        'specialist': [search_web, analyze_data],")
        code.append("        'communication_facilitator': [],")
        code.append("        'reflective_observer': [analyze_data],")
        code.append("    }")
        code.append("    return tool_mapping.get(role, [])")
        code.append("")
        return "\n".join(code)

    def _generate_graph(self, architecture: SystemArchitecture) -> str:
        """Generate workflow graph with imports from individual agent files."""
        code = []
        code.append('"""')
        code.append(f"LangGraph workflow for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from langgraph.graph import StateGraph, END")
        code.append("from langgraph.checkpoint.memory import MemorySaver")
        code.append("from .state import AgentState")
        code.append("")

        # Import each agent from its own file
        for agent in architecture.agents:
            agent_class = agent.name.replace(" ", "")
            agent_module = agent.name.lower().replace(" ", "_") + "_agent"
            code.append(f"from .agents.{agent_module} import {agent_class}")

        code.append("")
        code.append("")
        code.append("def create_graph():")
        code.append(f'    """Create the workflow graph for {architecture.project_name}."""')
        code.append("")
        code.append("    # Initialize agents")

        agent_vars = []
        for agent in architecture.agents:
            agent_class = agent.name.replace(" ", "")
            agent_var = agent.name.lower().replace(" ", "_")
            code.append(f"    {agent_var} = {agent_class}()")
            agent_vars.append((agent_var, agent.name, agent.role))

        code.append("")
        code.append("    # Create graph")
        code.append("    workflow = StateGraph(AgentState)")
        code.append("")
        code.append("    # Add nodes for each agent")

        for agent_var, _, _ in agent_vars:
            code.append(f"    workflow.add_node('{agent_var}', {agent_var}.invoke)")

        code.append("")
        code.append("    # Define workflow")

        # Find master planner
        master_var = next((v for v, n, r in agent_vars if r == AgentRole.MASTER_PLANNER), None)
        specialist_vars = [v for v, n, r in agent_vars if r == AgentRole.SPECIALIST]

        if master_var:
            code.append(f"    workflow.set_entry_point('{master_var}')")
            code.append("")

            if specialist_vars:
                code.append("    # Master planner can route to specialists")
                for spec in specialist_vars[:2]:
                    code.append(f"    workflow.add_edge('{master_var}', '{spec}')")
                    code.append(f"    workflow.add_edge('{spec}', '{master_var}')")
                code.append("")

            code.append("    # Conditional routing for completion")
            code.append("    def should_continue(state: AgentState) -> str:")
            code.append("        if state.get('task_status') == 'completed':")
            code.append("            return 'end'")
            code.append("        return 'continue'")
            code.append("")
            code.append(f"    workflow.add_conditional_edges(")
            code.append(f"        '{master_var}',")
            code.append(f"        should_continue,")
            code.append(f"        {{'continue': '{specialist_vars[0] if specialist_vars else master_var}', 'end': END}}")
            code.append(f"    )")
        else:
            # Simple linear flow
            if agent_vars:
                code.append(f"    workflow.set_entry_point('{agent_vars[0][0]}')")
                code.append(f"    workflow.add_edge('{agent_vars[0][0]}', END)")

        code.append("")
        code.append("    # Compile with checkpointing")
        code.append("    memory = MemorySaver()")
        code.append("    app = workflow.compile(checkpointer=memory)")
        code.append("")
        code.append("    return app")
        code.append("")
        return "\n".join(code)

    def _generate_config(self, architecture: SystemArchitecture) -> str:
        """Generate configuration."""
        code = []
        code.append('"""')
        code.append("Configuration settings.")
        code.append('"""')
        code.append("")
        code.append("import os")
        code.append("")
        code.append("")
        code.append("class Config:")
        code.append('    """Configuration for the multi-agent system."""')
        code.append("")
        code.append("    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')")
        code.append("    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '')")
        code.append(f"    PROJECT_NAME = '{architecture.project_name}'")
        code.append(f"    NUM_AGENTS = {len(architecture.agents)}")
        code.append("    DEFAULT_MODEL = 'gpt-4'")
        code.append("")
        code.append("")
        code.append("config = Config()")
        code.append("")
        return "\n".join(code)

    def _generate_main(self, architecture: SystemArchitecture) -> str:
        """Generate main entry point."""
        code = []
        code.append('"""')
        code.append(f"Main entry point for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from langchain_core.messages import HumanMessage")
        code.append("from graph import create_graph")
        code.append("from state import AgentState")
        code.append("from config import config")
        code.append("")
        code.append("")
        code.append("def run(task: str):")
        code.append(f'    """Run {architecture.project_name} on a task."""')
        code.append("    if not config.OPENAI_API_KEY:")
        code.append("        print('Error: OPENAI_API_KEY not set')")
        code.append("        return")
        code.append("")
        code.append("    app = create_graph()")
        code.append("")
        code.append("    initial_state: AgentState = {")
        code.append("        'messages': [HumanMessage(content=task)],")
        code.append("        'current_task': task,")
        code.append("        'task_status': 'pending',")
        code.append("        'completed_tasks': [],")
        code.append("        'next_agent': '',")
        code.append("        'tool_results': {},")
        code.append("    }")
        code.append("")
        code.append("    print(f'Starting task: {task}\\n')")
        code.append("")
        code.append("    config_dict = {'configurable': {'thread_id': '1'}}")
        code.append("")
        code.append("    for output in app.stream(initial_state, config_dict):")
        code.append("        for key, value in output.items():")
        code.append("            print(f'\\n--- {key} ---')")
        code.append("            if 'messages' in value:")
        code.append("                print(value['messages'][-1].content)")
        code.append("")
        code.append("    print('\\n=== Task Complete ===')")
        code.append("")
        code.append("")
        code.append("if __name__ == '__main__':")
        code.append(f"    task = \"{architecture.description}\"")
        code.append("    run(task)")
        code.append("")
        return "\n".join(code)

    def _generate_readme(self, architecture: SystemArchitecture) -> str:
        """Generate README for the generated project."""
        lines = []
        lines.append(f"# {architecture.project_name}")
        lines.append("")
        lines.append(f"{architecture.description}")
        lines.append("")
        lines.append("## Architecture")
        lines.append("")
        lines.append(f"**Agents:** {len(architecture.agents)}")
        for agent in architecture.agents:
            lines.append(f"- **{agent.name}**: {agent.role.value}")
        lines.append("")
        lines.append("## Setup")
        lines.append("")
        lines.append("```bash")
        lines.append("# Install dependencies")
        lines.append("pip install langchain langgraph langchain-openai langchain-community tavily-python")
        lines.append("")
        lines.append("# Set API keys")
        lines.append("export OPENAI_API_KEY='your-key'")
        lines.append("export TAVILY_API_KEY='your-key'  # Optional")
        lines.append("```")
        lines.append("")
        lines.append("## Usage")
        lines.append("")
        lines.append("```bash")
        lines.append("python main.py")
        lines.append("```")
        lines.append("")
        lines.append("## Project Structure")
        lines.append("")
        lines.append("```")
        lines.append(".")
        lines.append("├── agents/")
        lines.append("│   ├── __init__.py          # Base agent class")
        for agent in architecture.agents:
            filename = agent.name.lower().replace(" ", "_") + "_agent.py"
            lines.append(f"│   └── {filename:<25} # {agent.name}")
        lines.append("├── state.py                # State definitions")
        lines.append("├── tools.py                # Tool definitions")
        lines.append("├── graph.py                # Workflow graph")
        lines.append("├── config.py               # Configuration")
        lines.append("├── main.py                 # Entry point")
        lines.append("└── README.md               # This file")
        lines.append("```")
        lines.append("")
        lines.append("## Generated by")
        lines.append("")
        lines.append("Agentic AI Application Designer")
        lines.append("")
        return "\n".join(lines)
