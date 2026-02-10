"""
Processing stages: small, focused steps that transform data as it flows
through a pipeline (Input → Transform → Output).
"""

from .base import ProcessingStage
from .input_stage import InputStage
from .transform_stage import TransformStage
from .output_stage import OutputStage

__all__ = ["ProcessingStage", "InputStage", "TransformStage", "OutputStage"]
