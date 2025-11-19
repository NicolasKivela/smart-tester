from datetime import datetime
from typing import Dict, Any

SESSION_TOKEN_LOGGERS: dict[str, "TokenLoggerService"] = {}

class TokenLoggerService:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.api_calls: list[Dict[str, Any]] = []
        self.total_tokens = 0

    def log_api_call(self, usage: Dict[str, Any], completion_kwargs: Dict[str, Any],agent):
        """Store one API call’s token usage."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": completion_kwargs.get("model"),
            "agent": agent,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }
        self.total_tokens += entry["total_tokens"]
        self.api_calls.append(entry)
        return entry

    def get_summary(self):
        return {
            "session_id": self.session_id,
            "total_tokens": self.total_tokens,
            "api_calls": self.api_calls,
        }
