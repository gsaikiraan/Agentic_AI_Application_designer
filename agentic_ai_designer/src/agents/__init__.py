"""
LLM-powered reasoning agent for intelligent architecture analysis.
Makes the designer truly agentic by using LLMs to reason about design decisions.
"""

import os
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..analyzer import SystemRequirements
from ..framework import ComponentType, AgentRole, DesignPattern


class LLMReasoningAgent:
    """
    Agentic reasoning agent that uses LLMs to analyze requirements
    and make intelligent architecture decisions.
    """

    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the reasoning agent.

        Args:
            model: LLM model to use
            temperature: Temperature for generation (higher = more creative)
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY", "")
        )

    def analyze_requirements(self, requirements: SystemRequirements) -> Dict:
        """
        Use LLM to deeply analyze requirements and suggest architecture.

        Args:
            requirements: System requirements

        Returns:
            Analysis with LLM reasoning
        """
        system_prompt = """You are an expert AI architect specializing in multi-agent systems.
Your role is to analyze system requirements and provide intelligent recommendations for:
- Agent roles and responsibilities
- Architectural components needed
- Design patterns to apply
- Potential challenges and mitigations

Think step-by-step and provide reasoned recommendations based on the requirements."""

        user_prompt = f"""Analyze these requirements for an agentic AI application:

**Project:** {requirements.project_name}
**Description:** {requirements.description}
**Domain:** {requirements.domain}

**Goals:**
{chr(10).join(f"- {goal}" for goal in requirements.primary_goals)}

**Agent Configuration:**
- Number of agents: {requirements.num_agents}
- Specializations: {', '.join(requirements.agent_specializations) if requirements.agent_specializations else 'None specified'}
- Required tools: {', '.join(requirements.required_tools) if requirements.required_tools else 'None specified'}

**Requirements:**
- Scalability: {requirements.scalability_needs}
- Performance: {requirements.performance_requirements}
- Reliability: {requirements.reliability_requirements}

Please analyze and recommend:
1. What agent roles are needed and why?
2. Which architectural components (Reflection, Planning, Communication, Execution, Tools) are essential?
3. What design patterns should be applied?
4. What are the main architectural considerations?
5. Any potential challenges or risks?

Provide clear, actionable recommendations."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)

        return {
            "llm_analysis": response.content,
            "reasoning_used": True
        }

    def suggest_agent_roles(
        self,
        requirements: SystemRequirements,
        analysis: str
    ) -> List[Dict]:
        """
        Use LLM to suggest specific agent roles with reasoning.

        Args:
            requirements: System requirements
            analysis: Previous LLM analysis

        Returns:
            List of suggested agent roles with justifications
        """
        prompt = f"""Based on this analysis:

{analysis}

And these requirements:
- Project: {requirements.project_name}
- Goals: {', '.join(requirements.primary_goals)}
- Specializations needed: {', '.join(requirements.agent_specializations) if requirements.agent_specializations else 'General purpose'}

Suggest specific agent roles. For each agent, provide:
1. Role name (e.g., "Master Planner", "Research Specialist")
2. Key responsibilities
3. Why this role is needed
4. What components it should have

Format as a structured list."""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return {
            "suggestions": response.content,
            "reasoning": "LLM-generated based on requirements analysis"
        }

    def evaluate_complexity(
        self,
        requirements: SystemRequirements
    ) -> Dict:
        """
        Use LLM to evaluate system complexity with detailed reasoning.

        Args:
            requirements: System requirements

        Returns:
            Complexity evaluation with reasoning
        """
        prompt = f"""Evaluate the complexity of this agentic AI system:

**Project:** {requirements.project_name}
**Description:** {requirements.description}
**Number of agents:** {requirements.num_agents}
**Specializations:** {len(requirements.agent_specializations)}
**Tools required:** {len(requirements.required_tools)}
**Goals:** {len(requirements.primary_goals)}

Consider:
- Coordination complexity
- State management needs
- Tool integration complexity
- Scalability requirements
- Domain-specific challenges

Rate complexity as: Simple, Moderate, Complex, or Very Complex
Provide detailed reasoning for your rating."""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return {
            "complexity_reasoning": response.content,
            "llm_evaluated": True
        }

    def recommend_patterns(
        self,
        requirements: SystemRequirements,
        analysis: str
    ) -> List[str]:
        """
        Use LLM to recommend design patterns with reasoning.

        Args:
            requirements: System requirements
            analysis: Previous analysis

        Returns:
            Pattern recommendations with reasoning
        """
        available_patterns = """
Available patterns:
1. Reflection Pattern - Self-evaluation and adaptation
2. Tool Use Pattern - External API and service integration
3. Planning Pattern - Task decomposition and orchestration
4. Multi-Agent Collaboration Pattern - Agent coordination and communication
"""

        prompt = f"""{available_patterns}

Based on these requirements:
{analysis}

Project goals:
{chr(10).join(f"- {goal}" for goal in requirements.primary_goals)}

