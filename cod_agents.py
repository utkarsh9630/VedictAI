"""Chain-of-Debate agents: Verifier, Skeptic, Moderator"""
import json
from typing import Dict, Any, List
from openai import AsyncOpenAI
from config import config

class CoD_Agents:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.LLM_API_KEY)
        self.model = config.LLM_MODEL
    
    async def _call_llm(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Call LLM and parse JSON response"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        
        except Exception as e:
            print(f"LLM call error: {e}")
            return {"error": str(e)}
    
    async def verifier_agent(self, claim: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verifier agent argues the claim could be true"""
        system_prompt = """You are the VERIFIER agent in a Chain-of-Debate system.

Goal: Argue the claim could be true or partially true, using ONLY the provided search results.

Output STRICT JSON with this structure:
{
  "stance": "support|partial_support|unclear",
  "key_points": ["point1", "point2"],
  "evidence_for": [
    {"title": "...", "url": "...", "snippet": "...", "supports": "why this supports the claim"}
  ],
  "questions_for_skeptic": ["question1", "question2"],
  "confidence_support": 75
}

Rules:
- Do NOT invent facts
- Use only information from provided search results
- Prefer reputable sources
- If evidence is weak, say "unclear"
- Confidence should reflect strength of evidence"""

        user_message = f"""Claim: {claim}

Search Results:
{json.dumps(search_results, indent=2)}

Analyze and provide your JSON response."""

        return await self._call_llm(system_prompt, user_message)
    
    async def skeptic_agent(self, claim: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Skeptic agent argues the claim is false or misleading"""
        system_prompt = """You are the SKEPTIC agent in a Chain-of-Debate system.

Goal: Argue the claim is false, misleading, or lacks evidence, using ONLY the provided search results.

Output STRICT JSON with this structure:
{
  "stance": "refute|misleading|unclear",
  "key_points": ["point1", "point2"],
  "evidence_against": [
    {"title": "...", "url": "...", "snippet": "...", "refutes": "why this refutes the claim"}
  ],
  "questions_for_verifier": ["question1", "question2"],
  "confidence_refute": 80,
  "risk_flags": ["health", "emergency", "finance", "scam", "none"]
}

Rules:
- No hallucinations
- Use only information from provided search results
- If you can't refute, say "unclear"
- Flag potential harm conservatively
- Confidence should reflect strength of counter-evidence"""

        user_message = f"""Claim: {claim}

Search Results:
{json.dumps(search_results, indent=2)}

Analyze and provide your JSON response."""

        return await self._call_llm(system_prompt, user_message)
    
    async def moderator_agent(
        self, 
        claim: str, 
        verifier_output: Dict[str, Any],
        skeptic_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Moderator adjudicates and produces final verdict"""
        system_prompt = """You are the MODERATOR agent in a Chain-of-Debate system.

Your job: Review the Verifier and Skeptic arguments and make a final decision.

Output STRICT JSON with this structure:
{
  "verdict": "true|false|mixed|uncertain",
  "confidence": 85,
  "risk_level": "low|medium|high",
  "topic": "health|finance|emergency|politics|general",
  "why_bullets": [
    "Reason 1 for verdict",
    "Reason 2 for verdict"
  ],
  "uncertainties": [
    "Area of uncertainty 1",
    "Area of uncertainty 2"
  ],
  "debate_transcript": [
    {"agent": "verifier", "message": "Summary of verifier's main argument"},
    {"agent": "skeptic", "message": "Summary of skeptic's main argument"},
    {"agent": "moderator", "message": "Final decision rationale"}
  ],
  "reply_templates": {
    "neutral": "Brief neutral response",
    "firm_mod": "Firm moderation response",
    "friendly": "Friendly educational response"
  }
}

Decision rules:
- Strong reputable refutation → false
- Both sides have merit → mixed
- Weak/conflicting evidence → uncertain
- List specific uncertainties for mixed/uncertain

Risk assessment:
- health/emergency → high
- finance/scam/security → medium or high
- politics/rumors → low or medium
- opinions/harmless → low"""

        user_message = f"""Claim: {claim}

VERIFIER OUTPUT:
{json.dumps(verifier_output, indent=2)}

SKEPTIC OUTPUT:
{json.dumps(skeptic_output, indent=2)}

Provide your final adjudication in JSON format."""

        return await self._call_llm(system_prompt, user_message)
    
    async def run_debate(
        self, 
        claim: str, 
        evidence: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Run the full Chain-of-Debate process"""
        # Verifier argues for the claim
        verifier_output = await self.verifier_agent(claim, evidence["all"])
        
        # Skeptic argues against the claim
        skeptic_output = await self.skeptic_agent(claim, evidence["all"])
        
        # Moderator adjudicates
        moderator_output = await self.moderator_agent(claim, verifier_output, skeptic_output)
        
        # Combine evidence from both agents
        evidence_for = verifier_output.get("evidence_for", [])
        evidence_against = skeptic_output.get("evidence_against", [])
        
        return {
            **moderator_output,
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "verifier_stance": verifier_output.get("stance"),
            "skeptic_stance": skeptic_output.get("stance")
        }
