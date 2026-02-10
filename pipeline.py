# codenexus/pipeline.py
from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any, List

from stages.base import ProcessingStage


class ProcessingPipeline(ABC):
    """
    Owns stages and the mechanics of running them.
    Concrete pipelines decide policy via the abstract .process().
    """

    def __init__(self) -> None:
        self.stages: List[ProcessingStage] = []

    def add_stage(self, stage: ProcessingStage) -> "ProcessingPipeline":
        """
        Configuration-time method.
        Keep it simple: store the stage and allow chaining.
        """
        if not hasattr(stage, "process") or not callable(stage.process):  # type: ignore[attr-defined]
            raise TypeError("Stage must define a callable .process(data) method.")
        self.stages.append(stage)
        return self

    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Policy hook.
        A concrete pipeline can choose:
        - fail-fast vs tolerant
        - return packet vs return report string
        - enable/disable monitoring
        """
        raise NotImplementedError

    # ---- core orchestration (the "engine") ----

    def _run_stages(self, data: Any, *, tolerant: bool = True) -> Any:
        """
        Runs every stage in order.
        If tolerant=True, stage failures get recorded and the pipeline continues
        whenever possible.
        """
        current = data

        for stage in self.stages:
            stage_name = stage.__class__.__name__
            t0 = perf_counter()

            try:
                current = stage.process(current)
            except Exception as exc:
                current = self._handle_stage_error(current, stage_name, exc, tolerant=tolerant)
                if current is None:
                    # fail-fast path
                    raise

            elapsed_ms = int((perf_counter() - t0) * 1000)
            self._record_timing(current, stage_name, elapsed_ms)

        return current

    def _handle_stage_error(self, current: Any, stage_name: str, exc: Exception, *, tolerant: bool) -> Any:
        """
        Minimal recovery strategy:
        - If current is a packet, record the error and continue with the same packet.
        - Otherwise, either fail or wrap into a packet-like dict.
        """
        if isinstance(current, dict) and "metrics" in current:
            current.setdefault("errors", []).append({"stage": stage_name, "error": str(exc)})
            current["metrics"]["error_count"] = current["metrics"].get("error_count", 0) + 1
            return current

        if tolerant:
            # Wrap unknown data into something the later stages can still work with.
            return {
                "records": [],
                "meta": {},
                "metrics": {"in_records": 0, "out_records": 0, "error_count": 1, "quarantined_count": 0, "stage_timings_ms": {}},
                "errors": [{"stage": stage_name, "error": str(exc)}],
                "quarantine": [],
            }

        # fail-fast
        return None

    def _record_timing(self, current: Any, stage_name: str, elapsed_ms: int) -> None:
        """
        If we have a metrics dict, store stage timings there.
        If not, do nothing (pipeline remains generic).
        """
        if isinstance(current, dict):
            metrics = current.setdefault("metrics", {})
            timings = metrics.setdefault("stage_timings_ms", {})
            timings[stage_name] = elapsed_ms
