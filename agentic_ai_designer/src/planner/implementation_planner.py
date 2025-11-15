"""
Implementation planner for agentic AI applications.
Generates detailed implementation plans with phases, tasks, and code examples.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from ..designer import SystemArchitecture
from ..framework import (
    ComponentType,
    DesignPattern,
    get_implementation_guidelines,
    get_challenges,
    DESIGN_PATTERNS
)


@dataclass
class ImplementationTask:
    """Individual implementation task."""
    task_id: str
    title: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    estimated_effort: str = "medium"
    code_example: str = ""
    testing_considerations: List[str] = field(default_factory=list)


@dataclass
class ImplementationPhase:
    """Implementation phase containing related tasks."""
    phase_number: int
    name: str
    description: str
    tasks: List[ImplementationTask]
    deliverables: List[str]


@dataclass
class ImplementationPlan:
    """Complete implementation plan for the system."""
    project_name: str
    phases: List[ImplementationPhase]
    technology_stack: Dict[str, List[str]]
    best_practices: List[str]
    testing_strategy: List[str]
    risk_mitigation: List[str]
    next_steps: List[str]


class ImplementationPlanner:
    """Generates detailed implementation plans."""

    def create_plan(self, architecture: SystemArchitecture) -> ImplementationPlan:
        """
        Create implementation plan from architecture design.

        Args:
            architecture: System architecture

        Returns:
            Detailed implementation plan
        """
        # Generate implementation phases
        phases = self._generate_phases(architecture)

        # Recommend technology stack
        tech_stack = self._recommend_technology_stack(architecture)

        # Compile best practices
        best_practices = self._compile_best_practices(architecture)

        # Define testing strategy
        testing_strategy = self._define_testing_strategy(architecture)

        # Risk mitigation strategies
        risk_mitigation = self._generate_risk_mitigation(architecture)

        # Next steps
        next_steps = self._generate_next_steps()

        return ImplementationPlan(
            project_name=architecture.project_name,
            phases=phases,
            technology_stack=tech_stack,
            best_practices=best_practices,
            testing_strategy=testing_strategy,
            risk_mitigation=risk_mitigation,
            next_steps=next_steps
        )

    def _generate_phases(self, architecture: SystemArchitecture) -> List[ImplementationPhase]:
        """Generate implementation phases."""
        phases = []

        # Phase 1: Foundation
        phases.append(self._create_foundation_phase(architecture))

        # Phase 2: Core Components
        phases.append(self._create_components_phase(architecture))

        # Phase 3: Agent Implementation
        phases.append(self._create_agents_phase(architecture))

        # Phase 4: Integration
        phases.append(self._create_integration_phase(architecture))

        # Phase 5: Testing and Optimization
        phases.append(self._create_testing_phase(architecture))

        return phases

    def _create_foundation_phase(self, architecture: SystemArchitecture) -> ImplementationPhase:
        """Create foundation setup phase."""
        tasks = []

        # Project setup
        tasks.append(ImplementationTask(
            task_id="1.1",
            title="Project Structure Setup",
            description="Create project directory structure and configuration files",
            estimated_effort="small",
            code_example="""
# Recommended project structure
project_root/
├── src/
│   ├── agents/
│   ├── components/
│   │   ├── reflection/
│   │   ├── planning/
│   │   ├── communication/
│   │   ├── execution/
│   │   └── tools/
│   ├── config/
│   └── utils/
├── tests/
├── docs/
├── requirements.txt
└── README.md
            """,
            testing_considerations=[
                "Verify directory structure is created correctly",
                "Ensure configuration files are valid"
            ]
        ))

        # Dependency management
        tasks.append(ImplementationTask(
            task_id="1.2",
            title="Install Core Dependencies",
            description="Set up Python environment and install required packages",
            dependencies=["1.1"],
            estimated_effort="small",
            code_example="""
# requirements.txt
# LangChain and LangGraph for agentic AI
langchain>=0.1.0
langchain-core>=0.1.0
langgraph>=0.0.50
langchain-openai>=0.0.5
langchain-community>=0.0.20

# Additional tools
tavily-python>=0.3.0  # Web search
pydantic>=2.0.0
python-dotenv>=1.0.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
            """,
            testing_considerations=[
                "Verify all dependencies install successfully",
                "Check for version conflicts"
            ]
        ))

        # Configuration system
        tasks.append(ImplementationTask(
            task_id="1.3",
            title="Implement Configuration System",
            description="Create configuration management for agents and components",
            dependencies=["1.2"],
            estimated_effort="medium",
            code_example="""
