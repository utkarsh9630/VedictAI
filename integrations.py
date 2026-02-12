# integrations.py
"""
Integration stubs for future workflow actions.
Currently disabled - focus is on core fact-checking functionality.
"""

from typing import Dict, Any


class ActionEngine:
    """
    Action engine for future workflow integrations.
    
    Planned integrations:
    - Intercom alerts for customer support
    - Composio for Twitter/Slack/Discord
    - Email notifications
    
    Currently: All actions disabled, returns stub responses
    """
    
    def __init__(self):
        # Integrations will be added in future versions
        pass
    
    async def execute_actions(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Placeholder for future action execution.
        Returns no-op results.
        """
        return {
            "intercom": {"sent": False, "reason": "Integration not enabled"},
            "composio": {"sent": False, "reason": "Integration not enabled"},
        }