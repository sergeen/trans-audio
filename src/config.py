"""Configuration classes and default settings for the application."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional


@dataclass
class AudioConfig:
    """Audio capture configuration."""

    sample_rate: int = 16000
    chunk_duration_sec: float = 0.1  # 100ms per audio slice
    device_index: Optional[int] = None  # None for default input device

    @property
    def chunk_samples(self) -> int:
        return int(self.sample_rate * self.chunk_duration_sec)


@dataclass
class ModelConfig:
    """Paths and options for sherpa-onnx streaming recognizer model."""

    tokens_path: Path
    encoder_path: Path
    decoder_path: Path
    joiner_path: Path
    num_threads: int = 2
    sample_rate: int = 16000
    feature_dim: int = 80
    decoding_method: str = "greedy_search"
    enable_endpoint: bool = True
    rule1_min_trailing_silence: float = 2.4
    rule2_min_trailing_silence: float = 1.0
    rule3_min_utterance_length: float = 20.0
    provider: str = "cpu"

    def validate(self) -> None:
        """Ensure all required model files exist on disk."""
        for label, path in [
            ("tokens", self.tokens_path),
            ("encoder", self.encoder_path),
            ("decoder", self.decoder_path),
            ("joiner", self.joiner_path),
        ]:
            if not path.is_file():
                raise FileNotFoundError(
                    f"Model file for {label} not found at: {path.resolve()}"
                )


@dataclass
class AppConfig:
    """Top-level application configuration."""

    audio: AudioConfig = field(default_factory=AudioConfig)
    model: Optional[ModelConfig] = None
    output_format: str = "raw"  # Options: 'raw', 'json', 'compact'
