# codenexus/stages/base.py
from __future__ import annotations

from typing import Any, Protocol


class ProcessingStage(Protocol):
    """
    A tiny contract: if it has a .process(data) method, it can be a stage.
    We don't force inheritance—this is duck typing on purpose.
    """
    def process(self, data: Any) -> Any: ...
