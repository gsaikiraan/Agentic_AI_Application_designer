"""
Main orchestrator for the Agentic AI Application Designer.
Coordinates the analysis, design, and planning process.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from pathlib import Path
from .analyzer import RequirementsAnalyzer, SystemRequirements, AnalysisResult
from .designer import ArchitectureDesigner, SystemArchitecture, format_architecture
from .planner import ImplementationPlanner, ImplementationPlan, format_implementation_plan
from .framework import get_all_patterns, get_academic_insights, get_application_domains
from .codegen import LangGraphCodeGenerator, format_langgraph_code


@dataclass
class DesignOutput:
    """Complete output from the design process."""
    requirements: SystemRequirements
    analysis: AnalysisResult
    architecture: SystemArchitecture
    implementation_plan: ImplementationPlan
    langgraph_code: Optional[Dict[str, str]] = None


class AgenticAIDesigner:
    """
    Main orchestrator that thinks like an AI engineer to design
    agentic AI applications based on the design framework.
    """

    def __init__(self):
        self.analyzer = RequirementsAnalyzer()
        self.designer = ArchitectureDesigner()
        self.planner = ImplementationPlanner()
        self.code_generator = LangGraphCodeGenerator()

    def design_system(self, requirements: SystemRequirements) -> DesignOutput:
        """
        Complete design process from requirements to implementation plan.

        Args:
            requirements: System requirements

        Returns:
            Complete design output
        """
        # Step 1: Analyze requirements
        print("🔍 Analyzing requirements...")
        analysis = self.analyzer.analyze(requirements)

        # Step 2: Design architecture
        print("🏗️  Designing system architecture...")
        architecture = self.designer.design(analysis)

        # Step 3: Create implementation plan
        print("📋 Creating implementation plan...")
        implementation_plan = self.planner.create_plan(architecture)

        # Step 4: Generate LangGraph code
        print("💻 Generating LangGraph implementation code...")
        langgraph_code = self.code_generator.generate_implementation(architecture)

        print("✅ Design process completed!\n")

        return DesignOutput(
            requirements=requirements,
            analysis=analysis,
            architecture=architecture,
            implementation_plan=implementation_plan,
            langgraph_code=langgraph_code
        )

    def generate_report(self, output: DesignOutput) -> str:
        """
        Generate comprehensive design report.

        Args:
            output: Design output

        Returns:
            Formatted report
        """
        report = []

        # Header
        report.append("=" * 80)
        report.append(f"AGENTIC AI APPLICATION DESIGN REPORT")
        report.append(f"Project: {output.requirements.project_name}")
        report.append("=" * 80)
        report.append("")

        # Executive Summary
        report.append("## EXECUTIVE SUMMARY\n")
        report.append(f"**Project:** {output.requirements.project_name}")
        report.append(f"**Domain:** {output.requirements.domain}")
        report.append(f"**Complexity:** {output.analysis.complexity_assessment}")
        report.append(f"**Number of Agents:** {len(output.architecture.agents)}")
        report.append(f"**Design Patterns:** {', '.join([p.value for p in output.architecture.patterns])}")
        report.append("")

        # Requirements
        report.append("\n" + "=" * 80)
        report.append("## 1. REQUIREMENTS ANALYSIS")
        report.append("=" * 80)
        report.append("")
        report.append(f"**Description:** {output.requirements.description}\n")
        report.append("**Primary Goals:**")
        for goal in output.requirements.primary_goals:
            report.append(f"- {goal}")
        report.append("")

        # Capabilities Analysis
        report.append("**Detected Capabilities:**")
        capabilities = []
        if output.requirements.needs_reflection:
            capabilities.append("✓ Reflection")
        if output.requirements.needs_planning:
            capabilities.append("✓ Planning")
        if output.requirements.needs_multi_agent:
            capabilities.append("✓ Multi-Agent Collaboration")
        if output.requirements.needs_tool_integration:
            capabilities.append("✓ Tool Integration")
        report.append(", ".join(capabilities))
        report.append("")

        # Recommendations
        if output.analysis.recommendations:
            report.append("**Recommendations:**")
            for rec in output.analysis.recommendations:
                report.append(f"- {rec}")
            report.append("")

        # Warnings
        if output.analysis.warnings:
            report.append("**Warnings:**")
            for warning in output.analysis.warnings:
                report.append(f"⚠️  {warning}")
            report.append("")

        # Architecture
        report.append("\n" + "=" * 80)
        report.append("## 2. SYSTEM ARCHITECTURE")
        report.append("=" * 80)
        report.append("")
        report.append(format_architecture(output.architecture))

        # Implementation Plan
        report.append("\n" + "=" * 80)
        report.append("## 3. IMPLEMENTATION PLAN")
        report.append("=" * 80)
        report.append("")
        report.append(format_implementation_plan(output.implementation_plan))

        # Framework References
        report.append("\n" + "=" * 80)
        report.append("## 4. ACADEMIC FOUNDATIONS")
        report.append("=" * 80)
        report.append("")
        report.append("This design is based on the following academic research:\n")

        insights = get_academic_insights()
        for insight in insights:
            report.append(f"**{insight.title}**")
            report.append(f"*{insight.authors}*")
            report.append(f"{insight.key_contribution}")
            report.append(f"Application: {insight.application_to_framework}")
            report.append(f"Reference: {insight.reference}")
            report.append("")

        # LangGraph Implementation Code
        if output.langgraph_code:
            report.append("\n" + "=" * 80)
            report.append("## 5. LANGGRAPH IMPLEMENTATION CODE")
            report.append("=" * 80)
            report.append("")
            report.append("The following code provides a working LangGraph implementation")
            report.append("of the designed multi-agent system. This code is production-ready")
            report.append("and follows LangChain/LangGraph best practices.")
            report.append("")

            formatted_code = format_langgraph_code(output.langgraph_code)
            report.append(formatted_code)

        # Conclusion
        report.append("\n" + "=" * 80)
        report.append("## 6. CONCLUSION")
        report.append("=" * 80)
        report.append("")
        report.append(
            f"This comprehensive design provides a blueprint for building {output.requirements.project_name}, "
            f"a {output.requirements.complexity.value} agentic AI application. "
            f"The architecture leverages {len(output.architecture.patterns)} design patterns and "
            f"incorporates {len(output.architecture.agents)} specialized agents to achieve the specified goals."
        )
        report.append("")
        report.append(
            "The implementation plan provides a phased approach with detailed tasks, code examples, "
            "and testing considerations. Following this plan will result in a scalable, maintainable, "
            "and robust agentic AI system aligned with state-of-the-art academic research and "
            "industry best practices."
        )
        report.append("")

        return "\n".join(report)

    def get_framework_info(self) -> Dict:
        """Get information about the design framework."""
        return {
            "patterns": [
                {
                    "name": p.name,
                    "type": p.pattern_type.value,
                    "description": p.description
                }
                for p in get_all_patterns()
            ],
            "academic_insights": [
                {
                    "title": i.title,
                    "authors": i.authors,
                    "contribution": i.key_contribution
                }
                for i in get_academic_insights()
            ],
            "application_domains": list(get_application_domains().keys())
        }

    def export_architecture_diagram(self, architecture: SystemArchitecture) -> str:
        """
        Generate a textual architecture diagram.

        Args:
            architecture: System architecture

        Returns:
            ASCII diagram
        """
        diagram = []

        diagram.append(f"\n{'=' * 60}")
        diagram.append(f"  {architecture.project_name} - Architecture Diagram")
        diagram.append(f"{'=' * 60}\n")

        # Draw agent hierarchy
        master_agents = [a for a in architecture.agents if a.role.value == "master_planner"]
        specialist_agents = [a for a in architecture.agents if a.role.value == "specialist"]
        support_agents = [a for a in architecture.agents if a.role.value in ["communication_facilitator", "reflective_observer"]]

        if master_agents:
            diagram.append("     ┌─────────────────────────┐")
            diagram.append(f"     │  {master_agents[0].name.center(21)}  │")
            diagram.append("     └─────────────────────────┘")
            diagram.append("               │")
            diagram.append("     ┌─────────┴─────────┐")

        if specialist_agents:
            diagram.append("     │                   │")
            # Draw specialists
            for i, agent in enumerate(specialist_agents):
                if i == 0:
                    diagram.append(f"     ▼                   ▼")
                    diagram.append(f" ┌───────────┐       ┌───────────┐")
                    if len(specialist_agents) > 1:
                        diagram.append(f" │ {specialist_agents[0].name[:9].center(9)} │       │ {specialist_agents[1].name[:9].center(9)} │")
                    else:
                        diagram.append(f" │ {agent.name[:9].center(9)} │")
                    diagram.append(f" └───────────┘       └───────────┘")
                    break

            if len(specialist_agents) > 2:
                diagram.append(f"          ... ({len(specialist_agents) - 2} more)")

        if support_agents:
            diagram.append("\n     Support Agents:")
            for agent in support_agents:
                diagram.append(f"     • {agent.name}")

        diagram.append(f"\n{'=' * 60}\n")

        return "\n".join(diagram)

    def save_langgraph_code(self, output: DesignOutput, output_dir: str = "generated_code") -> None:
        """
        Save generated LangGraph code to files.

        Args:
            output: Design output with LangGraph code
            output_dir: Directory to save code files
        """
        if not output.langgraph_code:
            print("⚠️  No LangGraph code to save")
            return

        # Create output directory
        code_dir = Path(output_dir) / output.requirements.project_name.lower().replace(" ", "_")
        code_dir.mkdir(parents=True, exist_ok=True)

        # Save each file
        for filename, code in output.langgraph_code.items():
            filepath = code_dir / filename
            with open(filepath, 'w') as f:
                f.write(code)
            print(f"✅ Created: {filepath}")

        # Create __init__.py
        init_file = code_dir / "__init__.py"
        with open(init_file, 'w') as f:
            f.write(f'"""\n{output.requirements.project_name}\n"""')

        print(f"\n✅ LangGraph code saved to: {code_dir}")
        print("\nTo run the generated code:")
        print(f"  cd {code_dir}")
        print("  export OPENAI_API_KEY=your_key_here")
        print("  export TAVILY_API_KEY=your_key_here  # Optional for web search")
        print("  python main.py")
