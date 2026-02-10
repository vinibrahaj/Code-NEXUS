# codenexus/stages/transform_stage.py
from __future__ import annotations

from typing import Any, Dict


class TransformStage:
    """
    Goal: business-ish transformations, but still minimal.

    Typical examples:
    - normalize field names
    - cast types
    - filter bad records to quarantine
    """

    def process(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        records = packet["records"]
        cleaned = []

        for rec in records:
            try:
                # Example normalization: strip string values (simple but realistic).
                normalized = {
                    k: (v.strip() if isinstance(v, str) else v)
                    for k, v in rec.items()
                }

                # Example "validation": if a record has no fields, quarantine it.
                if not normalized:
                    raise ValueError("empty record")

                cleaned.append(normalized)

            except Exception as exc:
                packet["quarantine"].append({"record": rec, "reason": str(exc)})
                packet["metrics"]["quarantined_count"] += 1
                packet["metrics"]["error_count"] += 1

        packet["records"] = cleaned
        return packet