# config/base_config.py
from pydantic import BaseModel
from typing import Dict, List

class AgentConfig(BaseModel):
    name: str
    role: str
    max_iterations: int = 10
    timeout: float = 30.0

class SystemConfig(BaseModel):
    agents: List[AgentConfig]
    communication_protocol: str = "message_queue"
    log_level: str = "INFO"

# Load from environment or file
config = SystemConfig.from_yaml("config.yaml")
            """,
            testing_considerations=[
                "Test configuration loading from files",
                "Validate configuration schema",
                "Test environment variable overrides"
            ]
        ))

        return ImplementationPhase(
            phase_number=1,
            name="Foundation Setup",
            description="Establish project infrastructure and development environment",
            tasks=tasks,
            deliverables=[
                "Project structure created",
                "Development environment configured",
                "Configuration system implemented"
            ]
        )

    def _create_components_phase(self, architecture: SystemArchitecture) -> ImplementationPhase:
        """Create core components implementation phase."""
        tasks = []

        # Reflection module
        if ComponentType.REFLECTION in architecture.components:
            tasks.append(ImplementationTask(
                task_id="2.1",
                title="Implement Reflection Module",
                description="Create self-monitoring and evaluation capabilities",
                dependencies=["1.3"],
                estimated_effort="large",
                code_example="""
# components/reflection/reflector.py
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ReflectionResult:
    agent_id: str
    performance_metrics: Dict[str, float]
    issues_detected: List[str]
    recommendations: List[str]

class ReflectionModule:
    def __init__(self, metrics_config: Dict):
        self.metrics_config = metrics_config
        self.history = []

    async def reflect(self, execution_context: Dict) -> ReflectionResult:
        \"\"\"Perform reflection on recent execution.\"\"\"
        # Analyze performance metrics
        metrics = self._compute_metrics(execution_context)

        # Detect issues
        issues = self._detect_issues(metrics)

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, issues)

        result = ReflectionResult(
            agent_id=execution_context['agent_id'],
            performance_metrics=metrics,
            issues_detected=issues,
            recommendations=recommendations
        )

        self.history.append(result)
        return result

    def _compute_metrics(self, context: Dict) -> Dict[str, float]:
        return {
            'success_rate': context.get('successes', 0) / max(context.get('attempts', 1), 1),
            'avg_execution_time': context.get('total_time', 0) / max(context.get('attempts', 1), 1),
            'error_rate': context.get('errors', 0) / max(context.get('attempts', 1), 1)
        }

    def _detect_issues(self, metrics: Dict[str, float]) -> List[str]:
        issues = []
        if metrics['success_rate'] < 0.8:
            issues.append("Low success rate detected")
        if metrics['avg_execution_time'] > 5.0:
            issues.append("High execution time detected")
        return issues

    def _generate_recommendations(self, metrics: Dict, issues: List[str]) -> List[str]:
        recommendations = []
        if "Low success rate" in issues:
            recommendations.append("Review error handling and retry logic")
        if "High execution time" in issues:
            recommendations.append("Consider optimization or parallel execution")
        return recommendations
                """,
                testing_considerations=[
                    "Unit test metric computation",
                    "Test issue detection thresholds",
                    "Verify recommendation generation",
                    "Test reflection history storage"
                ]
            ))

        # Planning module
        if ComponentType.PLANNING in architecture.components:
            tasks.append(ImplementationTask(
                task_id="2.2",
                title="Implement Planning Module",
                description="Create hierarchical task decomposition and planning",
                dependencies=["1.3"],
                estimated_effort="large",
                code_example="""
# components/planning/planner.py
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    task_id: str
    description: str
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List['Task'] = None
    dependencies: List[str] = None

    def __post_init__(self):
        self.subtasks = self.subtasks or []
        self.dependencies = self.dependencies or []

