"""
Format adapters: turn external formats (CSV/JSON/stream) into Python records,
then route them into a pipeline via the NexusManager.
"""

from .csv_adapter import CSVAdapter
from .json_adapter import JSONAdapter
from .stream_adapter import StreamAdapter

__all__ = ["CSVAdapter", "JSONAdapter", "StreamAdapter"]
