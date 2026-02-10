# stages/output_stage.py
from __future__ import annotations

from typing import Any, Dict, List
import csv
import io


class OutputStage:
    """
    Final stage: serialize cleaned records into CSV text.
    """

    COLUMNS = ["id", "name", "age", "email"]

    def process(self, packet: Dict[str, Any]) -> str:
        records: List[dict] = packet.get("records", [])
        if not records:
            return ""

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=self.COLUMNS)

        writer.writeheader()
        for rec in records:
            writer.writerow({col: rec.get(col, "") for col in self.COLUMNS})

        return buffer.getvalue()

