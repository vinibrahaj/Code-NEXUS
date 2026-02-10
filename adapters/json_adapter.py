# codenexus/adapters/json_adapter.py
from __future__ import annotations

import json
from typing import Any, Union


class JSONAdapter:
    """
    Adapter = format bridge.
    It does NOT contain business logic; it just translates JSON <-> pipeline.
    """

    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id

    def process(self, data: Any, manager: "NexusManager") -> Union[str, Any]:
        # Accept either a JSON string or a python object.
        payload = json.loads(data) if isinstance(data, str) else data
        return manager.process_data(self.pipeline_id, payload)


# local import hint (prevents circular import in minimal examples)
from manager import NexusManager  # noqa: E402
