# codenexus/pipelines/default_pipeline.py
from __future__ import annotations

from typing import Any

from pipeline import ProcessingPipeline


class DefaultPipeline(ProcessingPipeline):
    """
    A concrete pipeline that:
    - runs stages
    - if the last stage returns a packet, updates out_records
    - returns whatever the last stage produced (packet or string)
    """

    def process(self, data: Any) -> Any:
        result = self._run_stages(data, tolerant=True)

        # If the pipeline ends on a packet, finalize metrics.
        if isinstance(result, dict) and "records" in result and "metrics" in result:
            result["metrics"]["out_records"] = len(result["records"])

        return result
