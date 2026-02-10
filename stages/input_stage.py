# codenexus/stages/input_stage.py
from __future__ import annotations

from typing import Any, Dict, List


class InputStage:
    """
    Goal: take 'whatever the adapter gives me' and produce a canonical packet.

    After this stage, everyone downstream can rely on a stable shape:
      {
        "records": [ {..}, {..}, ... ],
        "meta": {...},
        "metrics": {...},
        "errors": [...],
        "quarantine": [...]
      }
    """

    def process(self, data: Any) -> Dict[str, Any]:
        # If we're already in packet form, just ensure keys exist.
        if isinstance(data, dict) and "records" in data:
            packet = data
        else:
            # Otherwise, wrap raw data into a packet.
            packet = {"records": self._coerce_to_records(data)}

        packet.setdefault("meta", {})
        packet.setdefault("metrics", {
            "in_records": len(packet["records"]),
            "out_records": 0,
            "error_count": 0,
            "quarantined_count": 0,
            "stage_timings_ms": {},
        })
        packet.setdefault("errors", [])
        packet.setdefault("quarantine", [])
        return packet

    def _coerce_to_records(self, data: Any) -> List[dict]:
        """
        Keep this intentionally permissive:
        - list[dict] -> use it
        - dict -> treat as a single record
        - anything else -> represent as a single record under a 'value' key
        """
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            return data
        if isinstance(data, dict):
            return [data]
        return [{"value": data}]
