"""
Concrete pipeline implementations.
A pipeline is a configured sequence of stages + execution policy.
"""

from .default_pipeline import DefaultPipeline

__all__ = ["DefaultPipeline"]
