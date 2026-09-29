"""Unit and integration tests for sherpa-onnx microphone transcription app."""

import wave
from pathlib import Path
import numpy as np
import pytest

from src.callbacks import ConsoleOutputCallback, CallableOutputCallback
from src.events import TranscriptionResult
from src.model_manager import resolve_model, PREDEFINED_MODELS
from src.recognizer import SherpaRecognizer


def test_model_resolver_english():
    config = resolve_model(lang="en", base_models_dir=Path("models"))
    assert config.tokens_path.exists()
    assert config.encoder_path.exists()
    assert config.decoder_path.exists()
    assert config.joiner_path.exists()
    # Ensure int8 was selected for 20M model on CPU
    assert "int8" in config.encoder_path.name


def test_model_resolver_spanish():
    config = resolve_model(lang="es", base_models_dir=Path("models"))
    assert config.tokens_path.exists()
    assert config.encoder_path.exists()
    assert config.decoder_path.exists()
    assert config.joiner_path.exists()


def test_transcription_result_parsing():
    json_sample = (
        '{"text": "HELLO WORLD", "tokens": [" HELLO", " WORLD"], '
        '"timestamps": [1.0, 1.5], "ys_probs": [-0.1, -0.2], "start_time": 0.0}'
    )
    res = TranscriptionResult.from_sherpa_json(json_sample, segment_id=1, is_endpoint=True)
    assert res.text == "HELLO WORLD"
    assert res.tokens == [" HELLO", " WORLD"]
    assert res.timestamps == [1.0, 1.5]
    assert res.segment_id == 1
    assert res.is_endpoint is True
    d = res.to_dict()
    assert d["text"] == "HELLO WORLD"
    assert d["segment_id"] == 1


def test_recognizer_end_to_end_english():
    config = resolve_model(lang="en", base_models_dir=Path("models"))
    recognizer = SherpaRecognizer(config)

    wav_path = Path("models/sherpa-onnx-streaming-zipformer-en-20M-2023-02-17/test_wavs/0.wav")
    assert wav_path.is_file()

    with wave.open(str(wav_path), "rb") as wf:
        sample_rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

    collected_results = []
    chunk_size = int(0.1 * sample_rate)  # 100ms
    for i in range(0, len(samples), chunk_size):
        chunk = samples[i:i + chunk_size]
        res = recognizer.process_chunk(chunk, sample_rate)
        if res:
            collected_results.append(res)

    final_res = recognizer.finish_stream()
    if final_res:
        collected_results.append(final_res)

    assert len(collected_results) > 0
    final_text = collected_results[-1].text
    assert "YELLOW LAMPS" in final_text


def test_callbacks():
    json_sample = '{"text": "TEST", "tokens": ["TEST"], "timestamps": [0.5]}'
    res = TranscriptionResult.from_sherpa_json(json_sample, segment_id=0, is_endpoint=False)

    captured = []
    cb = CallableOutputCallback(lambda r: captured.append(r))
    cb.on_result(res)
    assert len(captured) == 1
    assert captured[0].text == "TEST"

    # Test console callbacks for all formats without errors
    for fmt in ["raw", "json", "compact"]:
        console = ConsoleOutputCallback(format_mode=fmt)
        console.on_result(res)
