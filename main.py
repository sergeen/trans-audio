#!/usr/bin/env python3
"""CLI entry point for sherpa-onnx real-time microphone speech recognition."""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.app import SpeechRecognitionApp
from src.audio_stream import list_input_devices
from src.callbacks import ConsoleOutputCallback
from src.config import AppConfig, AudioConfig
from src.model_manager import PREDEFINED_MODELS, resolve_model


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Real-time CPU microphone transcription using sherpa-onnx.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--lang",
        type=str,
        default="es",
        choices=list(PREDEFINED_MODELS.keys()),
        help=f"Language model to use ({', '.join(PREDEFINED_MODELS.keys())}).",
    )

    parser.add_argument(
        "--model-dir",
        type=str,
        default=None,
        help="Path to a custom model directory containing encoder, decoder, joiner, and tokens.txt.",
    )

    parser.add_argument(
        "--device",
        type=int,
        default=None,
        help="Audio input device index. Use --list-devices to view options.",
    )

    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List available audio input devices and exit.",
    )

    parser.add_argument(
        "--format",
        type=str,
        default="raw",
        choices=["raw", "json", "compact"],
        help="Output display format: 'raw' (sherpa raw json), 'json' (formatted), 'compact' (live terminal text).",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=2,
        help="Number of CPU threads for neural network inference.",
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Microphone sampling rate in Hz.",
    )

    return parser.parse_args()


def handle_list_devices() -> None:
    devices = list_input_devices()
    print("\nAvailable Audio Input Devices:")
    print("-" * 65)
    print(f"{'ID':<4} {'Default':<9} {'Channels':<10} {'Name'}")
    print("-" * 65)
    for dev in devices:
        default_mark = "[*]" if dev["is_default"] else ""
        print(f"{dev['index']:<4} {default_mark:<9} {dev['channels']:<10} {dev['name']}")
    print("-" * 65)
    print("Pass --device <ID> to choose a specific microphone.\n")


def main() -> None:
    args = parse_arguments()

    if args.list_devices:
        handle_list_devices()
        return

    # 1. Resolve model configuration (auto-downloads if not present)
    try:
        model_config = resolve_model(
            lang=args.lang,
            model_dir_path=args.model_dir,
            num_threads=args.threads,
        )
    except Exception as e:
        print(f"\n[Error] Failed to resolve model: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Build Audio and App config
    audio_config = AudioConfig(
        sample_rate=args.sample_rate,
        device_index=args.device,
    )
    app_config = AppConfig(
        audio=audio_config,
        model=model_config,
        output_format=args.format,
    )

    # 3. Create console output callback
    console_cb = ConsoleOutputCallback(format_mode=args.format)

    # 4. Instantiate and run application
    app = SpeechRecognitionApp(
        config=app_config,
        model_config=model_config,
        callbacks=[console_cb],
    )

    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