class PlanningModule:
    def __init__(self):
        self.tasks = {}

    def decompose_goal(self, goal: str, context: Dict) -> List[Task]:
        \"\"\"Decompose high-level goal into executable tasks.\"\"\"
        # This is a simplified example - real implementation would use
        # LLM or more sophisticated planning algorithm

        tasks = []
        # Example decomposition logic
        if "multi-step" in goal.lower():
            # Create hierarchical task structure
            main_task = Task(
                task_id=f"task_{len(self.tasks)}",
                description=goal,
                status=TaskStatus.PENDING
            )

            # Decompose into subtasks
            subtasks = self._generate_subtasks(goal, context)
            main_task.subtasks = subtasks

            self.tasks[main_task.task_id] = main_task
            tasks.append(main_task)

        return tasks

    def _generate_subtasks(self, goal: str, context: Dict) -> List[Task]:
        # Simplified subtask generation
        return [
            Task(task_id=f"subtask_{i}", description=f"Step {i+1} of {goal}")
            for i in range(3)
        ]

    def replan(self, task_id: str, reflection_result) -> List[Task]:
        \"\"\"Replan based on reflection feedback.\"\"\"
        task = self.tasks.get(task_id)
        if not task:
            return []

        # Analyze reflection and adjust plan
        if reflection_result.issues_detected:
            # Create alternative approach
            new_tasks = self._create_alternative_plan(task, reflection_result)
            return new_tasks

        return []
                """,
                testing_considerations=[
                    "Test goal decomposition logic",
                    "Verify task dependency handling",
                    "Test replanning triggers",
                    "Validate task status transitions"
                ]
            ))

        # Communication layer
        if ComponentType.COMMUNICATION in architecture.components:
            tasks.append(ImplementationTask(
                task_id="2.3",
                title="Implement Communication Layer",
                description="Create message passing and coordination protocols",
                dependencies=["1.3"],
                estimated_effort="large",
                code_example="""
# components/communication/message_bus.py
import asyncio
from typing import Dict, Callable, List
from dataclasses import dataclass
from enum import Enum

class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3

@dataclass
class Message:
    sender: str
    receiver: str
    content: Dict
    priority: MessagePriority = MessagePriority.NORMAL
    correlation_id: str = None

class MessageBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_queue = asyncio.Queue()

    def subscribe(self, agent_id: str, handler: Callable):
        \"\"\"Subscribe agent to receive messages.\"\"\"
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(handler)

    async def publish(self, message: Message):
        \"\"\"Publish message to receiver.\"\"\"
        await self.message_queue.put(message)

    async def start(self):
        \"\"\"Start message processing loop.\"\"\"
        while True:
            message = await self.message_queue.get()
            await self._deliver_message(message)

    async def _deliver_message(self, message: Message):
        \"\"\"Deliver message to subscribed handlers.\"\"\"
        handlers = self.subscribers.get(message.receiver, [])

        for handler in handlers:
            try:
                await handler(message)
            except Exception as e:
                print(f"Error delivering message: {e}")
                """,
                testing_considerations=[
                    "Test message routing to correct agents",
                    "Verify message priority handling",
                    "Test error handling for failed deliveries",
                    "Validate message queue performance"
                ]
            ))

        # Tool integration
        if ComponentType.TOOL_INTEGRATION in architecture.components:
            tasks.append(ImplementationTask(
                task_id="2.4",
                title="Implement Tool Integration Interface",
                description="Create adapter pattern for external tool integration",
                dependencies=["1.3"],
                estimated_effort="medium",
                code_example="""
# components/tools/tool_manager.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    data: Any
    error: str = None

class Tool(ABC):
    \"\"\"Base class for all tools.\"\"\"

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        pass

    @abstractmethod
    def get_schema(self) -> Dict:
        \"\"\"Return tool parameter schema.\"\"\"
        pass

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, name: str, tool: Tool):
        \"\"\"Register a tool for use by agents.\"\"\"
        self.tools[name] = tool

    async def execute_tool(self, name: str, **kwargs) -> ToolResult:
        \"\"\"Execute a tool by name.\"\"\"
        if name not in self.tools:
            return ToolResult(success=False, data=None, error=f"Tool {name} not found")

        try:
            result = await self.tools[name].execute(**kwargs)
            return result
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))

    def list_tools(self) -> List[Dict]:
        \"\"\"List all available tools with schemas.\"\"\"
        return [
            {"name": name, "schema": tool.get_schema()}
            for name, tool in self.tools.items()
        ]

