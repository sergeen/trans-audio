"""Output callback handlers for dispatching speech recognition results."""

from abc import ABC, abstractmethod
import json
import sys
from typing import Callable

from src.events import TranscriptionResult


class BaseOutputCallback(ABC):
    """Abstract interface for speech recognition output handlers."""

    @abstractmethod
    def on_result(self, result: TranscriptionResult) -> None:
        """Handle a recognition result (partial update or finalized utterance)."""
        pass


class ConsoleOutputCallback(BaseOutputCallback):
    """Prints raw or formatted speech recognition results directly to stdout."""

    def __init__(self, format_mode: str = "raw"):
        """Initialize callback.
        
        Args:
            format_mode: One of 'raw' (sherpa raw json string), 'json' (indented json),
                         or 'compact' (live terminal line update).
        """
        self.format_mode = format_mode.lower()
        # Ensure stdout is utf-8 configured on Windows
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    def on_result(self, result: TranscriptionResult) -> None:
        if self.format_mode == "raw":
            status = "[ENDPOINT]" if result.is_endpoint else "[PARTIAL]"
            print(f"{status} {result.raw_json}", flush=True)

        elif self.format_mode == "json":
            status = "[ENDPOINT]" if result.is_endpoint else "[PARTIAL]"
            payload = {
                "status": status,
                "segment_id": result.segment_id,
                "text": result.text,
                "tokens": result.tokens,
                "timestamps": result.timestamps,
                "is_endpoint": result.is_endpoint,
                "raw_sherpa": result.raw_dict,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)

        elif self.format_mode == "compact":
            if result.is_endpoint:
                print(f"\r[Seg {result.segment_id:02d}] {result.text}", flush=True)
            else:
                print(f"\r[Seg {result.segment_id:02d}...] {result.text}", end="", flush=True)


class CallableOutputCallback(BaseOutputCallback):
    """Invokes a custom Python callable for each result.
    
    Ideal for bridging to a web interface (e.g., WebSocket send, FastAPI queue, EventEmitter).
    """

    def __init__(self, func: Callable[[TranscriptionResult], None]):
        self._func = func

    def on_result(self, result: TranscriptionResult) -> None:
        self._func(result)
