from distutils.log import error
import json
from argparse import ArgumentParser
from lib2to3.pytree import Base
from ntpath import join
import os

def importConfig(path):
    try:
        with open(path, "r") as f:
            content = json.load(f)
            return content
    except BaseException as e:
        print('Error during JSON Import: {}'.format(e))
        SystemExit

def writeM3U(path, songPaths, musicPath):
    try:
        file = open(path, "w", encoding="utf-8")
        file.write("#EXTM3U\n")
        
        for i in songPaths:
            file.write("{}/{}\n".format(musicPath, i))
        print("Successfully written to: ", path)
        file.close()
    except BaseException as e:
        print('Error during M3U Write: {}'.format(e))
        SystemExit

def findSongPaths(MusicPath, songFiles):
    songPaths = []
    for i in songFiles:
        for dirpath, subdirs, files in os.walk(MusicPath):
            for x in files:
                if x == i.strip():
                    songPaths.append(x)
    return songPaths


def newM3UName(M3UPath):
    try:
        if 'New' in M3UPath:
            return M3UPath
        else:
          M3UPath =   M3UPath.rsplit('.',1)[0]
          M3UPath = M3UPath + 'New.m3u'
          return M3UPath
    except BaseException as e:
        print('Error While generating new M3U Name: {}'.format(e))
        SystemExit


def readM3U(path):
    try:
        file = open(path, 'r', encoding="utf-8")
        lines = file.readlines()
        file.close()
        return lines
    except BaseException as e:
        print('Error During M3U Read: {}'.format(e))
        SystemExit

def iterateSongs(songs):
    try:
        songs.pop(0)
        songFiles = []
        for i in range(len(songs)):
            if '/' in songs[i]:
                song = songs[i].rsplit('/', 1)[1]
                songFiles.append(song)
    except BaseException as e:
        print('Error Iterating M3U Songs: {}'.format(e))
    return songFiles

def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="configFile",help="Path to Config.Json", metavar="FILE")
    global args, jsonConfig
    args = parser.parse_args()
    jsonConfig =    importConfig(args.configFile)
    if "M3UPath" in jsonConfig:
        if jsonConfig["M3UPath"]:
            for dirpath, _, files in os.walk(jsonConfig["M3UPath"]):
                for x in files:
                    if '.m3u' in x:
                        lines =  readM3U(dirpath + '/' + x)
                        if lines:
                            songFiles = iterateSongs(lines)
                            songPaths = findSongPaths(jsonConfig["MusicPath"], songFiles)
                            newName = newM3UName(dirpath + '/' + x)
                            writeM3U(newName,songPaths, jsonConfig["MusicPath"])

main()