# Example tool implementation
class WebSearchTool(Tool):
    async def execute(self, query: str) -> ToolResult:
        # Implement actual web search
        results = await self._search(query)
        return ToolResult(success=True, data=results)

    def get_schema(self) -> Dict:
        return {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "query": {"type": "string", "required": True}
            }
        }
                """,
                testing_considerations=[
                    "Test tool registration and discovery",
                    "Verify tool execution with various inputs",
                    "Test error handling for tool failures",
                    "Validate tool schema generation"
                ]
            ))

        return ImplementationPhase(
            phase_number=2,
            name="Core Components Implementation",
            description="Build fundamental architectural components",
            tasks=tasks,
            deliverables=[
                "Reflection module implemented",
                "Planning module implemented",
                "Communication layer implemented",
                "Tool integration interface implemented"
            ]
        )

    def _create_agents_phase(self, architecture: SystemArchitecture) -> ImplementationPhase:
        """Create agent implementation phase."""
        tasks = []

        tasks.append(ImplementationTask(
            task_id="3.1",
            title="Implement Base Agent with LangGraph",
            description="Create base agent using LangGraph and LangChain",
            dependencies=["2.1", "2.2", "2.3"],
            estimated_effort="large",
            code_example="""
# agents/base_agent.py
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    \"\"\"Shared state for LangGraph agents.\"\"\"
    messages: Annotated[List, add_messages]
    current_task: str
    next_agent: str
    reflection_data: dict
    tool_results: dict

class BaseAgent:
    def __init__(
        self,
        agent_id: str,
        role: str,
        model: str = "gpt-4"
    ):
        self.agent_id = agent_id
        self.role = role
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.tools = self._get_tools()

        # Bind tools to LLM if available
        if self.tools:
            self.llm = self.llm.bind_tools(self.tools)

    def _get_tools(self) -> list:
        \"\"\"Get tools for this agent role. Override in subclasses.\"\"\"
        return []

    def get_system_prompt(self) -> str:
        \"\"\"Get system prompt for this agent.\"\"\"
        return f\"You are {self.agent_id}, a {self.role} agent in a multi-agent system.\"

    def invoke(self, state: AgentState) -> AgentState:
        \"\"\"Main agent execution - called by LangGraph.\"\"\"
        # Prepare messages with system prompt
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            *state['messages']
        ]

        # Invoke LLM
        response = self.llm.invoke(messages)

        # Return updated state
        return {
            'messages': [response],
            'next_agent': self.determine_next_agent(state, response)
        }

    def determine_next_agent(self, state: AgentState, response) -> str:
        \"\"\"Determine which agent should run next. Override in subclasses.\"\"\"
        return 'END'

# Example: Master Planner Agent
from langgraph.graph import StateGraph, END

class MasterPlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("master_planner", "coordinator")

    def get_system_prompt(self) -> str:
        return \"\"\"You are the Master Planner agent.

Your role is to:
1. Analyze incoming tasks
2. Break them into subtasks
3. Delegate to specialist agents
4. Coordinate overall workflow

Be strategic and efficient in your planning.\"\"\"

    def determine_next_agent(self, state: AgentState, response) -> str:
        # Route to appropriate specialist
        task = state.get('current_task', '')
        if 'research' in task.lower():
            return 'research_specialist'
        return 'END'
            """,
            testing_considerations=[
                "Test agent lifecycle (initialization, execution, cleanup)",
                "Verify message handling",
                "Test reflection integration",
                "Validate task execution flow"
            ]
        ))

        # Create specific agent implementations
        for i, agent in enumerate(architecture.agents):
            tasks.append(ImplementationTask(
                task_id=f"3.{i+2}",
                title=f"Implement {agent.name}",
                description=f"Create {agent.name} with role-specific capabilities",
                dependencies=["3.1"],
                estimated_effort="medium",
                testing_considerations=[
                    f"Test {agent.name} specific functionality",
                    "Verify integration with components",
                    "Test communication with other agents"
                ]
            ))

        return ImplementationPhase(
            phase_number=3,
            name="Agent Implementation",
            description="Implement individual agents with specific roles",
            tasks=tasks,
            deliverables=[
                "Base agent class implemented",
                f"All {len(architecture.agents)} agents implemented",
                "Agent communication verified"
            ]
        )

    def _create_integration_phase(self, architecture: SystemArchitecture) -> ImplementationPhase:
        """Create integration phase."""
        tasks = [
            ImplementationTask(
                task_id="4.1",
                title="Create LangGraph Workflow",
                description="Build the multi-agent workflow graph using LangGraph",
                dependencies=["3.1"] + [f"3.{i+2}" for i in range(len(architecture.agents))],
                estimated_effort="large",
                code_example="""
