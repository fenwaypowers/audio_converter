# audio_converter
A python script that mass converts a folder of audio files into another audio file type using ffmpeg, eyeD3 and audioread.

Metadata is preserved, but image metadata is only preserved when converting to MP3. 

## Prerequisites: 

* [ffmpeg](https://ffmpeg.org/ffmpeg.html)
* [eyeD3](https://eyed3.readthedocs.io/en/latest/)
* [audioread](https://pypi.org/project/audioread/)
* [Python 3.9+](https://python.org)

To install the required packages, run:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

`python3 main.py -i [directory] -br [bitrate] -o [file extension] -target [size in MB]`

## Example Use

`python3 main.py -i 'HOME - Odyssey' -br 128 -o opus`

`python3 main.py -o opus -target 4`

`python3 main.py -help`

## Help Message
            
```
usage: main.py [-h] [-i INPUT_DIR] [-br BITRATE]
               [-o {mp3,opus,ogg,aac,m4a,ac3,mp2,flac,wav,alac}] [-t TARGET]
               [--codec CODEC]

Audio Converter by Fenway Powers

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Input directory containing audio files
  -br BITRATE, --bitrate BITRATE
                        Bitrate for audio in kbps
  -o {mp3,opus,ogg,aac,m4a,ac3,mp2,flac,wav,alac}, --output_ext {mp3,opus,ogg,aac,m4a,ac3,mp2,flac,wav,alac}
                        Output file extension
  -t TARGET, --target TARGET
                        Target file size in MB
  --codec CODEC         Custom codec to use for conversion
```
