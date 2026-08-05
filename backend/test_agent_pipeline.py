#!/usr/bin/env python3
"""
Simple test script to verify the agent pipeline works without running the full server.
Run this to test core functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.graph import run_agent_pipeline_simple
from app.core.config import settings


async def test_simple_question():
    """Test with a simple question that doesn't need data."""
    print("\n" + "="*60)
    print("🧪 Testing Agent Pipeline - Simple Question")
    print("="*60)

    question = "What is 2 + 2?"
    session_id = "test_session_001"

    print(f"\n📝 Question: {question}")
    print(f"🔄 Session: {session_id}")
    print(f"🤖 LLM Model: {settings.anthropic_model}")

    try:
        print("\n⏳ Running agent pipeline...")
        state = await run_agent_pipeline_simple(
            question=question,
            session_id=session_id,
            user_id=None
        )

        print(f"\n✅ Pipeline completed in {state.total_time_ms:.2f}ms")
        print(f"\n📊 Results:")
        print(f"   Intent: {state.intent}")
        print(f"   SQL Query: {state.sql_query}")
        print(f"   Errors: {len(state.errors)}")
        if state.errors:
            print(f"   Error Details: {state.errors}")

        print(f"\n📈 KPIs Found: {len(state.kpis)}")
        print(f"📈 Trends Found: {len(state.trends)}")
        print(f"⚠️  Anomalies Found: {len(state.anomalies)}")
        print(f"🎯 Recommendations: {len(state.recommendations)}")

        if state.executive_summary:
            print(f"\n📋 Executive Summary Generated: ✅")
            if isinstance(state.executive_summary, dict):
                print(f"   Key Findings: {len(state.executive_summary.get('key_findings', []))}")
                if state.executive_summary.get('narrative'):
                    print(f"   Narrative Preview: {state.executive_summary['narrative'][:100]}...")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_diagnostic_question():
    """Test with a diagnostic business question."""
    print("\n" + "="*60)
    print("🧪 Testing Agent Pipeline - Diagnostic Question")
    print("="*60)

    question = "Why did revenue decline?"
    session_id = "test_session_002"

    print(f"\n📝 Question: {question}")
    print(f"🔄 Session: {session_id}")

    try:
        print("\n⏳ Running agent pipeline...")
        state = await run_agent_pipeline_simple(
            question=question,
            session_id=session_id,
            user_id=None
        )

        print(f"\n✅ Pipeline completed in {state.total_time_ms:.2f}ms")
        print(f"\n📊 Results:")
        print(f"   Intent: {state.intent}")
        print(f"   KPIs: {len(state.kpis)}")
        print(f"   Trends: {len(state.trends)}")
        print(f"   Root Causes: {state.root_causes}")
        print(f"   Recommendations: {len(state.recommendations)}")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("\n" + "="*70)
    print(" "*10 + "🚀 DecisionLens AI - Agent Pipeline Test Suite")
    print("="*70)

    print("\n📋 Test Configuration:")
    print(f"   Environment: {settings.environment}")
    print(f"   Debug Mode: {settings.debug}")
    print(f"   LLM Provider: OpenRouter")
    print(f"   LLM Model: {settings.anthropic_model}")
    print(f"   DuckDB Path: {settings.duckdb_path}")

    # Test 1: Simple question
    print("\n" + "-"*70)
    test1_passed = await test_simple_question()

    # Test 2: Diagnostic question
    print("\n" + "-"*70)
    test2_passed = await test_diagnostic_question()

    # Summary
    print("\n" + "="*70)
    print("📊 Test Summary:")
    print(f"   Test 1 (Simple Question): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Test 2 (Diagnostic): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"   Overall: {'✅ ALL TESTS PASSED' if (test1_passed and test2_passed) else '❌ SOME TESTS FAILED'}")
    print("="*70 + "\n")

    return test1_passed and test2_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
