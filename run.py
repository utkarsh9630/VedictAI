#!/usr/bin/env python3
"""
DebateShield Lite - Startup Script
"""
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import openai
        import aiosqlite
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False

def check_env():
    """Check environment configuration"""
    from dotenv import load_dotenv
    load_dotenv()
    
    warnings = []
    
    if not os.getenv("LLM_API_KEY"):
        warnings.append("LLM_API_KEY not set - LLM features will fail")
    
    if not os.getenv("YOU_API_KEY"):
        warnings.append("YOU_API_KEY not set - will use mock search results")
    
    if not os.getenv("INTERCOM_TOKEN"):
        warnings.append("INTERCOM_TOKEN not set - alerts will be simulated")
    
    if not os.getenv("PLIVO_AUTH_ID"):
        warnings.append("PLIVO credentials not set - SMS will be simulated")
    
    if warnings:
        print("\n⚠️  Configuration warnings:")
        for w in warnings:
            print(f"   • {w}")
        print("\n💡 Copy .env.example to .env and add your API keys")
        print("   The app will still run with mock/simulated integrations\n")
    else:
        print("✅ All API keys configured")
    
    return True

def main():
    """Main startup function"""
    print("=" * 60)
    print("🛡️  DebateShield Lite - Starting Up")
    print("=" * 60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    check_env()
    
    # Start the server
    print("\n🚀 Starting FastAPI server...")
    print("📍 URL: http://localhost:8000")
    print("📊 API Docs: http://localhost:8000/docs")
    print("💾 Health Check: http://localhost:8000/health")
    print("\nPress CTRL+C to stop\n")
    print("=" * 60)
    print()
    
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down DebateShield Lite...")
        print("   Thanks for using the system!")
        sys.exit(0)
