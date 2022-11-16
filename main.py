import sys, os, subprocess, audioread

bitrate = 320 #(Kbps) don't need to modify if you are using target file size mode
out_ext = "mp3" #output file you want (decides the encoder you use as well)
target_size = 8 #in MB

encoders = {
    "mp3":"libmp3lame",
    "opus":"libopus",
    "ogg":"libopus",
    "aac":"aac",
    "m4a":"aac",
    "ac3":"ac3",
    "mp2":"mp2",
    "flac":"flac",
    "wav":"wavpack",
    "alac":"alac",
    }

directory = ""
outdirectory = ""
image_dir = "images"
extensions = [".flac",".mp3",".aac",".ogg",".wav",".m4a",".alac",".opus",".ac3",".mp2", ".mka"]
target_mode = False

if (os.path.isdir(image_dir)) == False:
    os.mkdir(image_dir)

if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == "-help" or sys.argv[i] == '-h':
            print('''
Welcome to Audio Converter by Fenway Powers
This program lets you convert entire folders of audio files with ease.

Usage:
python3 main.py -i [directory] -br [bitrate] -o [file extension] -target [size in MB]
            
Use -i to specify the directory you want to convert. If left blank, it will convert all the audio files in the program's directory.

Use -br to specify the bitrate of your audio in kbps. If left blank, default is 320kbps.

Use -o to specify the extension you want to output to. If left blank, MP3 is default.

Use -target if you want to convert all your files to a certain size (in MB).

Use -codec to specify the codec you would like to use. Only necessary if you are not going to use the default codecs for each extension.

Use -default_codec to view the default codecs for each extension.''')
            sys.exit(0)
        elif sys.argv[i] == "-default_codec" or sys.argv[i] == '-default':
            for enc in encoders:
                print(enc + ": " + encoders[enc])
            sys.exit(0)
        elif sys.argv[i] == "-br":
            if sys.argv[i+1].isdecimal and sys.argv[i+1]:
                bitrate = int(sys.argv[i+1])
            else:
                print("Error: Incorrect use of -br, proper use is: -br [bitrate]\nExample: -br 320")
                sys.exit(0)

            increment=True
        elif sys.argv[i] == "-o":
            cont = False
            if "."+sys.argv[i+1] in extensions:
                cont = True
                out_ext = sys.argv[i+1]
            
            if cont == False:
                print("Error: incorrect use of -o. Correct use is: -o [extension]\nExample: -o mp3")
                sys.exit(0)

        elif sys.argv[i] == "-codec":
            cont = False
            if "-" not in sys.argv[i+1]:
                for ext in encoders:
                    encoders[ext] = sys.argv[i+1]
                cont = True

        elif sys.argv[i] == "-i":
            if os.path.exists(sys.argv[i+1]):
                if sys.argv[i+1][len(sys.argv[i+1])-1] != "/":
                    directory = sys.argv[i+1]+"/"
                else:
                    directory = sys.argv[i+1]
            else:
                print("Error: incorrect use of -i. Correct use is: -i [path]\nMake sure your input was a real directory.\nExample: -i \'music/album\'")
                sys.exit(0)

        elif sys.argv[i] == "-target":
            if sys.argv[i+1].isdecimal:
                target_size = int(sys.argv[i+1])
                target_mode = True
            else:
                print("Error: incorrect use of -target. Correct use is: -target [size]\nExample: -target 6")
                sys.exit(0)

if outdirectory == "":
    outdirectory = directory+out_ext

if directory != "":
    dir_list = os.listdir(directory)
else:
    dir_list = os.listdir()

if (os.path.isdir(outdirectory)) == False:
    os.mkdir(outdirectory)

for file in dir_list:
    for ext in extensions:
        if ext in file:
            
            if target_mode:
                with audioread.audio_open(file) as f:
                        totalsec = f.duration
                bitrate = int((target_size*8192)/(totalsec)) #math for calculating bitrate for target file size (in MB)

            cut = len(ext)

            img_dir = image_dir+"/"+file[0:-(cut)]+".jpg"

            subprocess.run(["ffmpeg","-y","-i",directory+file,"-an",img_dir])
            
            command = ["ffmpeg","-y","-i",directory+file,"-b:a",str(bitrate)+"k","-map_metadata","0","-map_metadata","0:s:0","-id3v2_version","3","-vn",outdirectory+"/"+file[0:-(cut)]+"."+out_ext]

            subprocess.run(command)
            
            if out_ext == "mp3" and (os.path.isfile(img_dir)):
                subprocess.run(["eyeD3","--add-image",img_dir+":FRONT_COVER",outdirectory+"/"+file[0:-(cut)]+"."+out_ext])

for img in os.listdir(image_dir):
    os.remove(image_dir+"/"+img)

os.rmdir(image_dir)
