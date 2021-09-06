#Youtube Content Saver Plugin
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import pytube 
from pytube import Playlist, YouTube
from pytube.helpers import safe_filename
from waiting import wait

playlist_flag = False
video_flag = False
video_paths = []
video_savenames = []
video_urls = []

#Playlist-ID input
url = input("Enter a video or playlist url: ")
if not url:
    print("You did not enter a video or playlist url")
    quit()
    
#Directory input
directory = input("Enter file directory: ")
if not directory:
    print("You did not enter a directory")
    quit()

#check if link is video or playlist
if "watch" in url:
    video_flag = True
if "playlist" in url:
    playlist_flag = True

def downloadVideo(links: list, save_directory: str):
    list_number = 0
    list_itemcounter = 0
    for link in links:
        list_number += 1
        print(link)
        print("Currently working on: " + str(list_number) + "/" + str(len(links)))
        #try downloading until it works (to catch some occurring connection errors)
        while True:
            try:
                video = YouTube(link)
                video_title = safe_filename(video.title)
                stream = video.streams
                video_stream = stream.get_highest_resolution()
                #create a save for saving video title
                if list_number:
                    video_savenames.append(str(list_number) + " " + video_title)
                else:
                    video_savenames.append(video_title)
                video_path = video_stream.download(save_directory, video_savenames[list_itemcounter] + ".mp4", skip_existing=True)
                video_paths.append(video_path)
            except pytube.exceptions.VideoUnavailable:
                print("Video is regional unavailable")
                break
            except Exception as e:
                print(e)
                continue
            break
        list_itemcounter += 1
        

def convertVideo(links: list, paths: list, titles: list, save_directory:str):
    list_itemcounter = 0
    for link in links:
        #wait for video to be saved succesfully
        while True:
            try:
                wait(lambda: os.path.isfile(paths[list_itemcounter]), timeout_seconds = 30, waiting_for= "Download to finish")
                break
            except:
                continue
        save_video_title = safe_filename(titles[list_itemcounter])
        if not os.path.isfile(os.path.join(save_directory, save_video_title + ".mp3")):
                mp4_vid = VideoFileClip(paths[list_itemcounter])        
                mp4_vid.audio.write_audiofile(os.path.join(audio_directory, save_video_title + ".mp3"))
        list_itemcounter += 1

#case: is video
if video_flag:
    #create video directory
    video_directory = directory
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)
    #create audio directory
    audio_directory = directory
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)
    video_urls.append(url)
    downloadVideo(video_urls, video_directory)
    convertVideo(video_urls, video_paths, video_savenames, audio_directory)    

#case: is playlist
elif playlist_flag:
    #get playlist title
    playlist = Playlist(url)
    playlist_title = playlist.title
    #create playlist directory
    playlist_directory = directory + "/" + playlist_title
    if not os.path.exists(playlist_directory):
        os.makedirs(playlist_directory)
    #create video directory
    video_directory = playlist_directory + "/" + playlist_title + " (Video)" + "/"
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)
    #create audio directory
    audio_directory = playlist_directory + "/" + playlist_title + " (Audio)" + "/"
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    try:
        playlist_itemcount = playlist.length
        #gives error if playlist has only one video
    except:
        playlist_itemcount = 1
    video_number = 0 
    video_urls = playlist.video_urls
    downloadVideo(video_urls, video_directory)
    convertVideo(video_urls, video_paths, video_savenames, audio_directory)
    
    print('Playlist has been saved with ' + str(playlist_itemcount) + ' entries')

else:
    print("Links was not a downloadable source")


