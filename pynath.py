#!/usr/bin/python
import os
import sys
import getopt
import mad
import ID3
import tkFileDialog
import Tkinter

FORMAT_DESCRIPTOR = "#EXTM3U"
RECORD_MARKER = "#EXTINF"

def generate_list(name="songs_list.m3u", path=".",
                  sort=True, walk=False):
    """ generates the M3U playlist with the given file name

    and in the given path """

    fp = None
    try:
        try:
            if walk:
                # recursive version
                mp3_list = [os.path.join(root, i) for root, dirs, files in os.walk(path) for i in files \
                            if i[-3:] == "mp3"]
            else:
                # non recursive version
                mp3_list = [i for i in os.listdir(path) if i[-3:] == "mp3"]

            #print mp3_list

            if sort:
                mp3_list.sort()

            fp = file(name, "w")
            fp.write(FORMAT_DESCRIPTOR + "\n")

            for track in mp3_list:
                if not walk:
                    track = os.path.join(path, track)
                else:
                    track = os.path.abspath(track)
                # open the track with mad and ID3
                mf = mad.MadFile(track)
                id3info = ID3.ID3(track)
        
                # M3U format needs seconds but
                # total_time returns milliseconds
                # hence i convert them in seconds
                track_length = mf.total_time() / 1000
        
                # get the artist name and the title
                artist, title = id3info.artist, id3info.title

                # if artist and title are there
                if artist and title:
                    fp.write(RECORD_MARKER + ":" + str(track_length) + "," +\
                             artist + " - " + title + "\n")
                else:
                    fp.write(RECORD_MARKER + ":" + str(track_length) + "," +\
                             os.path.basename(track)[:-4] + "\n")

                # write the fullpath
                fp.write(track + "\n")
                
        except (OSError, IOError), e:
            print e
    finally:
        if fp:
            fp.close()

if __name__ == "__main__":

    root = Tkinter.Tk()
    root.withdraw()
    dirname = tkFileDialog.askdirectory(initialdir="/",  title='Choisi le dossier de ta playlist')

    playlistName = os.path.split(os.path.abspath(dirname))[1] + '.m3u'
    m3ufile = os.path.join(dirname, playlistName)

    print playlistName
    print m3ufile
    generate_list(name=m3ufile, path=dirname, sort=True, walk=True)
