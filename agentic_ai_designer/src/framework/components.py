"""
Core components and definitions from the Agentic AI Design Framework.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class ComponentType(Enum):
    """Types of architectural components in the framework."""
    REFLECTION = "reflection"
    PLANNING = "planning"
    COMMUNICATION = "communication"
    EXECUTION = "execution"
    TOOL_INTEGRATION = "tool_integration"


class AgentRole(Enum):
    """Agent roles in the hierarchical structure."""
    MASTER_PLANNER = "master_planner"
    SPECIALIST = "specialist"
    COMMUNICATION_FACILITATOR = "communication_facilitator"
    REFLECTIVE_OBSERVER = "reflective_observer"


@dataclass
class ArchitecturalComponent:
    """Represents a component in the agentic AI architecture."""
    name: str
    component_type: ComponentType
    description: str
    capabilities: List[str]
    dependencies: List[str] = field(default_factory=list)
    implementation_considerations: List[str] = field(default_factory=list)


@dataclass
class AgentDefinition:
    """Defines an agent in the multi-agent system."""
    role: AgentRole
    name: str
    responsibilities: List[str]
    components: List[ComponentType]
    communication_protocols: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)


# Define core architectural components
REFLECTION_MODULE = ArchitecturalComponent(
    name="Reflection Module",
    component_type=ComponentType.REFLECTION,
    description="Performs continuous self-monitoring and error detection",
    capabilities=[
        "Continuous self-monitoring and error detection",
        "Meta-cognition about states and intentions of peer agents",
        "Triggers replanning and strategy adjustments",
        "Detects discrepancies and suboptimal performance"
    ],
    dependencies=["Planning Module"],
    implementation_considerations=[
        "Efficient mechanisms to avoid overheads while maintaining responsiveness",
        "Design reflective loops to trigger only when significant discrepancies detected",
        "Balance between monitoring frequency and performance impact"
    ]
)

PLANNING_MODULE = ArchitecturalComponent(
    name="Planning Module",
    component_type=ComponentType.PLANNING,
    description="Facilitates decomposition of high-level goals into prioritized sub-tasks",
    capabilities=[
        "Decomposition of high-level goals into prioritized sub-tasks",
        "Recursive planning and resource allocation",
        "Bidirectional interface with reflection for dynamic adaptation",
        "Hierarchical task management"
    ],
    dependencies=["Reflection Module", "Communication Layer"],
    implementation_considerations=[
        "Support for dynamic replanning based on reflection feedback",
        "Efficient task decomposition algorithms",
        "Resource optimization and allocation strategies"
    ]
)

COMMUNICATION_LAYER = ArchitecturalComponent(
    name="Communication Layer",
    component_type=ComponentType.COMMUNICATION,
    description="Implements message passing and coordination protocols",
    capabilities=[
        "Message passing and shared data repositories",
        "Environment-based signaling",
        "Predefined and learned communication protocols",
        "Coordination and intention sharing",
        "Addresses partial observability challenges"
    ],
    dependencies=[],
    implementation_considerations=[
        "Balance expressiveness with bandwidth and latency constraints",
        "Support for both synchronous and asynchronous communication",
        "Harmonizing learned policies with hand-crafted protocols"
    ]
)

EXECUTION_ENGINE = ArchitecturalComponent(
    name="Execution Engine",
    component_type=ComponentType.EXECUTION,
    description="Carries out task-specific actions and monitors execution",
    capabilities=[
        "Executes task-specific actions",
        "Invokes external tools as required",
        "Monitors execution status",
        "Provides feedback to reflection modules"
    ],
    dependencies=["Tool Integration Interface", "Reflection Module"],
    implementation_considerations=[
        "Error handling and recovery mechanisms",
        "Execution monitoring and logging",
        "Performance optimization for task execution"
    ]
)

TOOL_INTEGRATION_INTERFACE = ArchitecturalComponent(
    name="Tool Integration Interface",
    component_type=ComponentType.TOOL_INTEGRATION,
    description="Middleware for connecting to external services",
    capabilities=[
        "Connect to external APIs, databases, search engines",
        "Domain-specific service integration",
        "Augment agent capabilities beyond internal logic",
        "Standardized tool invocation interface"
    ],
    dependencies=[],
    implementation_considerations=[
        "Modular design for easy addition of new tools",
        "Error handling for external service failures",
        "Rate limiting and quota management",
        "Security and authentication considerations"
    ]
)

# Core components registry
CORE_COMPONENTS = {
    ComponentType.REFLECTION: REFLECTION_MODULE,
    ComponentType.PLANNING: PLANNING_MODULE,
    ComponentType.COMMUNICATION: COMMUNICATION_LAYER,
    ComponentType.EXECUTION: EXECUTION_ENGINE,
    ComponentType.TOOL_INTEGRATION: TOOL_INTEGRATION_INTERFACE
}


# Define standard agent roles
MASTER_PLANNER_AGENT = AgentDefinition(
    role=AgentRole.MASTER_PLANNER,
    name="Master Planner Agent",
    responsibilities=[
        "Oversee global task management",
        "Optimize resource distribution",
        "Coordinate subordinate agents",
        "High-level strategic planning"
    ],
    components=[
        ComponentType.PLANNING,
        ComponentType.REFLECTION,
        ComponentType.COMMUNICATION
    ],
    communication_protocols=["broadcast", "direct_messaging", "task_delegation"]
)

SPECIALIST_AGENT = AgentDefinition(
    role=AgentRole.SPECIALIST,
    name="Specialist Agent",
    responsibilities=[
        "Focus on domain-specific tasks",
        "Execute specialized operations",
        "Maintain domain expertise",
        "Report progress to master planner"
    ],
    components=[
        ComponentType.EXECUTION,
        ComponentType.REFLECTION,
        ComponentType.PLANNING,
        ComponentType.TOOL_INTEGRATION,
        ComponentType.COMMUNICATION
    ],
    communication_protocols=["direct_messaging", "status_reporting"]
)

COMMUNICATION_FACILITATOR_AGENT = AgentDefinition(
    role=AgentRole.COMMUNICATION_FACILITATOR,
    name="Communication Facilitator Agent",
    responsibilities=[
        "Manage communication protocols",
        "Ensure message consistency",
        "Resolve communication conflicts",
        "Optimize information flow"
    ],
    components=[
        ComponentType.COMMUNICATION,
        ComponentType.REFLECTION
    ],
    communication_protocols=["all_protocols"]
)

REFLECTIVE_OBSERVER_AGENT = AgentDefinition(
    role=AgentRole.REFLECTIVE_OBSERVER,
    name="Reflective Observer Agent",
    responsibilities=[
        "Aggregate system-wide performance data",
        "Analyze collective reflection outputs",
        "Recommend strategic adjustments",
        "Monitor overall system health"
    ],
    components=[
        ComponentType.REFLECTION,
        ComponentType.COMMUNICATION
    ],
    communication_protocols=["monitoring", "advisory_messages"]
)

# Agent definitions registry
AGENT_ROLES = {
    AgentRole.MASTER_PLANNER: MASTER_PLANNER_AGENT,
    AgentRole.SPECIALIST: SPECIALIST_AGENT,
    AgentRole.COMMUNICATION_FACILITATOR: COMMUNICATION_FACILITATOR_AGENT,
    AgentRole.REFLECTIVE_OBSERVER: REFLECTIVE_OBSERVER_AGENT
}
