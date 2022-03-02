import os
from pyfiglet import Figlet

os.system("cls")
f = Figlet(font='slant')
print(f.renderText(' - VAI  - '))

print("[VAI] Loading modules...")
from moviepy.editor import *
import sys
import numpy as np

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

print("[VAI] Loading video...")
clip = VideoFileClip(sys.argv[1])
print("[VAI] Founding duration of " + str(clip.duration) + "...")

print("[VAI] Extracting audio...")
audioclip = clip.audio

print("[VAI] Saving audio...")
audioclip.write_audiofile(sys.argv[1].split(".")[0] + ".mp3")

print("[VAI] Extracting volume...")
cut = lambda i: audioclip.subclip(i,i+1).to_soundarray(fps=22000)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = []
for i in range(0,int(audioclip.duration-2)):
    printProgressBar(i, int(audioclip.duration-2), prefix='Progress:', suffix="Complete", length=50)
    volumes.append(volume(cut(i)))
#volumes = [volume(cut(i)) for i in range(0,int(audioclip.duration-2))]
vol = []
for element in volumes:
    vol.append(round(element * 1000))
print("[VAI] Founding " + str(len(volumes)) + " volumes...")

print(vol)

print("[VAI] Deleting saved audio...")
os.remove(sys.argv[1].split(".")[0] + ".mp3")

sub = []
i = 0
last = False
lastsub = 0
print("[VAI] Searching subclips...")
for element in vol:
    if element > 0:
        if last == False:
            if i != 0:
                lastsub = i - 1
            else:
                lastsub = i
            last = True
        elif last == True:
            if i != len(vol) - 1:
                if vol[i + 1] == 0:
                    sub.append((lastsub, i + 1))
                    last = False
            else:
                sub.append((lastsub, i + 1))
                last = False

    i += 1
if len(sub) == 0:
    print("[VAI] Error: Audio needed...")
    exit()
print("[VAI] Founding " + str(len(sub)) + " subclips...")

subclean = []
print("[VAI] Cleaning subclips...")
def clean():
    global sub
    for i in range(len(sub)):
        if i < len(sub) - 1:
            if sub[i][1] == sub[i + 1][0] or sub[i][1] == sub[i + 1][0] - 1:
                x = (sub[i][0], sub[i + 1][1])
                del sub[i]
                del sub[i]
                sub.insert(i, x)
                clean()
clean()
print("[VAI] Cleaning to " + str(len(sub)) + " subclips...")

if len(sub) == 1 and sub[0][0] == 0 and sub[0][1] == len(volumes):
    print("[VAI] Video already perfect...")
    exit()

print("[VAI] Cutting subclips...")
fullclip = clip.subclip(sub[0][0], sub[0][1])
del sub[0]
for i in range(len(sub)):
    fullclip = concatenate_videoclips([fullclip,clip.subclip(sub[i][0],sub[i][1])])

print("[VAI] Eliminated " + str(clip.duration - fullclip.duration) + "s...")
if input("[VAI] Render? [y]es | [n]o - ") == "y":
    pass
else:
    exit()

print("[VAI] Rendering fullclip...")
fullclip.write_videofile(sys.argv[1].split(".")[0] + "-Full.mp4")