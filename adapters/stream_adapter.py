# codenexus/adapters/stream_adapter.py
from __future__ import annotations

from typing import Any, Iterable, Union


class StreamAdapter:
    """
    Stream adapter (simulated):
    - data is an iterable of chunks/events
    - we combine into records and run the pipeline once

    In a real system you'd process per-chunk, but for a minimal repo demo,
    this still shows the pattern cleanly.
    """

    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id

    def process(self, data: Any, manager: "NexusManager") -> Union[str, Any]:
        if not isinstance(data, Iterable):
            raise TypeError("StreamAdapter expects an iterable of events/records.")

        records = []
        for item in data:
            if isinstance(item, dict):
                records.append(item)
            else:
                records.append({"value": item})

        return manager.process_data(self.pipeline_id, records)


from manager import NexusManager  # noqa: E402
