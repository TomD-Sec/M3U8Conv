''' M3U exported Android to local PC Converter
    Converts M3U music playlist file entries from an android format to the format matching your local PC.
    Copyright (C) 2023  Thomas Davey-Spence

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

from distutils.log import error
from ntpath import join
import os

def writeM3U(path, songPaths, musicPath):
    '''Write the songPaths to the output path.'''
    try:
        #Open for writing, write the M3U identifier.
        file = open(path, "w", encoding="utf-8")
        file.write("#EXTM3U\n")
        
        #Write the songs line by line.
        for i in songPaths:
            file.write("{}/{}\n".format(musicPath, i))
        print("Successfully written to: ", path)
        file.close()
    except BaseException as e:
        raise Exception('Error Writing Song: {}'.format(e))


def findSongPaths(MusicPath, songFiles):
    '''Searches MusicPath for the files stored in songFiles. Returns the path of new songFiles. Songs which are not found will not be added to the list.'''
    songPaths = []
    for i in songFiles:
        #Walk through the MusicPath.
        for dirpath, subdirs, files in os.walk(MusicPath):
            for x in files:
                #If the files match append to the list of songPaths.
                if x == i.strip():
                    songPaths.append(x)
    return songPaths


def newM3UName(M3UPath, outputPath):
    '''Create the new output file path.'''
    try:
        #Remove the filename from the path.
          M3UPath =   M3UPath.rsplit('/',1)[1]
          #Add to the output path.
          return outputPath + '/' + M3UPath
    except BaseException as e:
        raise Exception('Error creating new name: {}'.format(e))



def readM3U(path):
    '''Read the contents of the M3U file line by line. Return the lines as a list.'''
    try:
        file = open(path, 'r', encoding="utf-8")
        lines = file.readlines()
        file.close()
        return lines
    except BaseException as e:
        raise Exception('Error reading song: {}'.format(e))
        

def iterateSongs(songs):
    '''iterate through the songs, accessing the song name from the list. Return the list of only the song names.'''
    try:
        #Pop the #EXTM3U value.
        songs.pop(0)

        songFiles = []
        for i in range(len(songs)):
            #Check the path contains a / to prevent runtime errors.
            if '/' in songs[i]:
                #Obtain the songs filename.
                song = songs[i].rsplit('/', 1)[1]
                songFiles.append(song)
    except BaseException as e:
        raise Exception('Error Iterating M3U Songs: {}'.format(e))
    return songFiles
