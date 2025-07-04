import os
import subprocess
import audioread
import argparse
import tempfile

# Default audio parameters (codec and its settings)
DEFAULT_CODEC = "libfdk_aac"
DEFAULT_AUDIO_PARAMS = ["-c:a", "libfdk_aac", "-vbr", "4"]
DEFAULT_OUT_EXT = "m4a"
DEFAULT_TARGET_SIZE = 8  # in MB

# Supported encoders based on file extension
ENCODERS = {
    "mp3": "libmp3lame",
    "opus": "libopus",
    "ogg": "libopus",
    "aac": "libfdk_aac",
    "m4a": "aac",
    "ac3": "ac3",
    "mp2": "mp2",
    "flac": "flac",
    "wav": "wavpack",
    "alac": "alac",
}

EXTENSIONS = [
    ".flac",
    ".mp3",
    ".aac",
    ".ogg",
    ".wav",
    ".m4a",
    ".alac",
    ".opus",
    ".ac3",
    ".mp2",
    ".mka",
]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Audio Converter by Fenway Powers")

    parser.add_argument(
        "-i",
        "--input_dir",
        type=str,
        help="Input directory containing audio files",
        default="",
    )
    parser.add_argument(
        "-o",
        "--output_ext",
        type=str,
        help="Output file extension",
        choices=ENCODERS.keys(),
        default=DEFAULT_OUT_EXT,
    )
    parser.add_argument(
        "-t", "--target", type=int, help="Target file size in MB", default=None
    )
    parser.add_argument(
        "--audio_params",
        nargs=argparse.REMAINDER,
        help="Custom audio codec and parameters (e.g. -c:a libfdk_aac -vbr 4)",
        default=DEFAULT_AUDIO_PARAMS,
    )

    return parser.parse_args()


def get_output_directory(input_dir, output_ext):
    if input_dir:
        return os.path.join(input_dir, output_ext)
    return output_ext


def calculate_bitrate_for_target(file, target_size):
    with audioread.audio_open(file) as f:
        total_sec = f.duration
    return int((target_size * 8192) / total_sec)  # bitrate in kbps


def process_files(input_dir, output_ext, target_mode, target_size, audio_params, temp_dir):
    if input_dir:
        files = os.listdir(input_dir)
    else:
        files = os.listdir()

    output_dir = get_output_directory(input_dir, output_ext)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for file in files:
        for ext in EXTENSIONS:
            if ext in file:
                cut = len(ext)
                input_path = os.path.join(input_dir, file)
                output_file = os.path.join(output_dir, file[:-cut] + "." + output_ext)
                img_path = os.path.join(temp_dir, file[:-cut] + ".jpg")

                # Extract album art
                subprocess.run(["ffmpeg", "-y", "-i", input_path, "-an", img_path])

                # Build command
                command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_path,
                    "-map_metadata",
                    "0",
                    "-map_metadata",
                    "0:s:0",
                    "-id3v2_version",
                    "3",
                    "-vn",
                ]

                # If target_mode is on, calculate bitrate and override audio_params
                if target_mode:
                    bitrate = calculate_bitrate_for_target(input_path, target_size)
                    command += ["-b:a", f"{bitrate}k", "-c:a", ENCODERS[output_ext]]
                else:
                    command += audio_params

                command.append(output_file)

                subprocess.run(command)

                # Embed album art if output is mp3
                if output_ext == "mp3" and os.path.isfile(img_path):
                    subprocess.run(
                        ["eyeD3", "--add-image", img_path + ":FRONT_COVER", output_file]
                    )


def main():
    args = parse_arguments()

    input_dir = args.input_dir
    output_ext = args.output_ext
    target_size = args.target
    audio_params = args.audio_params
    target_mode = target_size is not None

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")

        process_files(input_dir, output_ext, target_mode, target_size, audio_params, temp_dir)


if __name__ == "__main__":
    main()
