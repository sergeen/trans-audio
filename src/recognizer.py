"""Wrapper around sherpa-onnx OnlineRecognizer for streaming ASR."""

from typing import Generator, Optional
import numpy as np
import sherpa_onnx

from src.config import ModelConfig
from src.events import TranscriptionResult


class SherpaRecognizer:
    """Encapsulates sherpa-onnx online transducer recognizer and stream management."""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.config.validate()

        self._recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
            tokens=str(self.config.tokens_path),
            encoder=str(self.config.encoder_path),
            decoder=str(self.config.decoder_path),
            joiner=str(self.config.joiner_path),
            num_threads=self.config.num_threads,
            sample_rate=self.config.sample_rate,
            feature_dim=self.config.feature_dim,
            decoding_method=self.config.decoding_method,
            enable_endpoint_detection=self.config.enable_endpoint,
            rule1_min_trailing_silence=self.config.rule1_min_trailing_silence,
            rule2_min_trailing_silence=self.config.rule2_min_trailing_silence,
            rule3_min_utterance_length=self.config.rule3_min_utterance_length,
            provider=self.config.provider,
        )
        self._stream: Optional[sherpa_onnx.OnlineStream] = None
        self._segment_id = 0
        self._last_result_text = ""
        self.reset()

    def reset(self) -> None:
        """Create or reset the active stream."""
        self._stream = self._recognizer.create_stream()
        self._last_result_text = ""

    def process_chunk(
        self,
        chunk: np.ndarray,
        sample_rate: int,
    ) -> Optional[TranscriptionResult]:
        """Feed an audio chunk to the recognizer and return updated result if changed.
        
        Returns:
            TranscriptionResult if there is new text or an endpoint was hit, None otherwise.
        """
        if self._stream is None:
            self.reset()

        self._stream.accept_waveform(sample_rate, chunk)

        while self._recognizer.is_ready(self._stream):
            self._recognizer.decode_stream(self._stream)

        is_endpoint = self.config.enable_endpoint and self._recognizer.is_endpoint(self._stream)
        json_str = self._recognizer.get_result_as_json_string(self._stream)

        result = TranscriptionResult.from_sherpa_json(
            json_str=json_str,
            segment_id=self._segment_id,
            is_endpoint=is_endpoint,
        )

        # Check if output changed or endpoint reached
        has_change = result.text != self._last_result_text

        if is_endpoint:
            self._recognizer.reset(self._stream)
            self._segment_id += 1
            self._last_result_text = ""
            # If there was text in this finished segment, emit it
            if result.text.strip():
                return result
            return None

        if has_change and result.text.strip():
            self._last_result_text = result.text
            return result

        return None

    def finish_stream(self) -> Optional[TranscriptionResult]:
        """Signal input finished and decode remaining frames."""
        if self._stream is None:
            return None

        self._stream.input_finished()
        while self._recognizer.is_ready(self._stream):
            self._recognizer.decode_stream(self._stream)

        json_str = self._recognizer.get_result_as_json_string(self._stream)
        result = TranscriptionResult.from_sherpa_json(
            json_str=json_str,
            segment_id=self._segment_id,
            is_endpoint=True,
        )
        self._stream = None
        if result.text.strip():
            return result
        return None
