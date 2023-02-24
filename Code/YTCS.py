#Youtube Content Saver Plugin
import pytube, os, glob, sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import Playlist, YouTube
from pytube.helpers import safe_filename
from pytube.exceptions import VideoPrivate
from waiting import wait
import time

playlist_flag = False
video_flag = False
video_paths = []
video_savenames = []
video_urls = []

#settings
download_video = True
download_audio = True

#Playlist-ID input
url = input("Enter a video or playlist URL: ")
if not url:
    print("You did not enter a video or playlist URL")
    quit()

#check if url is video or playlist and pick the video number from which to start
if "playlist" in url:
    playlist_flag = True
    try:
        first_video = int(input("Enter a number from which playlist entry to start: ")) - 1
    except:
        first_video = None
    if not first_video:
        print("No input given, download starts from first entry")
        first_video = 0
elif "watch" in url and "list" in url:
    while True:
        choice = input("Do you only want to download the video(v) or the playlist(p)?: ")
        if choice == "v":
            video_flag = True
            first_video = 0
            break
        elif choice == "p":
            playlist_flag = True
            url = "https://www.youtube.com/playlist?list=" + url.split("list=",1)[1].split("&index",1)[0] # takes the playlist id and appends it to a playlist link
            try:
                first_video = int(input("Enter a number from which playlist entry to start: ")) - 1
            except:
                first_video = None
            if not first_video:
                print("No input given, download starts from first entry")
                first_video = 0
            break
        else:
            print("Choice has to be between (v)video or (p)playlist: ")
        choice = None
elif "watch" in url and not "list" in url:
    video_flag = True
    first_video = 0
else:
    print("This is not a video or playlist URL")
    quit()

#Directory input
directory = input("Enter file directory: ")
if not directory:
    print("You did not enter a directory")
    quit()

#choose to download video
choice = input("Download video? (y/n): ")
if choice == "y":
    download_video = True
elif choice == "n":
    download_video = False
else:
    print(f"Default video download is set to {download_video}")
choice = None

#choose to download audio
choice = input("Download audio? (y/n): ")
if choice == "y":
    download_audio = True
elif choice == "n":
    download_audio = False
else:
    print(f"Default audio download is set to {download_audio}")
choice = None

#check if eather video or audio should be downloaded
if not (download_video or download_audio):
    print("What do you even want?!")
    quit()

def progress_function(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

def downloadVideo(links: list, save_directory: str, startpoint: int = 0, playlist_lenght: int = 1):
    list_number = startpoint
    list_itemcounter = 0
    for x in range(startpoint ,playlist_lenght):
        list_number += 1
        print(links[x])
        print("Currently working on: " + str(list_number) + "/" + str(len(links)))
        #try downloading until it works (to catch some occurring connection errors)
        while True:
            try:
                video = YouTube(links[x], on_progress_callback=progress_function)
                video_title = safe_filename(video.title)
                stream = video.streams
                video_stream = stream.get_highest_resolution()
                #create a save video title for saving
                if list_number:
                    video_savenames.append(str(list_number) + " " + video_title)
                else:
                    video_savenames.append(video_title)
                video_path = video_stream.download(save_directory, video_savenames[list_itemcounter] + ".mp4", skip_existing=True)
                video_paths.append(video_path)
            except pytube.exceptions.VideoUnavailable:
                print("Video is regional unavailable") #occurs only when regional unavailable?
                break
            except Exception as e:
                print(e)
                print("Error occured")
                continue
            break
        list_itemcounter += 1
"""
def downloadAudio(links: list, save_directory: str, startpoint: int = 0, playlist_lenght: int = 1):
    list_number = startpoint
    list_itemcounter = 0
    for x in range(startpoint ,playlist_lenght):
        list_number += 1
        print(links[x])
        print("Currently working on: " + str(list_number) + "/" + str(len(links)))
        #try downloading until it works (to catch some occurring connection errors)
        while True:
            try:
                video = YouTube(links[x])
                video_title = safe_filename(video.title)
                stream = video.streams
                video_stream = stream.get_audio_only()
                #create a save video title for saving
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
"""        

def convertVideo(links: list, paths: list, titles: list, save_directory:str, startpoint: int = 0, playlist_length: int = 1):
    list_itemcounter = 0
    for x in range(startpoint, playlist_length):
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
                mp4_vid.close()
        list_itemcounter += 1

def deleteMP4(del_directory):
    for file in glob.glob(os.path.join(del_directory, "*.mp4")):
        print(file) #check if path is choosen correctly
        while True:
            try:
                os.remove(file)
                break
            except Exception as e:
                print(f"{file} could not be deleted")
                print(e)
                pass

start_time = time.time()

#case: is video
if video_flag:
    #get video title
    video = YouTube(url)
    video_title = safe_filename(video.title)
    #creat folder for video
    video_folder_directory = directory + "/" + video_title
    if not os.path.exists(video_folder_directory):
        os.makedirs(video_folder_directory)
    if download_video:
        #create video directory
        video_directory = video_folder_directory + "/" + video_title + "(Video)" + "/"
        if not os.path.exists(video_directory):
            os.makedirs(video_directory)
    if download_audio:
        #create audio directory
        audio_directory = video_folder_directory + "/" + video_title + "(Audio)" + "/"
        if not os.path.exists(audio_directory):
            os.makedirs(audio_directory)
    video_urls.append(url)
    if download_video and download_audio:
        downloadVideo(video_urls, video_directory)
        convertVideo(video_urls, video_paths, video_savenames, audio_directory)
    elif download_video:
        downloadVideo(video_urls, video_directory)
    elif download_audio:
        downloadVideo(video_urls, audio_directory)
        convertVideo(video_urls, video_paths, video_savenames, audio_directory)
        deleteMP4(audio_directory)

#case: is playlist
elif playlist_flag:
    #get playlist title
    playlist = Playlist(url)
    try:
        playlist_title = playlist.title
    except:
        print("Can not access playlist. Check if playlist is set to private.")
        quit()
    #create playlist directory
    playlist_directory = directory + "/" + playlist_title
    if not os.path.exists(playlist_directory):
        os.makedirs(playlist_directory)
    if download_video:
        #create video directory
        video_directory = playlist_directory + "/" + playlist_title + " (Video)" + "/"
        if not os.path.exists(video_directory):
            os.makedirs(video_directory)
    if download_audio:
        #create audio directory
        audio_directory = playlist_directory + "/" + playlist_title + " (Audio)" + "/"
        if not os.path.exists(audio_directory):
            os.makedirs(audio_directory)

    try:
        playlist_itemcount = playlist.length
        #gives error if playlist has only one video
    except:
        playlist_itemcount = 1
    video_urls = playlist.video_urls
    if download_video and download_audio:
        downloadVideo(video_urls, video_directory, first_video, playlist_itemcount)
        convertVideo(video_urls, video_paths, video_savenames, audio_directory, first_video, playlist_itemcount)
    elif download_video:
        downloadVideo(video_urls, video_directory, first_video, playlist_itemcount)
    elif download_audio:
        downloadVideo(video_urls, audio_directory, first_video, playlist_itemcount)
        convertVideo(video_urls, video_paths, video_savenames, audio_directory, first_video, playlist_itemcount)
        deleteMP4(audio_directory)
    
    print('Playlist has been saved with ' + str(playlist_itemcount) + ' entries')

else:
    print("URL was not a downloadable source")

delta_time = time.time() - start_time
delta_time_formated = time.strftime("%H:%M:%S", time.gmtime(delta_time))
print(f"Download finished in {delta_time_formated}!")