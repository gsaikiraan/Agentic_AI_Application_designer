"""
Architecture designer for agentic AI applications.
Generates detailed architecture designs based on requirements analysis.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from ..analyzer import AnalysisResult, SystemRequirements
from ..framework import (
    ComponentType,
    AgentRole,
    DesignPattern,
    CORE_COMPONENTS,
    AGENT_ROLES,
    DESIGN_PATTERNS
)


@dataclass
class AgentArchitecture:
    """Architecture definition for an individual agent."""
    name: str
    role: AgentRole
    responsibilities: List[str]
    components: List[ComponentType]
    tools: List[str] = field(default_factory=list)
    communication_interfaces: List[str] = field(default_factory=list)


@dataclass
class SystemArchitecture:
    """Complete system architecture definition."""
    project_name: str
    description: str
    agents: List[AgentArchitecture]
    patterns: List[DesignPattern]
    components: Dict[ComponentType, Dict[str, any]]
    communication_topology: str
    data_flow: List[str]
    deployment_considerations: List[str]


class ArchitectureDesigner:
    """Designs system architecture based on requirements analysis."""

    def design(self, analysis_result: AnalysisResult) -> SystemArchitecture:
        """
        Generate system architecture from analysis result.

        Args:
            analysis_result: Results from requirements analysis

        Returns:
            Complete system architecture
        """
        requirements = analysis_result.requirements

        # Design agents
        agents = self._design_agents(
            requirements,
            analysis_result.recommended_agent_roles
        )

        # Configure components
        components = self._configure_components(
            analysis_result.recommended_components,
            requirements
        )

        # Determine communication topology
        topology = self._determine_topology(requirements, agents)

        # Design data flow
        data_flow = self._design_data_flow(agents, requirements)

        # Deployment considerations
        deployment = self._generate_deployment_considerations(requirements)

        return SystemArchitecture(
            project_name=requirements.project_name,
            description=requirements.description,
            agents=agents,
            patterns=analysis_result.recommended_patterns,
            components=components,
            communication_topology=topology,
            data_flow=data_flow,
            deployment_considerations=deployment
        )

    def _design_agents(
        self,
        requirements: SystemRequirements,
        recommended_roles: List[AgentRole]
    ) -> List[AgentArchitecture]:
        """Design individual agents based on requirements."""
        agents = []

        # Create agents based on recommended roles
        for role in recommended_roles:
            if role == AgentRole.MASTER_PLANNER:
                agents.append(self._create_master_planner(requirements))
            elif role == AgentRole.SPECIALIST:
                agents.extend(self._create_specialists(requirements))
            elif role == AgentRole.COMMUNICATION_FACILITATOR:
                agents.append(self._create_communication_facilitator(requirements))
            elif role == AgentRole.REFLECTIVE_OBSERVER:
                agents.append(self._create_reflective_observer(requirements))

        return agents

    def _create_master_planner(self, requirements: SystemRequirements) -> AgentArchitecture:
        """Create master planner agent architecture."""
        agent_def = AGENT_ROLES[AgentRole.MASTER_PLANNER]

        return AgentArchitecture(
            name="Master Planner",
            role=AgentRole.MASTER_PLANNER,
            responsibilities=agent_def.responsibilities + [
                f"Coordinate {requirements.num_agents} agents in the system",
                "Allocate tasks based on agent specializations"
            ],
            components=agent_def.components,
            tools=["Task Queue", "Resource Manager", "Performance Monitor"],
            communication_interfaces=[
                "Task Distribution Interface",
                "Status Collection Interface",
                "Directive Broadcast Channel"
            ]
        )

    def _create_specialists(self, requirements: SystemRequirements) -> List[AgentArchitecture]:
        """Create specialist agents based on required specializations."""
        specialists = []
        agent_def = AGENT_ROLES[AgentRole.SPECIALIST]

        if requirements.agent_specializations:
            # Create specialists for each specialization
            for i, specialization in enumerate(requirements.agent_specializations):
                specialist = AgentArchitecture(
                    name=f"{specialization} Specialist",
                    role=AgentRole.SPECIALIST,
                    responsibilities=agent_def.responsibilities + [
                        f"Execute {specialization}-specific tasks",
                        f"Maintain expertise in {specialization} domain"
                    ],
                    components=agent_def.components,
                    tools=self._select_tools_for_specialization(
                        specialization,
                        requirements.required_tools
                    ),
                    communication_interfaces=[
                        "Task Reception Interface",
                        "Status Reporting Interface",
                        "Peer Collaboration Channel"
                    ]
                )
                specialists.append(specialist)
        else:
            # Create a general specialist
            specialist = AgentArchitecture(
                name="General Specialist",
                role=AgentRole.SPECIALIST,
                responsibilities=agent_def.responsibilities,
                components=agent_def.components,
                tools=requirements.required_tools,
                communication_interfaces=[
                    "Task Reception Interface",
                    "Status Reporting Interface"
                ]
            )
            specialists.append(specialist)

        return specialists

    def _create_communication_facilitator(
        self,
        requirements: SystemRequirements
    ) -> AgentArchitecture:
        """Create communication facilitator agent."""
        agent_def = AGENT_ROLES[AgentRole.COMMUNICATION_FACILITATOR]

        return AgentArchitecture(
            name="Communication Facilitator",
            role=AgentRole.COMMUNICATION_FACILITATOR,
            responsibilities=agent_def.responsibilities + [
                "Route messages between agents efficiently",
                "Detect and resolve communication deadlocks"
            ],
            components=agent_def.components,
            tools=["Message Router", "Protocol Validator", "Conflict Resolver"],
            communication_interfaces=[
                "All Agent Communication Channels",
                "Protocol Management Interface"
            ]
        )

    def _create_reflective_observer(
        self,
        requirements: SystemRequirements
    ) -> AgentArchitecture:
        """Create reflective observer agent."""
        agent_def = AGENT_ROLES[AgentRole.REFLECTIVE_OBSERVER]

        return AgentArchitecture(
            name="Reflective Observer",
            role=AgentRole.REFLECTIVE_OBSERVER,
            responsibilities=agent_def.responsibilities + [
                "Track system-wide performance metrics",
                "Identify bottlenecks and inefficiencies"
            ],
            components=agent_def.components,
            tools=["Metrics Aggregator", "Analytics Engine", "Alert System"],
            communication_interfaces=[
                "Monitoring Data Collection Channel",
                "Advisory Broadcast Interface"
            ]
        )

    def _select_tools_for_specialization(
        self,
        specialization: str,
        available_tools: List[str]
    ) -> List[str]:
        """Select relevant tools for a specialization."""
        # Simple keyword matching for tool selection
        specialization_lower = specialization.lower()
        relevant_tools = []

        for tool in available_tools:
            if any(keyword in tool.lower() for keyword in specialization_lower.split()):
                relevant_tools.append(tool)

        # If no specific match, return all tools
        return relevant_tools if relevant_tools else available_tools

    def _configure_components(
        self,
        component_types: List[ComponentType],
        requirements: SystemRequirements
    ) -> Dict[ComponentType, Dict]:
        """Configure architectural components with specific parameters."""
        components = {}

        for comp_type in component_types:
            component_def = CORE_COMPONENTS[comp_type]
            config = {
                "name": component_def.name,
                "description": component_def.description,
                "capabilities": component_def.capabilities,
                "implementation_notes": component_def.implementation_considerations,
                "configuration": self._generate_component_config(comp_type, requirements)
            }
            components[comp_type] = config

        return components

    def _generate_component_config(
        self,
        comp_type: ComponentType,
        requirements: SystemRequirements
    ) -> Dict:
        """Generate specific configuration for a component."""
        if comp_type == ComponentType.REFLECTION:
            return {
                "reflection_frequency": "event-driven",
                "metrics": ["task_success_rate", "execution_time", "resource_usage"],
                "triggers": ["task_completion", "error_occurrence", "performance_threshold"]
            }
        elif comp_type == ComponentType.PLANNING:
            return {
                "planning_horizon": "adaptive",
                "decomposition_strategy": "hierarchical",
                "replanning_threshold": "0.3"  # 30% deviation triggers replanning
            }
        elif comp_type == ComponentType.COMMUNICATION:
            return {
                "protocol": "message_passing",
                "message_format": "json",
                "delivery_guarantee": "at_least_once",
                "max_message_size": "1MB"
            }
        elif comp_type == ComponentType.EXECUTION:
            return {
                "execution_mode": "asynchronous",
                "timeout": "configurable_per_task",
                "retry_policy": "exponential_backoff"
            }
        elif comp_type == ComponentType.TOOL_INTEGRATION:
            return {
                "tool_registry": "dynamic",
                "invocation_pattern": "adapter",
                "error_handling": "circuit_breaker",
                "caching": "enabled"
            }
        return {}

    def _determine_topology(
        self,
        requirements: SystemRequirements,
        agents: List[AgentArchitecture]
    ) -> str:
        """Determine communication topology for the system."""
        if not requirements.needs_multi_agent:
            return "Standalone (single agent)"

        # Check if we have a master planner
        has_master = any(a.role == AgentRole.MASTER_PLANNER for a in agents)

        if has_master:
            if len(agents) > 5:
                return "Hierarchical with Communication Facilitator (star topology with routing)"
            else:
                return "Hierarchical (star topology centered on Master Planner)"
        else:
            if len(agents) <= 3:
                return "Peer-to-peer (full mesh)"
            else:
                return "Hybrid (partial mesh with designated coordinators)"

    def _design_data_flow(
        self,
        agents: List[AgentArchitecture],
        requirements: SystemRequirements
    ) -> List[str]:
        """Design data flow patterns in the system."""
        flows = []

        # Check for master planner
        has_master = any(a.role == AgentRole.MASTER_PLANNER for a in agents)

        if has_master:
            flows.append("User Request → Master Planner (task decomposition)")
            flows.append("Master Planner → Specialists (task delegation)")
            flows.append("Specialists → External Tools (tool invocation)")
            flows.append("Specialists → Master Planner (status updates)")
            flows.append("Master Planner → User (aggregated results)")

        if any(a.role == AgentRole.REFLECTIVE_OBSERVER for a in agents):
            flows.append("All Agents → Reflective Observer (performance metrics)")
            flows.append("Reflective Observer → Master Planner (optimization recommendations)")

        if any(a.role == AgentRole.COMMUNICATION_FACILITATOR for a in agents):
            flows.append("All Agent Messages → Communication Facilitator (routing)")

        if requirements.needs_reflection:
            flows.append("Execution Engine → Reflection Module (execution feedback)")
            flows.append("Reflection Module → Planning Module (adaptation signals)")

        return flows

    def _generate_deployment_considerations(
        self,
        requirements: SystemRequirements
    ) -> List[str]:
        """Generate deployment considerations."""
        considerations = []

        considerations.append(f"System Complexity: {requirements.complexity.value}")
        considerations.append(f"Number of Agents: {requirements.num_agents}")

        if requirements.scalability_needs == "high":
            considerations.append("Deploy agents in containerized environment (Docker/Kubernetes)")
            considerations.append("Use message queue for agent communication (RabbitMQ/Kafka)")
            considerations.append("Implement horizontal scaling for specialist agents")

        if requirements.reliability_requirements == "high":
            considerations.append("Implement agent health monitoring and auto-restart")
            considerations.append("Use persistent message queues for fault tolerance")
            considerations.append("Deploy redundant instances of critical agents")

        if requirements.performance_requirements == "high":
            considerations.append("Use asynchronous communication patterns")
            considerations.append("Implement caching for frequently accessed data")
            considerations.append("Optimize agent placement based on communication patterns")

        if len(requirements.required_tools) > 0:
            considerations.append("Ensure network access to external APIs and services")
            considerations.append("Implement API key management and rotation")
            considerations.append("Set up monitoring for external service dependencies")

        return considerations


def format_architecture(architecture: SystemArchitecture) -> str:
    """
    Format architecture as human-readable text.

    Args:
        architecture: System architecture to format

    Returns:
        Formatted architecture description
    """
    output = []

    output.append(f"# Architecture Design: {architecture.project_name}")
    output.append(f"\n{architecture.description}\n")

    # Patterns
    output.append("\n## Design Patterns")
    for pattern in architecture.patterns:
        output.append(f"- {pattern.value.replace('_', ' ').title()}")

    # Agents
    output.append(f"\n## Agent Architecture ({len(architecture.agents)} agents)\n")
    for agent in architecture.agents:
        output.append(f"### {agent.name}")
        output.append(f"**Role:** {agent.role.value.replace('_', ' ').title()}\n")
        output.append("**Responsibilities:**")
        for resp in agent.responsibilities:
            output.append(f"- {resp}")
        output.append("\n**Components:**")
        for comp in agent.components:
            output.append(f"- {comp.value.replace('_', ' ').title()}")
        if agent.tools:
            output.append("\n**Tools:**")
            for tool in agent.tools:
                output.append(f"- {tool}")
        output.append("")

    # Components
    output.append("\n## System Components\n")
    for comp_type, config in architecture.components.items():
        output.append(f"### {config['name']}")
        output.append(f"{config['description']}\n")
        output.append("**Configuration:**")
        for key, value in config['configuration'].items():
            output.append(f"- {key}: {value}")
        output.append("")

    # Communication
    output.append(f"\n## Communication Topology\n{architecture.communication_topology}\n")

    # Data Flow
    output.append("\n## Data Flow\n")
    for flow in architecture.data_flow:
        output.append(f"- {flow}")

    # Deployment
    output.append("\n## Deployment Considerations\n")
    for consideration in architecture.deployment_considerations:
        output.append(f"- {consideration}")

    return "\n".join(output)
