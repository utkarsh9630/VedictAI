#!/usr/bin/env python3
"""
Local test script for Composio integration
Tests Composio actions without running the full FastAPI app
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple config for testing
class TestConfig:
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
    COMPOSIO_ENTITY_ID = os.getenv("COMPOSIO_ENTITY_ID", "debateshield")
    INTERCOM_TOKEN = os.getenv("INTERCOM_TOKEN", "")
    INTERCOM_TARGET_ID = os.getenv("INTERCOM_TARGET_ID", "")

# Replace the config import
import sys
sys.modules['config'] = type('config', (), {'config': TestConfig})()

# Now import integrations
from integrations import ComposioActions, ActionEngine


async def test_composio_connections():
    """Test 1: List all Composio connections"""
    print("\n" + "="*60)
    print("TEST 1: List Composio Connections")
    print("="*60)
    
    composio = ComposioActions()
    
    if not composio.is_configured():
        print("Composio API key not configured!")
        print("   Set COMPOSIO_API_KEY in your .env file")
        return False
    
    print(f"Composio API Key: {composio.api_key[:20]}...")
    print(f"Entity ID: {composio.entity_id}")
    
    print("\nFetching connected accounts...")
    connections = await composio.list_connections()
    
    if "error" in connections:
        print(f"Error: {connections['error']}")
        return False
    
    print("\nConnected accounts:")
    if isinstance(connections, dict) and "items" in connections:
        for account in connections["items"]:
            app_name = account.get("appName", "Unknown")
            status = account.get("status", "Unknown")
            account_id = account.get("id", "Unknown")
            print(f"   • {app_name} (Status: {status}, ID: {account_id})")
    else:
        print(f"   Raw response: {connections}")
    
    return True


async def test_composio_twitter_post():
    """Test 2: Post to Twitter via Composio"""
    print("\n" + "="*60)
    print("TEST 2: Post to Twitter (DRY RUN)")
    print("="*60)
    
    composio = ComposioActions()
    
    if not composio.is_configured():
        print("Composio not configured")
        return False
    
    # Test tweet
    test_tweet = """🔍 Testing DebateShield Lite - AI-powered fact-checking system

Built with Chain-of-Debate architecture:
 Verifier Agent
 Skeptic Agent  
 Moderator Agent

#AI #FactCheck #Test"""
    
    print(f"\nTest tweet ({len(test_tweet)} chars):")
    print("-" * 40)
    print(test_tweet)
    print("-" * 40)
    
    # Ask for confirmation
    confirm = input("\n  This will post a REAL tweet. Continue? (yes/no): ")
    
    if confirm.lower() != "yes":
        print(" Aborted by user")
        return False
    
    print("\n Posting to Twitter...")
    result = await composio.post_to_twitter(test_tweet)
    
    if result.get("sent"):
        print(" Tweet posted successfully!")
        print(f"   Result: {result.get('result', {})}")
    else:
        print(f" Failed to post tweet")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    return result.get("sent", False)


async def test_composio_slack_message():
    """Test 3: Send Slack message via Composio"""
    print("\n" + "="*60)
    print("TEST 3: Send Slack Message (DRY RUN)")
    print("="*60)
    
    composio = ComposioActions()
    
    if not composio.is_configured():
        print(" Composio not configured")
        return False
    
    # Get channel from user
    channel = input("Enter Slack channel (e.g., #general): ").strip()
    if not channel:
        print(" No channel specified")
        return False
    
    test_message = """ *DebateShield Alert*

A high-risk claim was detected:

*Claim:* "Example misinformation claim"
*Verdict:* FALSE
*Confidence:* 92%
*Risk Level:* HIGH

_This is a test message from DebateShield Lite_"""
    
    print(f"\nTest message:")
    print("-" * 40)
    print(test_message)
    print("-" * 40)
    
    # Ask for confirmation
    confirm = input(f"\n⚠️  This will send a REAL message to {channel}. Continue? (yes/no): ")
    
    if confirm.lower() != "yes":
        print(" Aborted by user")
        return False
    
    print(f"\n Sending to Slack channel {channel}...")
    result = await composio.send_slack_message(channel, test_message)
    
    if result.get("sent"):
        print(" Message sent successfully!")
        print(f"   Result: {result.get('result', {})}")
    else:
        print(f" Failed to send message")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    return result.get("sent", False)


