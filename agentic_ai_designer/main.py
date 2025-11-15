#!/usr/bin/env python3
"""
Agentic AI Application Designer - Interactive CLI
Think like an AI engineer to design agentic AI applications.
"""

import sys
import json
from pathlib import Path
from typing import Optional

from src.orchestrator import AgenticAIDesigner
from src.analyzer import SystemRequirements, ComplexityLevel
from src.framework import get_application_domains


class InteractiveCLI:
    """Interactive command-line interface for the Agentic AI Designer."""

    def __init__(self):
        self.designer = AgenticAIDesigner()

    def print_header(self):
        """Print application header."""
        print("\n" + "=" * 80)
        print(" " * 15 + "🤖 AGENTIC AI APPLICATION DESIGNER 🤖")
        print(" " * 10 + "Think Like an AI Engineer")
        print("=" * 80)
        print("\nDesign sophisticated agentic AI applications based on cutting-edge")
        print("research and industry best practices.\n")

    def print_menu(self):
        """Print main menu."""
        print("\n" + "-" * 80)
        print("MAIN MENU")
        print("-" * 80)
        print("1. 🎯 Create New Design (Interactive)")
        print("2. 📁 Load Requirements from JSON")
        print("3. 📚 View Framework Information")
        print("4. 💡 View Example Use Cases")
        print("5. 🚪 Exit")
        print("-" * 80)

    def get_input(self, prompt: str, default: Optional[str] = None) -> str:
        """Get user input with optional default."""
        if default:
            full_prompt = f"{prompt} [{default}]: "
        else:
            full_prompt = f"{prompt}: "

        value = input(full_prompt).strip()
        return value if value else (default or "")

    def get_int_input(self, prompt: str, default: int = 1) -> int:
        """Get integer input with validation."""
        while True:
            try:
                value = self.get_input(prompt, str(default))
                return int(value)
            except ValueError:
                print("❌ Please enter a valid number.")

    def get_list_input(self, prompt: str) -> list:
        """Get list input (comma-separated)."""
        value = self.get_input(f"{prompt} (comma-separated)")
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]

    def interactive_requirements_gathering(self) -> SystemRequirements:
        """Gather requirements through interactive prompts."""
        print("\n" + "=" * 80)
        print("📝 REQUIREMENTS GATHERING")
        print("=" * 80)
        print("\nLet's gather information about your agentic AI application.\n")

        # Basic information
        project_name = self.get_input("Project Name", "My Agentic AI System")
        description = self.get_input(
            "Brief Description",
            "An intelligent multi-agent system"
        )

        # Primary goals
        print("\n💭 What are the primary goals of this system?")
        primary_goals = []
        while True:
            goal = self.get_input(f"  Goal #{len(primary_goals) + 1} (press Enter to finish)")
            if not goal:
                break
            primary_goals.append(goal)

        if not primary_goals:
            primary_goals = ["Automate complex tasks", "Improve decision-making"]

        # Domain selection
        print("\n🏢 Application Domain:")
        domains = list(get_application_domains().keys()) + ["General", "Other"]
        for i, domain in enumerate(domains, 1):
            print(f"  {i}. {domain}")

        domain_idx = self.get_int_input("Select domain number", 6) - 1
        domain = domains[domain_idx] if 0 <= domain_idx < len(domains) else "General"

        # Agent configuration
        print("\n👥 Agent Configuration:")
        num_agents = self.get_int_input("Number of agents", 3)

        specializations = []
        if num_agents > 1:
            print("\nWhat specializations do your agents need?")
            print("Examples: Research, Data Analysis, Code Generation, Planning, etc.")
            specializations = self.get_list_input("Agent specializations")

        # Tool requirements
        print("\n🛠️  External Tools and Integrations:")
        print("Examples: Web Search, Database, API, File System, Calculator, etc.")
        required_tools = self.get_list_input("Required tools")

        # Non-functional requirements
        print("\n⚙️  Non-Functional Requirements:")
        print("Scalability needs:")
        print("  1. Low")
        print("  2. Moderate")
        print("  3. High")
        scalability_idx = self.get_int_input("Select option", 2)
        scalability_map = {1: "low", 2: "moderate", 3: "high"}
        scalability = scalability_map.get(scalability_idx, "moderate")

        print("\nPerformance requirements:")
        print("  1. Standard")
        print("  2. High")
        print("  3. Real-time")
        performance_idx = self.get_int_input("Select option", 1)
        performance_map = {1: "standard", 2: "high", 3: "real-time"}
        performance = performance_map.get(performance_idx, "standard")

        # Constraints
        print("\n⚠️  Any constraints or preferences?")
        constraints = self.get_list_input("Constraints (optional)")

        # Create requirements object
        requirements = SystemRequirements(
            project_name=project_name,
            description=description,
            primary_goals=primary_goals,
            domain=domain,
            num_agents=num_agents,
            agent_specializations=specializations,
            required_tools=required_tools,
            scalability_needs=scalability,
            performance_requirements=performance,
            constraints=constraints
        )

        return requirements

    def load_requirements_from_json(self) -> Optional[SystemRequirements]:
        """Load requirements from JSON file."""
        file_path = self.get_input("\n📁 Enter JSON file path")

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                requirements = SystemRequirements(**data)
                print(f"✅ Successfully loaded requirements from {file_path}")
                return requirements
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON format")
        except Exception as e:
            print(f"❌ Error loading file: {e}")

        return None

    def view_framework_info(self):
        """Display framework information."""
        print("\n" + "=" * 80)
        print("📚 FRAMEWORK INFORMATION")
        print("=" * 80)

        info = self.designer.get_framework_info()

        print("\n## Core Design Patterns\n")
        for pattern in info["patterns"]:
            print(f"**{pattern['name']}**")
            print(f"  {pattern['description']}\n")

        print("\n## Academic Foundations\n")
        for insight in info["academic_insights"]:
            print(f"**{insight['title']}**")
            print(f"  Authors: {insight['authors']}")
            print(f"  Contribution: {insight['contribution']}\n")

        print("\n## Application Domains\n")
        for domain in info["application_domains"]:
            print(f"  • {domain}")

        input("\nPress Enter to continue...")

    def view_example_use_cases(self):
        """Display example use cases."""
        print("\n" + "=" * 80)
        print("💡 EXAMPLE USE CASES")
        print("=" * 80)

        examples = [
            {
                "name": "Autonomous Research Assistant",
                "description": "Multi-agent system for conducting literature reviews and synthesizing research",
                "agents": 4,
                "patterns": ["Reflection", "Planning", "Tool Use", "Multi-Agent Collaboration"],
                "tools": ["Web Search", "Paper Database", "Citation Manager"]
            },
            {
                "name": "Intelligent Code Review System",
                "description": "Automated code analysis and review with multiple specialized agents",
                "agents": 5,
                "patterns": ["Reflection", "Planning", "Multi-Agent Collaboration"],
                "tools": ["Git", "Static Analyzer", "Test Runner"]
            },
            {
                "name": "Customer Support Automation",
                "description": "Multi-agent system for handling customer inquiries and support tickets",
                "agents": 3,
                "patterns": ["Planning", "Tool Use", "Reflection"],
                "tools": ["CRM API", "Knowledge Base", "Email Service"]
            },
            {
                "name": "Data Analysis Pipeline",
                "description": "Automated data collection, analysis, and reporting system",
                "agents": 4,
                "patterns": ["Planning", "Tool Use", "Multi-Agent Collaboration"],
                "tools": ["Database", "Analytics Engine", "Visualization API"]
            }
        ]

        for i, example in enumerate(examples, 1):
            print(f"\n{i}. **{example['name']}**")
            print(f"   {example['description']}")
            print(f"   Agents: {example['agents']}")
            print(f"   Patterns: {', '.join(example['patterns'])}")
            print(f"   Tools: {', '.join(example['tools'])}")

        input("\nPress Enter to continue...")

    def save_report(self, report: str, project_name: str):
        """Save design report to file."""
        # Create output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # Create filename from project name
        filename = project_name.lower().replace(" ", "_") + "_design.md"
        filepath = output_dir / filename

        # Save report
        with open(filepath, 'w') as f:
            f.write(report)

        print(f"\n✅ Design report saved to: {filepath}")

    def run_design_process(self, requirements: SystemRequirements):
        """Run the complete design process."""
        print("\n" + "=" * 80)
        print("🚀 STARTING DESIGN PROCESS")
        print("=" * 80)

        # Run design
        output = self.designer.design_system(requirements)

        # Generate report
        print("\n📄 Generating comprehensive design report...")
        report = self.designer.generate_report(output)

        # Display summary
        print("\n" + "=" * 80)
        print("✨ DESIGN COMPLETE!")
        print("=" * 80)

        print("\n📊 Design Summary:")
        print(f"  • Project: {output.requirements.project_name}")
        print(f"  • Complexity: {output.requirements.complexity.value}")
        print(f"  • Agents: {len(output.architecture.agents)}")
        print(f"  • Patterns: {len(output.architecture.patterns)}")
        print(f"  • Implementation Phases: {len(output.implementation_plan.phases)}")

        # Show architecture diagram
        diagram = self.designer.export_architecture_diagram(output.architecture)
        print(diagram)

        # Ask to view full report
        view_report = self.get_input("\n📖 View full report? (y/n)", "y").lower()
        if view_report == 'y':
            print("\n" + report)

        # Ask to save report
        save_report = self.get_input("\n💾 Save report to file? (y/n)", "y").lower()
        if save_report == 'y':
            self.save_report(report, output.requirements.project_name)

        # Ask to save LangGraph code
        save_code = self.get_input("\n💻 Save LangGraph implementation code? (y/n)", "y").lower()
        if save_code == 'y':
            self.designer.save_langgraph_code(output)

    def run(self):
        """Run the interactive CLI application."""
        self.print_header()

        while True:
            self.print_menu()

            choice = self.get_input("\nSelect option", "1")

            if choice == "1":
                requirements = self.interactive_requirements_gathering()
                self.run_design_process(requirements)

            elif choice == "2":
                requirements = self.load_requirements_from_json()
                if requirements:
                    self.run_design_process(requirements)

            elif choice == "3":
                self.view_framework_info()

            elif choice == "4":
                self.view_example_use_cases()

            elif choice == "5":
                print("\n👋 Thank you for using Agentic AI Application Designer!")
                print("Happy building! 🚀\n")
                sys.exit(0)

            else:
                print("❌ Invalid option. Please try again.")


def main():
    """Main entry point."""
    try:
        cli = InteractiveCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
