"""
Agentic AI Design Framework - Core components and knowledge base.
"""

from .components import (
    ComponentType,
    AgentRole,
    ArchitecturalComponent,
    AgentDefinition,
    CORE_COMPONENTS,
    AGENT_ROLES
)

from .patterns import (
    DesignPattern,
    Pattern,
    DESIGN_PATTERNS,
    get_pattern,
    get_all_patterns,
    get_patterns_for_use_case
)

from .knowledge_base import (
    AcademicInsight,
    ImplementationGuideline,
    get_academic_insights,
    get_implementation_guidelines,
    get_challenges,
    get_application_domains,
    recommend_domain_architecture
)

__all__ = [
    # Components
    'ComponentType',
    'AgentRole',
    'ArchitecturalComponent',
    'AgentDefinition',
    'CORE_COMPONENTS',
    'AGENT_ROLES',
    # Patterns
    'DesignPattern',
    'Pattern',
    'DESIGN_PATTERNS',
    'get_pattern',
    'get_all_patterns',
    'get_patterns_for_use_case',
    # Knowledge Base
    'AcademicInsight',
    'ImplementationGuideline',
    'get_academic_insights',
    'get_implementation_guidelines',
    'get_challenges',
    'get_application_domains',
    'recommend_domain_architecture'
]
