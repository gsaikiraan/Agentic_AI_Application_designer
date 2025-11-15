"""
Design patterns for agentic AI applications based on the framework.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class DesignPattern(Enum):
    """Core design patterns for agentic AI."""
    REFLECTION = "reflection"
    TOOL_USE = "tool_use"
    PLANNING = "planning"
    MULTI_AGENT_COLLABORATION = "multi_agent_collaboration"


@dataclass
class Pattern:
    """Represents a design pattern with implementation guidance."""
    name: str
    pattern_type: DesignPattern
    description: str
    key_principles: List[str]
    implementation_steps: List[str]
    challenges: List[str]
    best_practices: List[str]
    use_cases: List[str]


# Define the four foundational patterns

REFLECTION_PATTERN = Pattern(
    name="Reflection Pattern",
    pattern_type=DesignPattern.REFLECTION,
    description="Ongoing self-evaluation, error detection, and strategy adjustment",
    key_principles=[
        "Continuous monitoring of agent performance and behavior",
        "Meta-cognitive reasoning about internal states and decisions",
        "Adaptive strategy refinement based on reflection outcomes",
        "Evaluation of peer agents' states and intentions"
    ],
    implementation_steps=[
        "1. Design reflection triggers (time-based, event-based, performance-based)",
        "2. Implement performance metrics and success criteria",
        "3. Create self-assessment mechanisms for strategy evaluation",
        "4. Build feedback loops to planning and execution modules",
        "5. Implement meta-cognitive reasoning capabilities",
        "6. Design reflection storage and history tracking"
    ],
    challenges=[
        "Balancing reflection frequency with computational overhead",
        "Avoiding infinite reflection loops",
        "Determining when reflection should trigger replanning",
        "Managing state consistency during reflection"
    ],
    best_practices=[
        "Trigger reflection only on significant discrepancies or milestones",
        "Use lightweight metrics for continuous monitoring",
        "Implement hierarchical reflection (task-level, strategy-level, system-level)",
        "Cache reflection results to avoid redundant computations",
        "Design clear escalation paths from reflection to action"
    ],
    use_cases=[
        "Error detection and recovery in autonomous systems",
        "Strategy optimization in dynamic environments",
        "Quality assurance and self-improvement",
        "Coordination improvement in multi-agent systems"
    ]
)

TOOL_USE_PATTERN = Pattern(
    name="Tool Use Pattern",
    pattern_type=DesignPattern.TOOL_USE,
    description="Integration with external APIs, databases, and services to augment capabilities",
    key_principles=[
        "Extend agent capabilities beyond internal logic",
        "Provide standardized interfaces for tool access",
        "Enable dynamic tool discovery and selection",
        "Manage tool execution lifecycle and error handling"
    ],
    implementation_steps=[
        "1. Define tool interface abstraction layer",
        "2. Implement tool registry and discovery mechanism",
        "3. Create tool invocation and result handling logic",
        "4. Design error recovery and fallback strategies",
        "5. Implement authentication and authorization for external services",
        "6. Build tool performance monitoring and caching",
        "7. Create tool documentation and capability descriptions"
    ],
    challenges=[
        "Managing API rate limits and quotas",
        "Handling tool failures and timeouts gracefully",
        "Ensuring security in external service integration",
        "Balancing tool complexity vs. agent autonomy"
    ],
    best_practices=[
        "Use adapter pattern for tool integration",
        "Implement circuit breakers for external service calls",
        "Cache results where appropriate to reduce API calls",
        "Provide clear tool descriptions for agent decision-making",
        "Use async/await for non-blocking tool operations",
        "Implement comprehensive logging for tool usage"
    ],
    use_cases=[
        "Web search and information retrieval",
        "Database queries and data analysis",
        "API interactions for specialized services",
        "Code execution and computation",
        "Document processing and generation"
    ]
)

PLANNING_PATTERN = Pattern(
    name="Planning Pattern",
    pattern_type=DesignPattern.PLANNING,
    description="Hierarchical task decomposition and dynamic management of sub-tasks",
    key_principles=[
        "Decompose high-level goals into executable sub-tasks",
        "Support recursive and hierarchical planning",
        "Enable dynamic replanning based on feedback",
        "Optimize resource allocation and task scheduling"
    ],
    implementation_steps=[
        "1. Design goal representation and task decomposition logic",
        "2. Implement hierarchical task structure (goals -> tasks -> actions)",
        "3. Create task prioritization and scheduling algorithms",
        "4. Build resource allocation and constraint management",
        "5. Implement replanning triggers and adaptation mechanisms",
        "6. Design task dependency tracking and execution ordering",
        "7. Create plan validation and feasibility checking"
    ],
    challenges=[
        "Managing computational complexity of planning in large spaces",
        "Handling uncertainty and incomplete information",
        "Balancing planning depth vs. execution speed",
        "Coordinating plans across multiple agents"
    ],
    best_practices=[
        "Use hierarchical planning to manage complexity",
        "Implement iterative refinement of plans",
        "Support both reactive and deliberative planning modes",
        "Maintain plan history for learning and improvement",
        "Design clear interfaces between planning and execution",
        "Use heuristics to prune search space in complex planning"
    ],
    use_cases=[
        "Project management and task orchestration",
        "Resource scheduling and optimization",
        "Workflow automation and business processes",
        "Robot motion planning and navigation",
        "Strategic decision-making in complex domains"
    ]
)

MULTI_AGENT_COLLABORATION_PATTERN = Pattern(
    name="Multi-Agent Collaboration Pattern",
    pattern_type=DesignPattern.MULTI_AGENT_COLLABORATION,
    description="Communication and coordination mechanisms for division of labor and knowledge sharing",
    key_principles=[
        "Enable effective communication and coordination between agents",
        "Support division of labor based on agent specializations",
        "Facilitate knowledge and intention sharing",
        "Manage conflicts and ensure consistency"
    ],
    implementation_steps=[
        "1. Define agent roles and responsibilities",
        "2. Design communication protocols and message formats",
        "3. Implement coordination mechanisms (task allocation, negotiation)",
        "4. Create shared knowledge repositories or blackboards",
        "5. Build conflict resolution and consensus mechanisms",
        "6. Implement agent discovery and registration",
        "7. Design hierarchical or peer-to-peer organizational structures",
        "8. Create monitoring and visualization for multi-agent interactions"
    ],
    challenges=[
        "Managing communication overhead and bandwidth",
        "Avoiding deadlocks and coordination failures",
        "Ensuring coherent behavior in decentralized systems",
        "Handling agent failures and dynamic agent populations",
        "Learning effective communication policies"
    ],
    best_practices=[
        "Use message queues or publish-subscribe for scalable communication",
        "Implement hierarchical coordination to reduce complexity",
        "Design clear agent interfaces and contracts",
        "Use shared conventions to reduce explicit communication needs",
        "Implement heartbeat and health monitoring",
        "Support both synchronous and asynchronous communication patterns",
        "Design for graceful degradation when agents fail"
    ],
    use_cases=[
        "Distributed problem-solving systems",
        "Collaborative robotics and swarm systems",
        "Multi-agent simulations and games",
        "Distributed workflow management",
        "Collaborative decision support systems"
    ]
)

# Pattern registry
DESIGN_PATTERNS = {
    DesignPattern.REFLECTION: REFLECTION_PATTERN,
    DesignPattern.TOOL_USE: TOOL_USE_PATTERN,
    DesignPattern.PLANNING: PLANNING_PATTERN,
    DesignPattern.MULTI_AGENT_COLLABORATION: MULTI_AGENT_COLLABORATION_PATTERN
}


def get_pattern(pattern_type: DesignPattern) -> Pattern:
    """Retrieve a design pattern by type."""
    return DESIGN_PATTERNS[pattern_type]


def get_all_patterns() -> List[Pattern]:
    """Get all available design patterns."""
    return list(DESIGN_PATTERNS.values())


def get_patterns_for_use_case(use_case_keywords: List[str]) -> List[Pattern]:
    """
    Suggest relevant patterns based on use case keywords.

    Args:
        use_case_keywords: Keywords describing the use case

    Returns:
        List of relevant patterns
    """
    relevant_patterns = []
    keywords_lower = [kw.lower() for kw in use_case_keywords]

    for pattern in DESIGN_PATTERNS.values():
        # Check if any keyword matches pattern use cases or description
        pattern_text = (pattern.description + " " + " ".join(pattern.use_cases)).lower()
        if any(keyword in pattern_text for keyword in keywords_lower):
            relevant_patterns.append(pattern)

    return relevant_patterns if relevant_patterns else list(DESIGN_PATTERNS.values())
