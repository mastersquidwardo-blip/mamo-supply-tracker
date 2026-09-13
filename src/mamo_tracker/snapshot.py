"""Load and validate snapshot JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import SnapshotInputs


REQUIRED = ("date", "m_obs", "tcg_boxes", "tcg_displays")


def load_snapshot(path: str | Path) -> SnapshotInputs:
    data = json.loads(Path(path).read_text())
    return parse_snapshot(data)


def parse_snapshot(data: dict[str, Any]) -> SnapshotInputs:
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        raise ValueError(f"snapshot missing keys: {missing}")
    notes = data.get("notes") or []
    if isinstance(notes, str):
        notes = [notes]
    return SnapshotInputs(
        date=str(data["date"]),
        m_obs=float(data["m_obs"]),
        tcg_boxes=float(data["tcg_boxes"]),
        tcg_displays=float(data["tcg_displays"]),
        a3p_box_bought=float(data.get("a3p_box_bought", 0) or 0),
        a3p_display_bought=float(data.get("a3p_display_bought", 0) or 0),
        notes=tuple(notes),
        confidence=str(data.get("confidence", "medium")),
    )
