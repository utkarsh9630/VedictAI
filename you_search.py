# you_search.py
import httpx
from typing import List, Dict, Any
from config import config


class YouSearcher:
    def __init__(self):
        self.api_key = (config.YOU_API_KEY or "").strip()
        self.base_url = "https://ydc-index.io/v1/search"

    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        if not self.api_key:
            raise RuntimeError("YOU_API_KEY is missing")

        headers = {"X-API-Key": self.api_key}
        params = {"query": query, "count": int(num_results)}

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(self.base_url, headers=headers, params=params)
            # 🔥 Print once so you can verify server is using this code path
            print(f"[YouSearcher] {resp.status_code} query='{query[:50]}'")
            resp.raise_for_status()
            data = resp.json()

        web = (data.get("results") or {}).get("web") or []
        out: List[Dict[str, Any]] = []
        for item in web[:num_results]:
            snippets = item.get("snippets") or []
            snippet = snippets[0] if snippets else (item.get("description") or "")
            out.append(
                {
                    "title": (item.get("title") or "").strip(),
                    "url": (item.get("url") or "").strip(),
                    "snippet": (snippet or "").strip(),
                }
            )
        return out

    async def retrieve_evidence(self, claim: str) -> Dict[str, List[Dict[str, Any]]]:
        support = await self.search(claim, num_results=5)
        refute = await self.search(f"debunk {claim}", num_results=5)
        return {"support": support, "refute": refute, "all": support + refute}
