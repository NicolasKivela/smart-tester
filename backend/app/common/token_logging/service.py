from datetime import datetime
import requests
from typing import Dict, Any

class TokenLoggerService:
    def __init__(self, session_id: str, front_api_url: str | None = None):
        self.session_id = session_id
        self.front_api_url = front_api_url
        self.api_calls: list[Dict[str, Any]] = []
        self.total_tokens = 0

    def log_api_call(self, usage: Dict[str, Any], completion_kwargs: Dict[str, Any]):
        """Store one API call’s token usage."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": completion_kwargs.get("model"),
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }
        self.total_tokens += entry["total_tokens"]
        self.api_calls.append(entry)
        return entry

    def get_summary(self):
        """Return total token stats for this session."""
        return {
            "session_id": self.session_id,
            "total_tokens": self.total_tokens,
            "api_calls": self.api_calls,
        }

    def send_to_frontend(self):
        """Send session token stats to frontend endpoint."""
        if not self.front_api_url:
            return

        try:
            requests.post(
                f"{self.front_api_url}/tokens",
                json=self.get_summary(),
                timeout=5
            )
        except Exception as e:
            print(f"[TokenLogger] Failed to send data to frontend: {e}")