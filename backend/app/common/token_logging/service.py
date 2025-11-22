from datetime import datetime
from typing import Dict, Any

SESSION_TOKEN_LOGGERS: dict[str, "TokenLoggerService"] = {}

class TokenLoggerService:
    def __init__(self, session_id: str):
        self.session_id = session_id
        # self.api_calls: list[Dict[str, Any]] = []
        # Session-level totals
        self.total_tokens = 0
        # Per-agent totals
        self.agent_totals: Dict[str, int] = {}
        # Per-agent API call entries
        self.agent_calls: Dict[str, list[Dict[str, Any]]] = {}

    def log_api_call(self, usage: Dict[str, Any], completion_kwargs: Dict[str, Any], agent: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": completion_kwargs.get("model"),
            "agent": agent,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }

        # update global totals
        self.total_tokens += entry["total_tokens"]

        # update per agent totals
        if agent not in self.agent_totals:
            self.agent_totals[agent] = 0
        self.agent_totals[agent] += entry["total_tokens"]

        # track per agent calls
        if agent not in self.agent_calls:
            self.agent_calls[agent] = []
        self.agent_calls[agent].append(entry)

        return entry

    def get_summary(self):
        return {
            "session_id": self.session_id,
            "total_tokens": self.total_tokens,
            "agents": {
                agent: {
                    "total_tokens": self.agent_totals.get(agent, 0),
                    "api_calls": self.agent_calls.get(agent, [])
                }
                for agent in self.agent_totals
            }
        }
