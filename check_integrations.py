#!/usr/bin/env python3
"""
Quick script to check what's in your current integrations.py
and help you replace it with the new version
"""

import os

# Check if old integrations.py exists
if os.path.exists("integrations.py"):
    print("Found integrations.py in current directory")
    print("\nFirst 50 lines of your current file:")
    print("="*60)
    with open("integrations.py", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:50], 1):
            print(f"{i:3d}: {line}", end="")
    print("="*60)
    print(f"\nTotal lines: {len(lines)}")
    
    # Check for old classes
    content = "".join(lines)
    if "ComposioTwitter" in content and "ComposioActions" not in content:
        print("\nDETECTED: Old version of integrations.py")
        print("You need to replace this file with the new version")
        print("\nYour file has:")
        if "ComposioTwitter" in content:
            print("  - ComposioTwitter (OLD)")
        if "PlivoSMS" in content:
            print("  - PlivoSMS (should be removed)")
        if "ActionEngine" in content:
            print("  - ActionEngine (needs update)")
        
        print("\nNew version should have:")
        print("  - IntercomAlert")
        print("  - ComposioActions (NEW)")
        print("  - ActionEngine (updated)")
        print("\nReplace your integrations.py with the new file I provided")
    else:
        print("\nFile appears to be correct version")
else:
    print("No integrations.py found in current directory")
    print("Current directory:", os.getcwd())