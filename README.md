# audio_converter
A python script that mass converts a folder of audio files into another audio file type using ffmpeg, eyeD3 and audioread.

Metadata is preserved, but image metadata is only preserved when converting to MP3. 

## Prerequisites: 

* [ffmpeg](https://ffmpeg.org/ffmpeg.html)
* [eyeD3](https://eyed3.readthedocs.io/en/latest/)
* [audioread](https://pypi.org/project/audioread/)

## Usage

`python3 main.py -i [directory] -br [bitrate] -o [file extension] -target [size in MB]`

## Example Use

`python3 main.py -i 'HOME - Odyssey' -br 128 -o opus`

`python3 main.py -o opus -target 4`

`python3 main.py -help`

## Help Message
            
* Use -i to specify the directory you want to convert. If left blank, it will convert all the audio files in the program's directory.

* Use -br to specify the bitrate of your audio in kbps. If left blank, default is 320kbps.

* Use -o to specify the extension you want to output to. If left blank, MP3 is default.

* Use -target if you want to convert all your files to a certain size (in MB).

* Use -codec to specify the codec you would like to use. Only necessary if you are not going to use the default codecs for each extension.

* Use -default_codec to view the default codecs for each extension.
