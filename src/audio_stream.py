"""Microphone capture and audio streaming using sounddevice."""

import queue
import sys
from typing import Any, Dict, Generator, List, Optional
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    print("Error: sounddevice is not installed. Please run: pip install sounddevice")
    sys.exit(1)

from src.config import AudioConfig


def list_input_devices() -> List[Dict[str, Any]]:
    """List all available audio input devices."""
    devices = sd.query_devices()
    default_input = sd.default.device[0]

    input_devices = []
    for idx, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            input_devices.append({
                "index": idx,
                "name": dev["name"],
                "channels": dev["max_input_channels"],
                "default_samplerate": dev["default_samplerate"],
                "is_default": (idx == default_input),
            })
    return input_devices


class AudioStreamer:
    """Manages audio capture from a microphone and yields PCM float32 chunks."""

    def __init__(self, config: AudioConfig):
        self.config = config
        self._audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        self._stream: Optional[sd.InputStream] = None
        self._running = False

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: Any,
        status: sd.CallbackFlags,
    ) -> None:
        """Callback invoked by sounddevice for incoming audio frames."""
        if status:
            # Drop/overflow warnings can be logged if needed
            pass
        if self._running:
            # Flatten to 1D float32 array
            self._audio_queue.put(indata.copy().flatten())

    def __enter__(self) -> "AudioStreamer":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()

    def start(self) -> None:
        """Start capturing audio from the input device."""
        if self._running:
            return

        self._running = True
        self._audio_queue = queue.Queue()
        self._stream = sd.InputStream(
            channels=1,
            dtype="float32",
            samplerate=self.config.sample_rate,
            blocksize=self.config.chunk_samples,
            device=self.config.device_index,
            callback=self._audio_callback,
        )
        self._stream.start()

    def stop(self) -> None:
        """Stop capturing audio and close the input stream."""
        self._running = False
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None

    def stream(self) -> Generator[np.ndarray, None, None]:
        """Yield audio chunks as they arrive from the microphone."""
        while self._running:
            try:
                chunk = self._audio_queue.get(timeout=0.2)
                yield chunk
            except queue.Empty:
                continue