# workflow.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.base_agent import AgentState
from agents.master_planner import MasterPlannerAgent
from agents.specialist import SpecialistAgent

def create_workflow():
    \"\"\"Create the multi-agent workflow graph.\"\"\"

    # Initialize agents
    master = MasterPlannerAgent()
    specialist = SpecialistAgent()

    # Create graph
    workflow = StateGraph(AgentState)

    # Add agent nodes
    workflow.add_node("master_planner", master.invoke)
    workflow.add_node("specialist", specialist.invoke)

    # Define workflow edges
    workflow.set_entry_point("master_planner")

    # Add conditional routing
    def route_agent(state: AgentState) -> str:
        next_agent = state.get("next_agent", "END")
        return next_agent

    workflow.add_conditional_edges(
        "master_planner",
        route_agent,
        {
            "specialist": "specialist",
            "END": END
        }
    )

    workflow.add_edge("specialist", "master_planner")

    # Compile with checkpointing for memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app

# Usage
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    app = create_workflow()

    # Run the workflow
    config = {"configurable": {"thread_id": "1"}}
    inputs = {
        "messages": [HumanMessage(content="Research multi-agent AI systems")],
        "current_task": "Research multi-agent AI systems"
    }

    for output in app.stream(inputs, config):
        for key, value in output.items():
            print(f"Agent {key}: {value}")
                """,
                testing_considerations=[
                    "Test workflow graph construction",
                    "Verify agent routing logic",
                    "Test state persistence with checkpointer",
                    "Validate end-to-end agent collaboration"
                ]
            ),
            ImplementationTask(
                task_id="4.2",
                title="Implement Monitoring and Logging",
                description="Add observability to the system",
                dependencies=["4.1"],
                estimated_effort="medium",
                testing_considerations=[
                    "Verify log output format",
                    "Test metric collection",
                    "Validate alert triggers"
                ]
            )
        ]

        return ImplementationPhase(
            phase_number=4,
            name="System Integration",
            description="Integrate all components into cohesive system",
            tasks=tasks,
            deliverables=[
                "All components integrated",
                "Monitoring and logging implemented",
                "System ready for testing"
            ]
        )

    def _create_testing_phase(self, architecture: SystemArchitecture) -> ImplementationPhase:
        """Create testing and optimization phase."""
        tasks = [
            ImplementationTask(
                task_id="5.1",
                title="Unit Testing",
                description="Write comprehensive unit tests for all components",
                dependencies=["4.2"],
                estimated_effort="large",
                testing_considerations=[
                    "Achieve >80% code coverage",
                    "Test edge cases",
                    "Mock external dependencies"
                ]
            ),
            ImplementationTask(
                task_id="5.2",
                title="Integration Testing",
                description="Test multi-agent interactions and workflows",
                dependencies=["5.1"],
                estimated_effort="large",
                testing_considerations=[
                    "Test complete user scenarios",
                    "Verify agent collaboration",
                    "Test failure recovery"
                ]
            ),
            ImplementationTask(
                task_id="5.3",
                title="Performance Optimization",
                description="Profile and optimize system performance",
                dependencies=["5.2"],
                estimated_effort="medium",
                testing_considerations=[
                    "Measure response times",
                    "Identify bottlenecks",
                    "Optimize critical paths"
                ]
            )
        ]

        return ImplementationPhase(
            phase_number=5,
            name="Testing and Optimization",
            description="Comprehensive testing and performance tuning",
            tasks=tasks,
            deliverables=[
                "Unit tests passing with >80% coverage",
                "Integration tests passing",
                "System performance optimized"
            ]
        )

    def _recommend_technology_stack(self, architecture: SystemArchitecture) -> Dict[str, List[str]]:
        """Recommend technology stack."""
        stack = {
            "Core Framework": [
                "Python 3.11+",
                "LangChain or LlamaIndex (for agent orchestration)",
                "Pydantic (for data validation)"
            ],
            "Communication": [
                "Redis (message broker)",
                "RabbitMQ (alternative message queue)",
                "WebSockets (real-time communication)"
            ],
            "Storage": [
                "PostgreSQL (structured data)",
                "MongoDB (document storage)",
                "Redis (caching)"
            ],
            "Monitoring": [
                "Prometheus (metrics)",
                "Grafana (visualization)",
                "ELK Stack (logging)"
            ],
            "Testing": [
                "pytest (unit testing)",
                "pytest-asyncio (async testing)",
                "locust (load testing)"
            ],
            "Deployment": [
                "Docker (containerization)",
                "Kubernetes (orchestration)",
                "GitHub Actions (CI/CD)"
            ]
        }

        return stack

    def _compile_best_practices(self, architecture: SystemArchitecture) -> List[str]:
        """Compile best practices from framework."""
        practices = []

        # Get guidelines from framework
        guidelines = get_implementation_guidelines()
        for guideline in guidelines:
            practices.append(f"{guideline.category}: {guideline.guideline}")

        # Add pattern-specific practices
        for pattern in architecture.patterns:
            pattern_info = DESIGN_PATTERNS[pattern]
            practices.extend(pattern_info.best_practices)

        return list(set(practices))  # Remove duplicates

    def _define_testing_strategy(self, architecture: SystemArchitecture) -> List[str]:
        """Define comprehensive testing strategy."""
        return [
            "Unit Testing: Test each component in isolation with mocked dependencies",
            "Integration Testing: Test interactions between components and agents",
            "End-to-End Testing: Test complete user workflows",
            "Performance Testing: Measure response times and throughput under load",
            "Chaos Testing: Test system resilience to component failures",
            "Reflection Testing: Verify self-assessment and adaptation capabilities",
            "Communication Testing: Test message passing and coordination protocols",
            "Tool Testing: Verify external tool integrations with mocks and real APIs"
        ]

    def _generate_risk_mitigation(self, architecture: SystemArchitecture) -> List[str]:
        """Generate risk mitigation strategies."""
        risks = []

        challenges = get_challenges()
        for challenge_name, challenge_info in challenges.items():
            risks.append(
                f"{challenge_name}: {challenge_info['description']} - " +
                f"Mitigation: {'; '.join(challenge_info['mitigation_strategies'][:2])}"
            )

        return risks

    def _generate_next_steps(self) -> List[str]:
        """Generate next steps after implementation."""
        return [
            "1. Set up development environment and install dependencies",
            "2. Implement Phase 1 (Foundation) tasks",
            "3. Proceed with Phase 2 (Core Components) in parallel where possible",
            "4. Implement agents according to Phase 3",
            "5. Complete integration in Phase 4",
            "6. Execute comprehensive testing in Phase 5",
            "7. Deploy to staging environment for validation",
            "8. Gather feedback and iterate",
            "9. Deploy to production with monitoring",
            "10. Plan for continuous improvement based on reflection data"
        ]


def format_implementation_plan(plan: ImplementationPlan) -> str:
    """Format implementation plan as readable text."""
    output = []

    output.append(f"# Implementation Plan: {plan.project_name}\n")

    # Technology Stack
    output.append("## Recommended Technology Stack\n")
    for category, technologies in plan.technology_stack.items():
        output.append(f"### {category}")
        for tech in technologies:
            output.append(f"- {tech}")
        output.append("")

    # Implementation Phases
    output.append("\n## Implementation Phases\n")
    for phase in plan.phases:
        output.append(f"### Phase {phase.phase_number}: {phase.name}")
        output.append(f"{phase.description}\n")
        output.append("**Tasks:**")
        for task in phase.tasks:
            output.append(f"\n**[{task.task_id}] {task.title}** ({task.estimated_effort} effort)")
            output.append(f"{task.description}")
            if task.dependencies:
                output.append(f"*Dependencies: {', '.join(task.dependencies)}*")
            if task.code_example:
                output.append(f"```python{task.code_example}```")
        output.append(f"\n**Deliverables:**")
        for deliverable in phase.deliverables:
            output.append(f"- {deliverable}")
        output.append("\n---\n")

    # Testing Strategy
    output.append("\n## Testing Strategy\n")
    for strategy in plan.testing_strategy:
        output.append(f"- {strategy}")

    # Best Practices
    output.append("\n## Best Practices\n")
    for practice in plan.best_practices[:10]:  # Limit to top 10
        output.append(f"- {practice}")

    # Risk Mitigation
    output.append("\n## Risk Mitigation\n")
    for risk in plan.risk_mitigation:
        output.append(f"- {risk}")

    # Next Steps
    output.append("\n## Next Steps\n")
    for step in plan.next_steps:
        output.append(step)

    return "\n".join(output)