Which patterns should be applied and why?
Provide specific reasoning for each pattern recommendation."""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return {
            "pattern_recommendations": response.content,
            "reasoning_provided": True
        }


class ArchitectureCriticAgent:
    """
    Agentic critic that evaluates and reflects on generated architectures.
    Provides self-reflection capabilities to the designer.
    """

    def __init__(self, model: str = "gpt-4", temperature: float = 0.3):
        """
        Initialize the critic agent.

        Args:
            model: LLM model to use
            temperature: Lower temperature for more focused critique
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY", "")
        )

    def critique_architecture(
        self,
        requirements: SystemRequirements,
        architecture_summary: str
    ) -> Dict:
        """
        Critique a generated architecture and suggest improvements.

        Args:
            requirements: Original requirements
            architecture_summary: Summary of generated architecture

        Returns:
            Critique with scores and recommendations
        """
        system_prompt = """You are an expert architecture reviewer specializing in multi-agent systems.
Your role is to critique architectures and identify:
- Potential issues or bottlenecks
- Missing components or capabilities
- Over-engineering or unnecessary complexity
- Scalability concerns
- Security or reliability risks

Provide constructive, actionable feedback."""

        user_prompt = f"""Review this architecture design:

**Original Requirements:**
- Project: {requirements.project_name}
- Goals: {', '.join(requirements.primary_goals)}
- Domain: {requirements.domain}
- Complexity target: Appropriate for {requirements.num_agents} agents

**Proposed Architecture:**
{architecture_summary}

Please critique this design:
1. Rate the architecture (1-10) on:
   - Alignment with requirements
   - Scalability
   - Maintainability
   - Complexity appropriateness

2. Identify potential issues or risks

3. Suggest specific improvements

4. Highlight what was done well

Be specific and constructive."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)

        return {
            "critique": response.content,
            "critic_agent_used": True
        }

    def suggest_alternatives(
        self,
        requirements: SystemRequirements,
        current_architecture: str,
        critique: str
    ) -> Dict:
        """
        Suggest alternative architectures based on critique.

        Args:
            requirements: Original requirements
            current_architecture: Current architecture summary
            critique: Critique of current architecture

        Returns:
            Alternative architecture suggestions
        """
        prompt = f"""Given this architecture and critique:

**Current Architecture:**
{current_architecture}

**Critique:**
{critique}

**Requirements:**
- Project: {requirements.project_name}
- Goals: {', '.join(requirements.primary_goals[:3])}

Suggest 2-3 alternative architectural approaches that address the critique.
For each alternative, explain:
- Key differences from current approach
- Advantages
- Trade-offs

Be specific and practical."""

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return {
            "alternatives": response.content,
            "alternative_count": "2-3 suggested"
        }

    def score_architecture(
        self,
        architecture_description: str,
        requirements: SystemRequirements
    ) -> Dict:
        """
        Score architecture on multiple dimensions.

        Args:
            architecture_description: Description of architecture
            requirements: Original requirements

        Returns:
            Scores and justifications
        """
        prompt = f"""Score this architecture on a scale of 1-10 for each criterion:

**Architecture:**
{architecture_description}

**Requirements:**
- Scalability needs: {requirements.scalability_needs}
- Performance: {requirements.performance_requirements}
- Reliability: {requirements.reliability_requirements}

**Criteria:**
1. Requirements Alignment - How well does it meet stated requirements?
2. Scalability - Can it scale as needed?
3. Maintainability - Is it easy to maintain and modify?
4. Complexity - Is the complexity appropriate (not over/under-engineered)?
5. Reliability - Is it robust and fault-tolerant?

Provide score and 1-sentence justification for each criterion.
Format: "Criterion: X/10 - Justification" """

        response = self.llm.invoke([HumanMessage(content=prompt)])

        return {
            "scores": response.content,
            "scoring_complete": True
        }


def format_llm_analysis(analysis: Dict) -> str:
    """Format LLM analysis for display."""
    output = []

    output.append("# LLM-Powered Analysis")
    output.append("")

    if "llm_analysis" in analysis:
        output.append("## Deep Analysis")
        output.append(analysis["llm_analysis"])
        output.append("")

    if "complexity_reasoning" in analysis:
        output.append("## Complexity Evaluation")
        output.append(analysis["complexity_reasoning"])
        output.append("")

    if "pattern_recommendations" in analysis:
        output.append("## Pattern Recommendations")
        output.append(analysis["pattern_recommendations"])
        output.append("")

    return "\n".join(output)


def format_critique(critique: Dict) -> str:
    """Format architecture critique for display."""
    output = []

    output.append("# Architecture Critique")
    output.append("")

    if "critique" in critique:
        output.append("## Review")
        output.append(critique["critique"])
        output.append("")

    if "scores" in critique:
        output.append("## Scores")
        output.append(critique["scores"])
        output.append("")

    if "alternatives" in critique:
        output.append("## Alternative Approaches")
        output.append(critique["alternatives"])
        output.append("")

    return "\n".join(output)
