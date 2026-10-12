from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests


class SearchEngine:
    """Search engine integration for web searches."""

    def __init__(self, engine: str = "google") -> None:
        self.engine = engine
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.google_search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

    def search_google(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        if not self.google_api_key or not self.google_search_engine_id:
            return {
                "success": False,
                "message": "Google Search API credentials not configured. Please set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in .env",
                "results": [],
            }

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.google_api_key,
            "cx": self.google_search_engine_id,
            "num": num_results,
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("items", []):
                    results.append(
                        {
                            "title": item.get("title", ""),
                            "url": item.get("link", ""),
                            "snippet": item.get("snippet", ""),
                        }
                    )
                return {"success": True, "query": query, "results": results, "message": f"Found {len(results)} results."}
            else:
                return {"success": False, "message": f"Google API error: {response.status_code}", "results": []}
        except Exception as exc:  # pragma: no cover
            return {"success": False, "message": f"Search failed: {exc}", "results": []}

    def search_wikipedia(self, query: str, num_results: int = 3) -> Dict[str, Any]:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srinfo": "totalhits",
            "srprop": "snippet",
            "srlimit": num_results,
            "format": "json",
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("query", {}).get("search", []):
                    results.append(
                        {
                            "title": item.get("title", ""),
                            "url": f"https://en.wikipedia.org/wiki/{item.get('title', '').replace(' ', '_')}",
                            "snippet": item.get("snippet", ""),
                        }
                    )
                return {"success": True, "query": query, "results": results, "message": f"Found {len(results)} Wikipedia results."}
            else:
                return {"success": False, "message": f"Wikipedia API error: {response.status_code}", "results": []}
        except Exception as exc:  # pragma: no cover
            return {"success": False, "message": f"Wikipedia search failed: {exc}", "results": []}

    def search(self, query: str, engine: Optional[str] = None) -> Dict[str, Any]:
        chosen_engine = engine or self.engine
        if chosen_engine == "google":
            return self.search_google(query)
        elif chosen_engine == "wikipedia":
            return self.search_wikipedia(query)
        else:
            return {"success": False, "message": f"Unknown search engine: {chosen_engine}", "results": []}
