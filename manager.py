# codenexus/manager.py
from __future__ import annotations

from typing import Any, Dict, List

from pipeline import ProcessingPipeline


class NexusManager:
    """
    Orchestration layer:
    - registers pipelines
    - dispatches data into a selected pipeline
    - can run chains of pipelines (output of one feeds the next)
    """

    def __init__(self) -> None:
        self.pipelines: Dict[str, ProcessingPipeline] = {}

    def add_pipeline(self, pipeline_id: str, pipeline: ProcessingPipeline) -> None:
        if pipeline_id in self.pipelines:
            raise ValueError(f"Pipeline id '{pipeline_id}' already exists.")
        self.pipelines[pipeline_id] = pipeline

    def process_data(self, pipeline_id: str, data: Any) -> Any:
        pipeline = self._get(pipeline_id)
        return pipeline.process(data)

    def process_chain(self, pipeline_ids: List[str], data: Any) -> Any:
        """
        Pipeline chaining:
        output of pipeline[i] becomes input to pipeline[i+1].
        """
        current = data
        for pid in pipeline_ids:
            current = self.process_data(pid, current)
        return current

    def _get(self, pipeline_id: str) -> ProcessingPipeline:
        if pipeline_id not in self.pipelines:
            raise KeyError(f"Unknown pipeline '{pipeline_id}'.")
        return self.pipelines[pipeline_id]
