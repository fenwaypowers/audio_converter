# audio_converter
A python script that mass converts a folder of audio files into another audio file type using ffmpeg, eyeD3 and audioread.

## Prerequisites: 

* [ffmpeg](https://ffmpeg.org/ffmpeg.html)
* [eyeD3](https://eyed3.readthedocs.io/en/latest/)
* [audioread](https://pypi.org/project/audioread/)

## Usage

`python3 convert_audio.py -i [directory] -br [bitrate] -o [file extension] -target [size in MB]`

## Example Use

`python3 convert_audio.py -i 'HOME - Odyssey' -br 128 -o opus`
