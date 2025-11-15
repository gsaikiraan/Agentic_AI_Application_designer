"""
LangGraph code generator for agentic AI applications.
Generates working LangGraph implementations from architecture designs.
"""

from typing import List, Dict
from ..designer import SystemArchitecture, AgentArchitecture
from ..framework import ComponentType, AgentRole


class LangGraphCodeGenerator:
    """Generates LangGraph implementation code from architecture."""

    def generate_implementation(self, architecture: SystemArchitecture) -> Dict[str, str]:
        """
        Generate complete LangGraph implementation.

        Args:
            architecture: System architecture

        Returns:
            Dictionary of filename -> code content
        """
        files = {}

        # Generate state definitions
        files["state.py"] = self._generate_state_module(architecture)

        # Generate agent implementations
        files["agents.py"] = self._generate_agents_module(architecture)

        # Generate tools
        files["tools.py"] = self._generate_tools_module(architecture)

        # Generate graph
        files["graph.py"] = self._generate_graph_module(architecture)

        # Generate main entry point
        files["main.py"] = self._generate_main_module(architecture)

        # Generate config
        files["config.py"] = self._generate_config_module(architecture)

        return files

    def _generate_state_module(self, architecture: SystemArchitecture) -> str:
        """Generate state definitions for LangGraph."""
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
        code.append('    """Shared state for all agents in the system."""')
        code.append("    ")
        code.append("    # Message history")
        code.append("    messages: Annotated[List, add_messages]")
        code.append("    ")
        code.append("    # Task tracking")
        code.append("    current_task: str")
        code.append("    task_status: str")
        code.append("    completed_tasks: List[str]")
        code.append("    ")
        code.append("    # Agent coordination")
        code.append("    next_agent: str")
        code.append("    delegation_history: List[Dict]")
        code.append("    ")

        # Add reflection state if needed
        if any(ComponentType.REFLECTION in agent.components for agent in architecture.agents):
            code.append("    # Reflection data")
            code.append("    reflection_results: List[Dict]")
            code.append("    performance_metrics: Dict")
            code.append("    ")

        # Add planning state if needed
        if any(ComponentType.PLANNING in agent.components for agent in architecture.agents):
            code.append("    # Planning data")
            code.append("    current_plan: List[Dict]")
            code.append("    plan_status: str")
            code.append("    ")

        code.append("    # Tool results")
        code.append("    tool_results: Dict")
        code.append("")
        code.append("")
        code.append("class TaskState(TypedDict):")
        code.append('    """State for individual task execution."""')
        code.append("    task_id: str")
        code.append("    description: str")
        code.append("    assigned_agent: str")
        code.append("    status: str  # pending, in_progress, completed, failed")
        code.append("    result: Dict")
        code.append("")

        return "\n".join(code)

    def _generate_agents_module(self, architecture: SystemArchitecture) -> str:
        """Generate agent implementations."""
        code = []
        code.append('"""')
        code.append(f"Agent implementations for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from langchain_core.messages import HumanMessage, AIMessage, SystemMessage")
        code.append("from langchain_openai import ChatOpenAI")
        code.append("from typing import Dict, List")
        code.append("from .state import AgentState, TaskState")
        code.append("from .tools import get_tools_for_agent")
        code.append("")
        code.append("")
        code.append("class BaseAgent:")
        code.append('    """Base class for all agents."""')
        code.append("    ")
        code.append("    def __init__(self, name: str, role: str, model_name: str = 'gpt-4'):")
        code.append("        self.name = name")
        code.append("        self.role = role")
        code.append("        self.llm = ChatOpenAI(model=model_name, temperature=0)")
        code.append("        self.tools = get_tools_for_agent(role)")
        code.append("        ")
        code.append("        if self.tools:")
        code.append("            self.llm = self.llm.bind_tools(self.tools)")
        code.append("    ")
        code.append("    def get_system_prompt(self) -> str:")
        code.append('        """Get system prompt for this agent."""')
        code.append("        return f\"You are {self.name}, a {self.role} agent.\"")
        code.append("    ")
        code.append("    def invoke(self, state: AgentState) -> Dict:")
        code.append('        """Process state and return updated state."""')
        code.append("        messages = [")
        code.append("            SystemMessage(content=self.get_system_prompt()),")
        code.append("            *state['messages']")
        code.append("        ]")
        code.append("        ")
        code.append("        response = self.llm.invoke(messages)")
        code.append("        ")
        code.append("        return {")
        code.append("            'messages': [response],")
        code.append("            'next_agent': self.determine_next_agent(state, response)")
        code.append("        }")
        code.append("    ")
        code.append("    def determine_next_agent(self, state: AgentState, response) -> str:")
        code.append('        """Determine which agent should process next."""')
        code.append("        # Override in subclasses")
        code.append("        return 'END'")
        code.append("")
        code.append("")

        # Generate specific agent classes
        for agent in architecture.agents:
            agent_class_name = agent.name.replace(" ", "")
            code.append(f"class {agent_class_name}(BaseAgent):")
            code.append(f'    """{agent.name} implementation."""')
            code.append("    ")
            code.append("    def __init__(self):")
            code.append(f"        super().__init__(")
            code.append(f"            name='{agent.name}',")
            code.append(f"            role='{agent.role.value}'")
            code.append("        )")
            code.append("    ")
            code.append("    def get_system_prompt(self) -> str:")
            code.append(f'        """System prompt for {agent.name}."""')
            code.append("        return f\"\"\"You are {self.name}.")
            code.append("")
            code.append("Your responsibilities:")
            for resp in agent.responsibilities[:3]:  # Limit to first 3
                code.append(f"- {resp}")
            code.append("")

            if agent.tools:
                code.append("You have access to the following tools:")
                for tool in agent.tools[:3]:
                    code.append(f"- {tool}")
                code.append("")

            code.append("Perform your tasks diligently and coordinate with other agents as needed.")
            code.append('"""')
            code.append("    ")

            # Add reflection method if applicable
            if ComponentType.REFLECTION in agent.components:
                code.append("    def reflect(self, state: AgentState) -> Dict:")
                code.append('        """Perform reflection on recent actions."""')
                code.append("        # Analyze performance metrics")
                code.append("        metrics = state.get('performance_metrics', {})")
                code.append("        ")
                code.append("        reflection = {")
                code.append("            'agent': self.name,")
                code.append("            'metrics': metrics,")
                code.append("            'issues': [],")
                code.append("            'recommendations': []")
                code.append("        }")
                code.append("        ")
                code.append("        # Add reflection logic here")
                code.append("        ")
                code.append("        return {")
                code.append("            'reflection_results': state.get('reflection_results', []) + [reflection]")
                code.append("        }")
                code.append("    ")

            # Add planning method if master planner
            if agent.role == AgentRole.MASTER_PLANNER:
                code.append("    def plan_tasks(self, state: AgentState) -> Dict:")
                code.append('        """Decompose goals into tasks."""')
                code.append("        current_task = state.get('current_task', '')")
                code.append("        ")
                code.append("        # Use LLM to decompose task")
                code.append("        planning_prompt = f\"\"\"")
                code.append("        Decompose the following task into subtasks:")
                code.append("        {current_task}")
                code.append("        ")
                code.append("        Provide a structured plan with specific subtasks.")
                code.append('        """')
                code.append("        ")
                code.append("        messages = [")
                code.append("            SystemMessage(content=self.get_system_prompt()),")
                code.append("            HumanMessage(content=planning_prompt)")
                code.append("        ]")
                code.append("        ")
                code.append("        response = self.llm.invoke(messages)")
                code.append("        ")
                code.append("        return {")
                code.append("            'current_plan': [{'task': response.content}],")
                code.append("            'plan_status': 'created'")
                code.append("        }")
                code.append("    ")

            code.append("    def determine_next_agent(self, state: AgentState, response) -> str:")
            code.append('        """Determine next agent in workflow."""')

            if agent.role == AgentRole.MASTER_PLANNER:
                code.append("        # Master planner delegates to specialists")
                code.append("        if state.get('task_status') == 'planned':")
                code.append("            return 'specialist'")
                code.append("        return 'END'")
            elif agent.role == AgentRole.SPECIALIST:
                code.append("        # Specialist returns to master or ends")
                code.append("        if state.get('task_status') == 'completed':")
                code.append("            return 'master_planner'")
                code.append("        return 'END'")
            else:
                code.append("        return 'END'")

            code.append("")
            code.append("")

        return "\n".join(code)

    def _generate_tools_module(self, architecture: SystemArchitecture) -> str:
        """Generate tools module."""
        code = []
        code.append('"""')
        code.append(f"Tools for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from langchain_core.tools import tool")
        code.append("from langchain_community.tools.tavily_search import TavilySearchResults")
        code.append("from typing import List")
        code.append("")
        code.append("")
        code.append("# Define tools")
        code.append("")
        code.append("@tool")
        code.append("def search_web(query: str) -> str:")
        code.append('    """Search the web for information."""')
        code.append("    search = TavilySearchResults(max_results=3)")
        code.append("    results = search.invoke(query)")
        code.append("    return str(results)")
        code.append("")
        code.append("")
        code.append("@tool")
        code.append("def analyze_data(data: str) -> str:")
        code.append('    """Analyze data and return insights."""')
        code.append("    # Implement data analysis logic")
        code.append("    return f\"Analysis of: {data}\"")
        code.append("")
        code.append("")
        code.append("@tool")
        code.append("def generate_report(content: str) -> str:")
        code.append('    """Generate a formatted report."""')
        code.append("    # Implement report generation")
        code.append("    return f\"Report:\\n{content}\"")
        code.append("")
        code.append("")
        code.append("# Tool registry")
        code.append("TOOL_REGISTRY = {")
        code.append("    'web_search': search_web,")
        code.append("    'data_analysis': analyze_data,")
        code.append("    'report_generation': generate_report,")
        code.append("}")
        code.append("")
        code.append("")
        code.append("def get_tools_for_agent(role: str) -> List:")
        code.append('    """Get tools available for an agent role."""')
        code.append("    ")
        code.append("    tool_mapping = {")
        code.append("        'master_planner': [],")
        code.append("        'specialist': [search_web, analyze_data],")
        code.append("        'communication_facilitator': [],")
        code.append("        'reflective_observer': [analyze_data],")
        code.append("    }")
        code.append("    ")
        code.append("    return tool_mapping.get(role, [])")
        code.append("")

        return "\n".join(code)

    def _generate_graph_module(self, architecture: SystemArchitecture) -> str:
        """Generate LangGraph workflow."""
        code = []
        code.append('"""')
        code.append(f"LangGraph workflow for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from langgraph.graph import StateGraph, END")
        code.append("from langgraph.checkpoint.memory import MemorySaver")
        code.append("from .state import AgentState")
        code.append("from .agents import (")

        # Import all agent classes
        agent_classes = []
        for agent in architecture.agents:
            agent_class = agent.name.replace(" ", "")
            agent_classes.append(f"    {agent_class}")

        code.append(",\n".join(agent_classes))
        code.append(")")
        code.append("")
        code.append("")
        code.append("def create_graph():")
        code.append(f'    """Create the multi-agent workflow graph for {architecture.project_name}."""')
        code.append("    ")
        code.append("    # Initialize agents")

        agent_instances = []
        for agent in architecture.agents:
            agent_class = agent.name.replace(" ", "")
            agent_var = agent.name.lower().replace(" ", "_")
            code.append(f"    {agent_var} = {agent_class}()")
            agent_instances.append((agent_var, agent.name, agent.role))

        code.append("    ")
        code.append("    # Create graph")
        code.append("    workflow = StateGraph(AgentState)")
        code.append("    ")
        code.append("    # Add nodes")

        for agent_var, agent_name, agent_role in agent_instances:
            node_name = agent_var
            code.append(f"    workflow.add_node('{node_name}', {agent_var}.invoke)")

        code.append("    ")
        code.append("    # Define edges")

        # Find master planner
        master_var = None
        specialist_vars = []
        for agent_var, agent_name, agent_role in agent_instances:
            if agent_role == AgentRole.MASTER_PLANNER:
                master_var = agent_var
            elif agent_role == AgentRole.SPECIALIST:
                specialist_vars.append(agent_var)

        if master_var:
            code.append(f"    # Start with master planner")
            code.append(f"    workflow.set_entry_point('{master_var}')")
            code.append("    ")

            if specialist_vars:
                code.append(f"    # Master delegates to specialists")
                for spec_var in specialist_vars[:2]:  # Limit connections
                    code.append(f"    workflow.add_edge('{master_var}', '{spec_var}')")

                code.append("    ")
                code.append(f"    # Specialists return to master")
                for spec_var in specialist_vars[:2]:
                    code.append(f"    workflow.add_edge('{spec_var}', '{master_var}')")
        else:
            # Simple linear flow
            if agent_instances:
                code.append(f"    workflow.set_entry_point('{agent_instances[0][0]}')")
                code.append(f"    workflow.add_edge('{agent_instances[0][0]}', END)")

        code.append("    ")
        code.append("    # Add conditional edges for dynamic routing")
        code.append("    def should_continue(state: AgentState) -> str:")
        code.append('        """Determine if workflow should continue."""')
        code.append("        if state.get('task_status') == 'completed':")
        code.append("            return 'end'")
        code.append("        return 'continue'")
        code.append("    ")

        if master_var:
            code.append(f"    workflow.add_conditional_edges(")
            code.append(f"        '{master_var}',")
            code.append(f"        should_continue,")
            code.append(f"        {{'continue': '{specialist_vars[0] if specialist_vars else master_var}', 'end': END}}")
            code.append(f"    )")

        code.append("    ")
        code.append("    # Compile graph with memory")
        code.append("    memory = MemorySaver()")
        code.append("    app = workflow.compile(checkpointer=memory)")
        code.append("    ")
        code.append("    return app")
        code.append("")

        return "\n".join(code)

    def _generate_main_module(self, architecture: SystemArchitecture) -> str:
        """Generate main entry point."""
        code = []
        code.append('"""')
        code.append(f"Main entry point for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("from langchain_core.messages import HumanMessage")
        code.append("from .graph import create_graph")
        code.append("from .state import AgentState")
        code.append("from .config import config")
        code.append("")
        code.append("")
        code.append("def run_agent_system(task: str) -> dict:")
        code.append(f'    """')
        code.append(f"    Run the {architecture.project_name} agent system.")
        code.append("    ")
        code.append("    Args:")
        code.append("        task: The task to execute")
        code.append("    ")
        code.append("    Returns:")
        code.append("        Final state with results")
        code.append('    """')
        code.append("    # Create graph")
        code.append("    app = create_graph()")
        code.append("    ")
        code.append("    # Initial state")
        code.append("    initial_state: AgentState = {")
        code.append("        'messages': [HumanMessage(content=task)],")
        code.append("        'current_task': task,")
        code.append("        'task_status': 'pending',")
        code.append("        'completed_tasks': [],")
        code.append("        'next_agent': '',")
        code.append("        'delegation_history': [],")
        code.append("        'tool_results': {},")
        code.append("    }")
        code.append("    ")
        code.append("    # Run graph")
        code.append("    config_dict = {'configurable': {'thread_id': '1'}}")
        code.append("    ")
        code.append("    final_state = None")
        code.append("    for output in app.stream(initial_state, config_dict):")
        code.append("        for key, value in output.items():")
        code.append("            print(f'Agent: {key}')")
        code.append("            print(f'Output: {value}\\n')")
        code.append("        final_state = value")
        code.append("    ")
        code.append("    return final_state")
        code.append("")
        code.append("")
        code.append("if __name__ == '__main__':")
        code.append(f'    # Example task')
        code.append(f"    task = \"{architecture.description}\"")
        code.append("    ")
        code.append("    print(f'Starting task: {task}\\n')")
        code.append("    result = run_agent_system(task)")
        code.append("    ")
        code.append("    print('\\n=== Final Result ===')")
        code.append("    print(result)")
        code.append("")

        return "\n".join(code)

    def _generate_config_module(self, architecture: SystemArchitecture) -> str:
        """Generate configuration module."""
        code = []
        code.append('"""')
        code.append(f"Configuration for {architecture.project_name}.")
        code.append('"""')
        code.append("")
        code.append("import os")
        code.append("from typing import Dict")
        code.append("")
        code.append("")
        code.append("class Config:")
        code.append('    """Configuration settings."""')
        code.append("    ")
        code.append("    # API Keys")
        code.append("    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')")
        code.append("    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '')")
        code.append("    ")
        code.append("    # Model settings")
        code.append("    DEFAULT_MODEL = 'gpt-4'")
        code.append("    TEMPERATURE = 0")
        code.append("    ")
        code.append("    # Agent settings")
        code.append(f"    PROJECT_NAME = '{architecture.project_name}'")
        code.append(f"    NUM_AGENTS = {len(architecture.agents)}")
        code.append("    ")
        code.append("    # Reflection settings")

        has_reflection = any(ComponentType.REFLECTION in agent.components
                           for agent in architecture.agents)
        code.append(f"    ENABLE_REFLECTION = {has_reflection}")
        code.append("    REFLECTION_INTERVAL = 5  # Reflect every N steps")
        code.append("    ")
        code.append("    # Planning settings")
        has_planning = any(ComponentType.PLANNING in agent.components
                         for agent in architecture.agents)
        code.append(f"    ENABLE_PLANNING = {has_planning}")
        code.append("    MAX_PLANNING_DEPTH = 3")
        code.append("    ")
        code.append("    @classmethod")
        code.append("    def validate(cls) -> bool:")
        code.append('        """Validate configuration."""')
        code.append("        if not cls.OPENAI_API_KEY:")
        code.append("            print('Warning: OPENAI_API_KEY not set')")
        code.append("            return False")
        code.append("        return True")
        code.append("")
        code.append("")
        code.append("config = Config()")
        code.append("")

        return "\n".join(code)


def format_langgraph_code(files: Dict[str, str]) -> str:
    """Format generated LangGraph code for display."""
    output = []

    output.append("# Generated LangGraph Implementation")
    output.append("")

    for filename, code in files.items():
        output.append(f"## {filename}")
        output.append("")
        output.append("```python")
        output.append(code)
        output.append("```")
        output.append("")

    return "\n".join(output)
