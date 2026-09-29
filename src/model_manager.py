"""Model manager for resolving, downloading, and configuring sherpa-onnx models."""

import os
import sys
import tarfile
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple

from src.config import ModelConfig


PREDEFINED_MODELS: Dict[str, Dict[str, str]] = {
    "en": {
        "name": "sherpa-onnx-streaming-zipformer-en-20M-2023-02-17",
        "description": "Lightweight 20M quantized int8 English Zipformer model (CPU-optimized)",
        "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-en-20M-2023-02-17.tar.bz2",
    },
    "es": {
        "name": "sherpa-onnx-streaming-zipformer-es-kroko-2025-08-06",
        "description": "Spanish streaming Zipformer model (Kroko)",
        "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-es-kroko-2025-08-06.tar.bz2",
    },
}


def _download_and_extract(url: str, output_dir: Path) -> Path:
    """Download a tar.bz2 model archive with progress and extract it."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1]
    archive_path = output_dir / filename

    print(f"\n[ModelManager] Downloading {filename} from {url}...")

    def _progress(count: int, block_size: int, total_size: int):
        if total_size > 0:
            percent = min(100, int(count * block_size * 100 / total_size))
            mb = (count * block_size) / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            sys.stdout.write(f"\r[ModelManager] Progress: {percent}% ({mb:.1f}/{total_mb:.1f} MB)")
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, archive_path, reporthook=_progress)
        print("\n[ModelManager] Download complete. Extracting archive...")
        with tarfile.open(archive_path, "r:bz2") as tar:
            tar.extractall(path=output_dir)
        print("[ModelManager] Extraction complete.")
    finally:
        if archive_path.exists():
            archive_path.unlink()

    extracted_folder_name = filename.replace(".tar.bz2", "")
    return output_dir / extracted_folder_name


def discover_model_files(model_dir: Path) -> Tuple[Path, Path, Path, Path]:
    """Inspect a directory to automatically find encoder, decoder, joiner, and tokens.
    
    Prefers int8 models if available for optimal CPU performance.
    """
    if not model_dir.is_dir():
        raise FileNotFoundError(f"Model directory '{model_dir}' does not exist.")

    all_files = list(model_dir.iterdir())

    def find_file(prefix: str) -> Optional[Path]:
        # First preference: int8 models (e.g. encoder-xxx.int8.onnx or encoder.int8.onnx)
        int8_candidates = [
            f for f in all_files
            if f.name.startswith(prefix) and f.name.endswith(".int8.onnx")
        ]
        if int8_candidates:
            return sorted(int8_candidates)[0]

        # Second preference: standard onnx models
        onnx_candidates = [
            f for f in all_files
            if f.name.startswith(prefix) and f.name.endswith(".onnx")
        ]
        if onnx_candidates:
            return sorted(onnx_candidates)[0]
        return None

    encoder = find_file("encoder")
    decoder = find_file("decoder")
    joiner = find_file("joiner")

    tokens_candidates = [f for f in all_files if f.name == "tokens.txt" or f.name.endswith("tokens.txt")]
    tokens = tokens_candidates[0] if tokens_candidates else None

    missing = []
    if not encoder:
        missing.append("encoder (.onnx / .int8.onnx)")
    if not decoder:
        missing.append("decoder (.onnx / .int8.onnx)")
    if not joiner:
        missing.append("joiner (.onnx / .int8.onnx)")
    if not tokens:
        missing.append("tokens.txt")

    if missing:
        raise FileNotFoundError(
            f"Could not locate required model files in '{model_dir}': missing {', '.join(missing)}"
        )

    return encoder, decoder, joiner, tokens


def resolve_model(
    lang: Optional[str] = None,
    model_dir_path: Optional[str] = None,
    base_models_dir: Path = Path("models"),
    num_threads: int = 2,
) -> ModelConfig:
    """Resolve ModelConfig from a language code or an explicit model directory.
    
    If neither is provided or language model folder is not found, automatically downloads it.
    """
    if model_dir_path:
        target_dir = Path(model_dir_path)
    else:
        lang_code = (lang or "es").lower()
        if lang_code not in PREDEFINED_MODELS:
            supported = ", ".join(PREDEFINED_MODELS.keys())
            raise ValueError(f"Unknown language '{lang}'. Supported languages: {supported}")

        model_info = PREDEFINED_MODELS[lang_code]
        target_dir = base_models_dir / model_info["name"]

        if not target_dir.exists():
            print(f"[ModelManager] Model for '{lang_code}' not found locally.")
            target_dir = _download_and_extract(model_info["url"], base_models_dir)

    encoder, decoder, joiner, tokens = discover_model_files(target_dir)

    config = ModelConfig(
        encoder_path=encoder,
        decoder_path=decoder,
        joiner_path=joiner,
        tokens_path=tokens,
        num_threads=num_threads,
    )
    config.validate()
    return config
