# codenexus/adapters/csv_adapter.py
from __future__ import annotations

import csv
from io import StringIO
from typing import Any, Union


class CSVAdapter:
    """
    Minimal CSV adapter:
    - accepts CSV as a string
    - turns it into list[dict] using DictReader
    - hands it to the pipeline via the manager
    """

    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id

    def process(self, data: Any, manager: "NexusManager") -> Union[str, Any]:
        if not isinstance(data, str):
            raise TypeError("CSVAdapter expects CSV input as a string.")

        reader = csv.DictReader(StringIO(data))
        records = list(reader)
        return manager.process_data(self.pipeline_id, records)


from manager import NexusManager  # noqa: E402
