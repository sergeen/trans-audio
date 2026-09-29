"""Core application orchestrator connecting audio capture, recognition, and callbacks."""

import signal
import sys
import threading
from typing import List, Optional

from src.audio_stream import AudioStreamer
from src.callbacks import BaseOutputCallback, ConsoleOutputCallback
from src.config import AppConfig, ModelConfig
from src.recognizer import SherpaRecognizer


class SpeechRecognitionApp:
    """Orchestrates microphone streaming and speech recognition."""

    def __init__(
        self,
        config: AppConfig,
        model_config: ModelConfig,
        callbacks: Optional[List[BaseOutputCallback]] = None,
    ):
        self.config = config
        self.model_config = model_config
        self.callbacks: List[BaseOutputCallback] = callbacks or []
        self._recognizer: Optional[SherpaRecognizer] = None
        self._streamer: Optional[AudioStreamer] = None
        self._stop_event = threading.Event()

    def add_callback(self, callback: BaseOutputCallback) -> None:
        """Register a new output callback."""
        self.callbacks.append(callback)

    def _dispatch_result(self, result) -> None:
        for cb in self.callbacks:
            try:
                cb.on_result(result)
            except Exception as e:
                print(f"[App] Error in callback {cb.__class__.__name__}: {e}", file=sys.stderr)

    def stop(self) -> None:
        """Signal the application to stop listening."""
        self._stop_event.set()
        if self._streamer:
            self._streamer.stop()

    def run(self) -> None:
        """Initialize models and run microphone recognition loop."""
        self._stop_event.clear()

        print("\n" + "=" * 60, flush=True)
        print("  SHERPA-ONNX REAL-TIME SPEECH RECOGNITION (CPU)", flush=True)
        print("=" * 60, flush=True)
        print(f"Model Encoder : {self.model_config.encoder_path.name}", flush=True)
        print(f"Model Decoder : {self.model_config.decoder_path.name}", flush=True)
        print(f"Model Joiner  : {self.model_config.joiner_path.name}", flush=True)
        print(f"Tokens file   : {self.model_config.tokens_path.name}", flush=True)
        print(f"Sample Rate   : {self.config.audio.sample_rate} Hz", flush=True)
        print(f"Threads (CPU) : {self.model_config.num_threads}", flush=True)
        print(f"Output Format : {self.config.output_format}", flush=True)
        print("=" * 60, flush=True)

        # Initialize recognizer
        print("[App] Initializing sherpa-onnx engine...", flush=True)
        self._recognizer = SherpaRecognizer(self.model_config)

        # Initialize audio capture
        self._streamer = AudioStreamer(self.config.audio)

        print("[App] Listening to microphone... (Press Ctrl + C to stop)\n", flush=True)

        # Set up graceful Ctrl+C handling
        def _sig_handler(sig, frame):
            print("\n[App] Stopping speech recognition...", flush=True)
            self.stop()

        signal.signal(signal.SIGINT, _sig_handler)

        try:
            with self._streamer as streamer:
                for chunk in streamer.stream():
                    if self._stop_event.is_set():
                        break

                    result = self._recognizer.process_chunk(
                        chunk=chunk,
                        sample_rate=self.config.audio.sample_rate,
                    )
                    if result is not None:
                        self._dispatch_result(result)

        finally:
            if self._recognizer:
                final_result = self._recognizer.finish_stream()
                if final_result:
                    self._dispatch_result(final_result)
            print("\n[App] Stopped gracefully.")
