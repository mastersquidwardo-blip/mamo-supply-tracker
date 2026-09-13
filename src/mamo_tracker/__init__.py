"""MAMO Americas sell-through → print tracker (model v2.1)."""

__version__ = "0.2.1"

from .model import ModelParams, SnapshotInputs, compute
from .report import format_dashboard

__all__ = [
    "ModelParams",
    "SnapshotInputs",
    "compute",
    "format_dashboard",
    "__version__",
]