async def test_action_engine():
    """Test 4: Full ActionEngine with sample analysis"""
    print("\n" + "="*60)
    print("TEST 4: ActionEngine with Sample Analysis")
    print("="*60)
    
    engine = ActionEngine()
    
    # Sample high-risk analysis
    sample_analysis = {
        "claim": "Drinking bleach cures COVID-19",
        "verdict": "false",
        "confidence": 95,
        "risk_level": "high",
        "topic": "health",
        "explainability": {
            "why_bullets": [
                "Multiple health authorities (CDC, WHO) explicitly warn against bleach consumption",
                "Medical evidence shows bleach is toxic and can cause severe harm or death",
                "No peer-reviewed studies support this claim"
            ],
            "uncertainties": [],
            "debate_transcript": [
                {"agent": "verifier", "message": "No credible medical sources support this claim"},
                {"agent": "skeptic", "message": "Strong evidence of harm; this is dangerous misinformation"},
                {"agent": "moderator", "message": "Verdict: FALSE with high confidence due to clear medical consensus"}
            ]
        },
        "evidence_for": [],
        "evidence_against": [
            {
                "title": "CDC Warning",
                "url": "https://www.cdc.gov/coronavirus/2019-ncov/",
                "snippet": "Never drink bleach or use it internally"
            }
        ]
    }
    
    print("\n Sample Analysis:")
    print(f"   Claim: {sample_analysis['claim']}")
    print(f"   Verdict: {sample_analysis['verdict'].upper()}")
    print(f"   Confidence: {sample_analysis['confidence']}%")
    print(f"   Risk Level: {sample_analysis['risk_level'].upper()}")
    
    print("\n  Checking action policy...")
    print(f"   Risk={sample_analysis['risk_level']}, Confidence={sample_analysis['confidence']}%")
    
    if sample_analysis['risk_level'] == 'high' and sample_analysis['confidence'] >= 70:
        print("    Should trigger: Intercom + Composio")
    
    confirm = input("\n  Execute actions? (yes/no): ")
    
    if confirm.lower() != "yes":
        print(" Aborted by user")
        return False
    
    print("\n Executing actions...")
    results = await engine.execute_actions(sample_analysis)
    
    print("\n Results:")
    print(f"   Intercom: {' SENT' if results['intercom']['sent'] else ' NOT SENT'}")
    if not results['intercom']['sent']:
        print(f"      Reason: {results['intercom'].get('reason', 'Unknown')}")
    
    print(f"   Composio: {' SENT' if results['composio']['sent'] else ' NOT SENT'}")
    if not results['composio']['sent']:
        print(f"      Error: {results['composio'].get('error', 'Not configured')}")
    
    return True


async def main():
    """Main test runner"""
    print("\n" + "="*60)
    print(" DEBATESHIELD LITE - COMPOSIO INTEGRATION TESTS")
    print("="*60)
    
    # Check environment
    print("\n Environment Check:")
    composio_key = os.getenv("COMPOSIO_API_KEY", "")
    if composio_key:
        print(f"    COMPOSIO_API_KEY: {composio_key[:20]}...")
    else:
        print("    COMPOSIO_API_KEY: Not set")
    
    composio_entity = os.getenv("COMPOSIO_ENTITY_ID", "debateshield")
    print(f"    COMPOSIO_ENTITY_ID: {composio_entity}")
    
    if not composio_key:
        print("\n  Please set COMPOSIO_API_KEY in your .env file")
        print("   Get your API key from: https://app.composio.dev/settings")
        return
    
    # Interactive menu
    while True:
        print("\n" + "="*60)
        print("Select a test:")
        print("="*60)
        print("1. List Composio Connections")
        print("2. Post to Twitter (LIVE)")
        print("3. Send Slack Message (LIVE)")
        print("4. Test Full ActionEngine")
        print("5. Run All Tests (Safe)")
        print("0. Exit")
        print("="*60)
        
        choice = input("\nEnter choice (0-5): ").strip()
        
        if choice == "0":
            print("\n Goodbye!")
            break
        elif choice == "1":
            await test_composio_connections()
        elif choice == "2":
            await test_composio_twitter_post()
        elif choice == "3":
            await test_composio_slack_message()
        elif choice == "4":
            await test_action_engine()
        elif choice == "5":
            print("\n Running safe tests (no actual posts)...")
            await test_composio_connections()
        else:
            print(" Invalid choice")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user")
    except Exception as e:
        print(f"\n\n Error: {e}")
        import traceback
        traceback.print_exc()