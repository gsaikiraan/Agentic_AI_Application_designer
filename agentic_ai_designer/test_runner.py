#!/usr/bin/env python3
"""
Test runner for the Agentic AI Application Designer.
Tests the application with example use cases.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.orchestrator import AgenticAIDesigner
from src.analyzer import SystemRequirements


def test_simple_assistant():
    """Test with simple assistant example."""
    print("\n" + "=" * 80)
    print("TEST 1: Simple Personal Assistant")
    print("=" * 80)

    with open("examples/simple_assistant.json") as f:
        data = json.load(f)

    requirements = SystemRequirements(**data)
    designer = AgenticAIDesigner()

    output = designer.design_system(requirements)

    print("\n✅ Analysis completed!")
    print(f"   Complexity: {output.requirements.complexity.value}")
    print(f"   Recommended Patterns: {[p.value for p in output.analysis.recommended_patterns]}")
    print(f"   Agents: {len(output.architecture.agents)}")

    # Generate and save report
    report = designer.generate_report(output)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "simple_assistant_design.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {report_path}")
    return True


def test_research_assistant():
    """Test with research assistant example."""
    print("\n" + "=" * 80)
    print("TEST 2: Autonomous Research Assistant")
    print("=" * 80)

    with open("examples/research_assistant.json") as f:
        data = json.load(f)

    requirements = SystemRequirements(**data)
    designer = AgenticAIDesigner()

    output = designer.design_system(requirements)

    print("\n✅ Analysis completed!")
    print(f"   Complexity: {output.requirements.complexity.value}")
    print(f"   Recommended Patterns: {[p.value for p in output.analysis.recommended_patterns]}")
    print(f"   Agents: {len(output.architecture.agents)}")
    print(f"   Implementation Phases: {len(output.implementation_plan.phases)}")

    # Show architecture diagram
    diagram = designer.export_architecture_diagram(output.architecture)
    print(diagram)

    # Generate and save report
    report = designer.generate_report(output)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "research_assistant_design.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"✅ Report saved to: {report_path}")
    return True


def test_code_review_system():
    """Test with code review system example."""
    print("\n" + "=" * 80)
    print("TEST 3: Intelligent Code Review System")
    print("=" * 80)

    with open("examples/code_review_system.json") as f:
        data = json.load(f)

    requirements = SystemRequirements(**data)
    designer = AgenticAIDesigner()

    output = designer.design_system(requirements)

    print("\n✅ Analysis completed!")
    print(f"   Complexity: {output.requirements.complexity.value}")
    print(f"   Recommended Patterns: {[p.value for p in output.analysis.recommended_patterns]}")
    print(f"   Agents: {len(output.architecture.agents)}")

    # Generate and save report
    report = designer.generate_report(output)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "code_review_system_design.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"✅ Report saved to: {report_path}")
    return True


def test_framework_info():
    """Test framework information retrieval."""
    print("\n" + "=" * 80)
    print("TEST 4: Framework Information")
    print("=" * 80)

    designer = AgenticAIDesigner()
    info = designer.get_framework_info()

    print(f"\n✅ Patterns: {len(info['patterns'])}")
    for pattern in info['patterns']:
        print(f"   - {pattern['name']}")

    print(f"\n✅ Academic Insights: {len(info['academic_insights'])}")
    for insight in info['academic_insights']:
        print(f"   - {insight['title']} ({insight['authors']})")

    print(f"\n✅ Application Domains: {len(info['application_domains'])}")
    for domain in info['application_domains']:
        print(f"   - {domain}")

    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🧪 AGENTIC AI APPLICATION DESIGNER - TEST SUITE")
    print("=" * 80)

    tests = [
        ("Simple Assistant", test_simple_assistant),
        ("Research Assistant", test_research_assistant),
        ("Code Review System", test_code_review_system),
        ("Framework Info", test_framework_info)
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
