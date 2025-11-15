"""
Requirements analyzer for agentic AI applications.
Analyzes user requirements and maps them to framework components.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set
from enum import Enum

from ..framework import (
    ComponentType,
    AgentRole,
    DesignPattern,
    get_patterns_for_use_case,
    get_application_domains
)


class ComplexityLevel(Enum):
    """System complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class SystemRequirements:
    """Structured representation of system requirements."""
    project_name: str
    description: str
    primary_goals: List[str]
    domain: str = "General"
    complexity: ComplexityLevel = ComplexityLevel.MODERATE

    # Functional requirements
    num_agents: int = 1
    agent_specializations: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    communication_needs: List[str] = field(default_factory=list)

    # Non-functional requirements
    scalability_needs: str = "moderate"
    performance_requirements: str = "standard"
    reliability_requirements: str = "standard"

    # Capabilities
    needs_reflection: bool = True
    needs_planning: bool = True
    needs_multi_agent: bool = False
    needs_tool_integration: bool = False

    # Additional context
    constraints: List[str] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """Result of requirements analysis."""
    requirements: SystemRequirements
    recommended_patterns: List[DesignPattern]
    recommended_components: List[ComponentType]
    recommended_agent_roles: List[AgentRole]
    complexity_assessment: str
    recommendations: List[str]
    warnings: List[str] = field(default_factory=list)


