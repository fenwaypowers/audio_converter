import os
import subprocess
import audioread
import argparse
import tempfile
import shutil

# Define constants
DEFAULT_BITRATE = 320  # in Kbps
DEFAULT_OUT_EXT = "mp3"
DEFAULT_TARGET_SIZE = 8  # in MB

# Supported encoders based on file extension
ENCODERS = {
    "mp3": "libmp3lame",
    "opus": "libopus",
    "ogg": "libopus",
    "aac": "aac",
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


# Parse arguments using argparse
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
        "-br",
        "--bitrate",
        type=int,
        help="Bitrate for audio in kbps",
        default=DEFAULT_BITRATE,
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
    parser.add_argument("--codec", type=str, help="Custom codec to use for conversion")

    return parser.parse_args()


# Get output directory based on input directory and output extension
def get_output_directory(input_dir, output_ext):
    if input_dir:
        return os.path.join(input_dir, output_ext)
    return output_ext


# Calculate bitrate for target file size mode
def calculate_bitrate_for_target(file, target_size):
    with audioread.audio_open(file) as f:
        total_sec = f.duration
    return int((target_size * 8192) / total_sec)  # bitrate calculation


# Process each file for conversion
def process_files(
    input_dir, output_ext, bitrate, target_mode, target_size, codec, temp_dir
):
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
                if target_mode:
                    bitrate = calculate_bitrate_for_target(file, target_size)

                cut = len(ext)
                img_path = os.path.join(temp_dir, file[:-cut] + ".jpg")
                output_file = os.path.join(output_dir, file[:-cut] + "." + output_ext)

                # Extract album art
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        os.path.join(input_dir, file),
                        "-an",
                        img_path,
                    ]
                )

                # Convert audio file
                command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    os.path.join(input_dir, file),
                    "-b:a",
                    f"{bitrate}k",
                    "-map_metadata",
                    "0",
                    "-map_metadata",
                    "0:s:0",
                    "-id3v2_version",
                    "3",
                    "-vn",
                    output_file,
                ]

                if codec:
                    command.insert(6, "-c:a")
                    command.insert(7, codec)
                else:
                    command.insert(6, "-c:a")
                    command.insert(7, ENCODERS[output_ext])

                subprocess.run(command)

                # Embed album art if output is mp3
                if output_ext == "mp3" and os.path.isfile(img_path):
                    subprocess.run(
                        ["eyeD3", "--add-image", img_path + ":FRONT_COVER", output_file]
                    )


# Main function
def main():
    args = parse_arguments()

    input_dir = args.input_dir
    bitrate = args.bitrate
    output_ext = args.output_ext
    target_size = args.target
    codec = args.codec
    target_mode = target_size is not None

    # Create a temporary directory for storing images
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")

        # Process files for conversion
        process_files(
            input_dir, output_ext, bitrate, target_mode, target_size, codec, temp_dir
        )


if __name__ == "__main__":
    main()
