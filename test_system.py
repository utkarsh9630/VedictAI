#!/usr/bin/env python3
"""
Test script for DebateShield Lite
Verifies all components are working
"""
import asyncio
import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("🧪 Testing imports...")
    try:
        import fastapi
        import uvicorn
        import httpx
        import openai
        import aiosqlite
        from fuzzywuzzy import fuzz
        from dotenv import load_dotenv
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    try:
        from config import config
        print(f"   Database path: {config.DATABASE_PATH}")
        print(f"   App environment: {config.APP_ENV}")
        print(f"   LLM configured: {'✅' if config.LLM_API_KEY else '❌ (will use mock)'}")
        print(f"   You.com configured: {'✅' if config.YOU_API_KEY else '❌ (will use mock)'}")
        print(f"   Intercom configured: {'✅' if config.INTERCOM_TOKEN else '❌ (optional)'}")
        print(f"   Plivo configured: {'✅' if config.PLIVO_AUTH_ID else '❌ (optional)'}")
        print("✅ Configuration loaded")
        return True
    except Exception as e:
        print(f"❌ Config failed: {e}")
        return False

async def test_memory():
    """Test memory system"""
    print("\n🧪 Testing memory system...")
    try:
        from memory import Memory
        memory = Memory(":memory:")  # Use in-memory database
        await memory.init_db()
        
        # Test storing
        await memory.store_claim(
            "Test claim",
            {
                "verdict": "false",
                "confidence": 80,
                "risk_level": "low",
                "topic": "test",
                "evidence_for": [],
                "evidence_against": [],
                "actions": {}
            }
        )
        
        # Test retrieval
        similar = await memory.find_similar_claim("Test claim")
        assert similar is not None
        assert similar["verdict"] == "false"
        
        print("✅ Memory system working")
        return True
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        return False

async def test_you_search():
    """Test You.com integration"""
    print("\n🧪 Testing You.com integration...")
    try:
        from you_search import YouSearcher
        searcher = YouSearcher()
        
        results = await searcher.search("test query", num_results=2)
        assert len(results) > 0
        
        evidence = await searcher.retrieve_evidence("test claim")
        assert "support" in evidence
        assert "refute" in evidence
        
        print("✅ You.com integration working (mock mode OK)")
        return True
    except Exception as e:
        print(f"❌ You.com test failed: {e}")
        return False

async def test_agents():
    """Test CoD agents (basic structure)"""
    print("\n🧪 Testing agent structure...")
    try:
        from cod_agents import CoD_Agents
        agents = CoD_Agents()
        
        print("✅ Agents initialized")
        print("   Note: Full agent test requires LLM API key")
        return True
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

async def test_integrations():
    """Test integration components"""
    print("\n🧪 Testing integrations...")
    try:
        from integrations import ActionEngine, IntercomIntegration, PlivoIntegration
        
        engine = ActionEngine()
        intercom = IntercomIntegration()
        plivo = PlivoIntegration()
        
        print("✅ Integrations initialized")
        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_ui():
    """Test that UI file exists"""
    print("\n🧪 Testing UI...")
    try:
        import os
        if os.path.exists("index.html"):
            with open("index.html", "r") as f:
                content = f.read()
                assert "DebateShield" in content
            print("✅ UI file present and valid")
            return True
        else:
            print("❌ index.html not found")
            return False
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🛡️  DebateShield Lite - System Tests")
    print("=" * 60)
    
    results = []
    
    # Synchronous tests
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("UI", test_ui()))
    
    # Async tests
    results.append(("Memory", await test_memory()))
    results.append(("You.com", await test_you_search()))
    results.append(("Agents", await test_agents()))
    results.append(("Integrations", await test_integrations()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {name}")
    
    print("=" * 60)
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to run.")
        print("\n💡 Next steps:")
        print("   1. Add API keys to .env")
        print("   2. Run: python run.py")
        print("   3. Visit: http://localhost:8000")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        print("   The system may still work with limited functionality.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
