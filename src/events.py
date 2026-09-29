"""Data structures for speech recognition events and results."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json


@dataclass
class TranscriptionResult:
    """Represents a speech recognition result from sherpa-onnx."""

    text: str
    tokens: List[str] = field(default_factory=list)
    timestamps: List[float] = field(default_factory=list)
    ys_probs: List[float] = field(default_factory=list)
    segment_id: int = 0
    start_time: float = 0.0
    is_endpoint: bool = False
    raw_json: str = ""
    raw_dict: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_sherpa_json(
        cls,
        json_str: str,
        segment_id: int = 0,
        is_endpoint: bool = False,
    ) -> "TranscriptionResult":
        """Build a TranscriptionResult from sherpa-onnx's get_result_as_json_string output."""
        try:
            data = json.loads(json_str)
        except Exception:
            data = {}

        return cls(
            text=data.get("text", ""),
            tokens=data.get("tokens", []),
            timestamps=data.get("timestamps", []),
            ys_probs=data.get("ys_probs", []),
            segment_id=segment_id,
            start_time=data.get("start_time", 0.0),
            is_endpoint=is_endpoint,
            raw_json=json_str,
            raw_dict=data,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary suitable for JSON serialization or web payload."""
        return {
            "text": self.text,
            "tokens": self.tokens,
            "timestamps": self.timestamps,
            "segment_id": self.segment_id,
            "start_time": self.start_time,
            "is_endpoint": self.is_endpoint,
            "raw": self.raw_dict,
        }
