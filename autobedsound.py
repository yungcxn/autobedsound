
from __future__ import unicode_literals
import sys
import youtube_dl
import urllib
import shutil
import os
import PIL.Image
import glob
import tempfile
from pydub import AudioSegment
from tkinter import *


#python bedsound.py (ytlink) (00:00 (begin)) (00:00 (end)) Name Args idk

def create_spack(ytlinkarg, beginarg, endarg, namearg):

    if ytlinkarg is None or ytlinkarg is "":
        return
    if beginarg is None or beginarg is "":
        return
    if endarg is None or endarg is "":
        return
    if namearg is None or namearg is "":
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    ytlink = ytlinkarg
    begin = beginarg
    begin_min = int(begin.split(":")[0])
    begin_sec = int(begin.split(":")[1])
    begin_msec = int(begin.split(":")[2])
    end = endarg
    end_min = int(end.split(":")[0])
    end_sec = int(end.split(":")[1])
    end_msec = int(end.split(":")[2])
    name = namearg





    sound_path = name + "/assets/minecraft/sounds/mob/wither"

    if os.path.exists(sound_path):
        shutil.rmtree(sound_path);

    os.makedirs(sound_path)
    os.chdir(sound_path)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([ytlink])

    for file in glob.glob("*.mp3"):
        data = open(file, "r").read()
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(data)
        AudioSegment.from_mp3(f.name).export('temp.ogg', format='ogg')
        f.close()

        sound = AudioSegment.from_file("temp.ogg", format="ogg")

        print(begin_min)
        print(begin_sec)
        print(end_min)
        print(end_sec)

        span = sound[begin_min * 60 * 1000 + begin_sec * 1000 + begin_msec * 10: end_min * 60 * 1000 + end_sec * 1000 + end_msec * 10]
        span.export("death.ogg", format="ogg")
        os.remove("temp.ogg")
        break

    for file in glob.glob("*.mp3"):
        os.remove(file)

    os.chdir("..") #now in mob
    os.chdir("..") #now in sounds
    os.chdir("..") #now in minecraft
    os.chdir("..") #now in assets
    os.chdir("..") #now in "name"

    fpack = open("pack.mcmeta","w+")
    fpack.write('{\n\t"pack": {\n\t\t"pack_format": 1,\n\t\t"description": "created by cxn\'s bot"\n\t}\n}')
    fpack.close()

    img = PIL.Image.new('RGB', (16,16), (119, 3, 252))
    img.save("pack.png", "PNG")

    os.chdir("..") #now in parent of "name"

    #shutil.copy("./")

    #Folder: "Pack Name"
    #   ->Folder: "assets"
    #       -> "minecraft"
    #           -> "sounds"
    #               -> "mob"
    #                   -> "wither"
    #                       -> death.ogg
    #   -> pack.png
    #   -> pack.mcmeta
    #

master = Tk()
master.title("Can's autobedsound v1")
Label(master, text="YT:").grid(row=0)
Label(master, text="Begin (00:00:00)").grid(row=1)
Label(master, text="End (00:00:00)").grid(row=2)
Label(master, text="Name").grid(row=3)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
Button(master, text='Create', command= lambda: create_spack(e1.get(), e2.get(), e3.get(), e4.get())).grid(row=4, column=0, sticky=W, pady=4)

mainloop( )