class RequirementsAnalyzer:
    """Analyzes user requirements and provides recommendations."""

    # Keywords for detecting needs
    REFLECTION_KEYWORDS = [
        'monitor', 'evaluate', 'self-assess', 'adapt', 'improve',
        'learn', 'optimize', 'quality', 'error detection', 'reflection'
    ]

    PLANNING_KEYWORDS = [
        'plan', 'schedule', 'organize', 'decompose', 'workflow',
        'task management', 'orchestrate', 'coordinate', 'strategy'
    ]

    MULTI_AGENT_KEYWORDS = [
        'multi-agent', 'multiple agents', 'collaboration', 'team',
        'distributed', 'cooperative', 'swarm', 'coordinated'
    ]

    TOOL_KEYWORDS = [
        'api', 'database', 'search', 'external', 'integration',
        'tool', 'service', 'web', 'data source'
    ]

    def analyze(self, requirements: SystemRequirements) -> AnalysisResult:
        """
        Analyze requirements and provide recommendations.

        Args:
            requirements: Structured system requirements

        Returns:
            Analysis result with recommendations
        """
        # Detect needed patterns and components
        self._detect_capabilities(requirements)

        # Assess complexity
        complexity_assessment = self._assess_complexity(requirements)

        # Recommend patterns
        recommended_patterns = self._recommend_patterns(requirements)

        # Recommend components
        recommended_components = self._recommend_components(requirements)

        # Recommend agent roles
        recommended_agent_roles = self._recommend_agent_roles(requirements)

        # Generate recommendations
        recommendations = self._generate_recommendations(requirements)

        # Generate warnings
        warnings = self._generate_warnings(requirements)

        return AnalysisResult(
            requirements=requirements,
            recommended_patterns=recommended_patterns,
            recommended_components=recommended_components,
            recommended_agent_roles=recommended_agent_roles,
            complexity_assessment=complexity_assessment,
            recommendations=recommendations,
            warnings=warnings
        )

    def _detect_capabilities(self, requirements: SystemRequirements) -> None:
        """Detect required capabilities from description and goals."""
        combined_text = (
            requirements.description + " " +
            " ".join(requirements.primary_goals) + " " +
            " ".join(requirements.agent_specializations)
        ).lower()

        # Check for reflection needs
        if any(kw in combined_text for kw in self.REFLECTION_KEYWORDS):
            requirements.needs_reflection = True

        # Check for planning needs
        if any(kw in combined_text for kw in self.PLANNING_KEYWORDS):
            requirements.needs_planning = True

        # Check for multi-agent needs
        if (any(kw in combined_text for kw in self.MULTI_AGENT_KEYWORDS) or
            requirements.num_agents > 1):
            requirements.needs_multi_agent = True

        # Check for tool integration needs
        if (any(kw in combined_text for kw in self.TOOL_KEYWORDS) or
            len(requirements.required_tools) > 0):
            requirements.needs_tool_integration = True

    def _assess_complexity(self, requirements: SystemRequirements) -> str:
        """Assess system complexity based on requirements."""
        complexity_score = 0

        # Factor: Number of agents
        if requirements.num_agents > 5:
            complexity_score += 3
        elif requirements.num_agents > 2:
            complexity_score += 2
        elif requirements.num_agents > 1:
            complexity_score += 1

        # Factor: Number of specializations
        complexity_score += min(len(requirements.agent_specializations), 3)

        # Factor: Required tools
        complexity_score += min(len(requirements.required_tools) // 2, 2)

        # Factor: Multi-agent coordination
        if requirements.needs_multi_agent:
            complexity_score += 2

        # Factor: Advanced capabilities
        if requirements.needs_reflection:
            complexity_score += 1
        if requirements.needs_planning:
            complexity_score += 1

        # Determine complexity level
        if complexity_score <= 2:
            requirements.complexity = ComplexityLevel.SIMPLE
            return "Simple: Single or few agents with basic capabilities"
        elif complexity_score <= 5:
            requirements.complexity = ComplexityLevel.MODERATE
            return "Moderate: Multiple agents with some coordination needs"
        elif complexity_score <= 8:
            requirements.complexity = ComplexityLevel.COMPLEX
            return "Complex: Multi-agent system with advanced capabilities"
        else:
            requirements.complexity = ComplexityLevel.VERY_COMPLEX
            return "Very Complex: Large-scale multi-agent system with sophisticated coordination"

    def _recommend_patterns(self, requirements: SystemRequirements) -> List[DesignPattern]:
        """Recommend design patterns based on requirements."""
        patterns = []

        if requirements.needs_reflection:
            patterns.append(DesignPattern.REFLECTION)

        if requirements.needs_planning:
            patterns.append(DesignPattern.PLANNING)

        if requirements.needs_tool_integration:
            patterns.append(DesignPattern.TOOL_USE)

        if requirements.needs_multi_agent:
            patterns.append(DesignPattern.MULTI_AGENT_COLLABORATION)

        # Ensure at least planning is included
        if not patterns:
            patterns.append(DesignPattern.PLANNING)

        return patterns

    def _recommend_components(self, requirements: SystemRequirements) -> List[ComponentType]:
        """Recommend architectural components based on requirements."""
        components = set()

        # Core execution is always needed
        components.add(ComponentType.EXECUTION)

        if requirements.needs_reflection:
            components.add(ComponentType.REFLECTION)

        if requirements.needs_planning:
            components.add(ComponentType.PLANNING)

        if requirements.needs_multi_agent:
            components.add(ComponentType.COMMUNICATION)

        if requirements.needs_tool_integration:
            components.add(ComponentType.TOOL_INTEGRATION)

        return list(components)

    def _recommend_agent_roles(self, requirements: SystemRequirements) -> List[AgentRole]:
        """Recommend agent roles based on requirements."""
        roles = []

        if requirements.needs_multi_agent:
            # For multi-agent systems, recommend hierarchical structure
            roles.append(AgentRole.MASTER_PLANNER)

            if len(requirements.agent_specializations) > 0:
                roles.append(AgentRole.SPECIALIST)

            if requirements.complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.VERY_COMPLEX]:
                roles.append(AgentRole.COMMUNICATION_FACILITATOR)
                roles.append(AgentRole.REFLECTIVE_OBSERVER)
        else:
            # For single-agent systems, recommend specialist role
            roles.append(AgentRole.SPECIALIST)

        return roles

    def _generate_recommendations(self, requirements: SystemRequirements) -> List[str]:
        """Generate implementation recommendations."""
        recommendations = []

        # Domain-specific recommendations
        domains = get_application_domains()
        if requirements.domain in domains:
            domain_info = domains[requirements.domain]
            recommendations.append(
                f"For {requirements.domain} applications, consider: " +
                "; ".join(domain_info["specific_considerations"])
            )

        # Complexity-based recommendations
        if requirements.complexity == ComplexityLevel.SIMPLE:
            recommendations.append(
                "Start with a single-agent architecture and expand as needed"
            )
        elif requirements.complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.VERY_COMPLEX]:
            recommendations.append(
                "Implement hierarchical agent structure to manage complexity"
            )
            recommendations.append(
                "Use Communication Facilitator agent to optimize message flow"
            )
            recommendations.append(
                "Deploy Reflective Observer for system-wide monitoring"
            )

        # Pattern-specific recommendations
        if requirements.needs_reflection:
            recommendations.append(
                "Implement event-driven reflection triggers to minimize overhead"
            )

        if requirements.needs_multi_agent:
            recommendations.append(
                "Design clear communication protocols before implementation"
            )
            recommendations.append(
                "Consider using message queues for scalable agent communication"
            )

        if requirements.needs_tool_integration:
            recommendations.append(
                "Use adapter pattern for external tool integration"
            )
            recommendations.append(
                "Implement circuit breakers for external service resilience"
            )

        return recommendations

    def _generate_warnings(self, requirements: SystemRequirements) -> List[str]:
        """Generate warnings about potential challenges."""
        warnings = []

        if requirements.num_agents > 10:
            warnings.append(
                "Large number of agents may cause coordination overhead. " +
                "Consider hierarchical organization."
            )

        if requirements.needs_multi_agent and not requirements.needs_planning:
            warnings.append(
                "Multi-agent systems typically require planning capabilities. " +
                "Consider enabling planning."
            )

        if len(requirements.required_tools) > 5:
            warnings.append(
                "Managing many external tools increases complexity. " +
                "Implement robust error handling."
            )

        if requirements.complexity == ComplexityLevel.VERY_COMPLEX:
            warnings.append(
                "Very complex systems require careful design and testing. " +
                "Consider phased implementation approach."
            )

        return warnings


def analyze_from_dict(requirements_dict: Dict) -> AnalysisResult:
    """
    Convenience function to analyze requirements from dictionary.

    Args:
        requirements_dict: Dictionary containing requirement fields

    Returns:
        Analysis result
    """
    requirements = SystemRequirements(**requirements_dict)
    analyzer = RequirementsAnalyzer()
    return analyzer.analyze(requirements)
