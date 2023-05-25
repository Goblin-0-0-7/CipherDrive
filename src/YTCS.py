#YouTube Content Saver
import pytube, os, glob, logging
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import Playlist, YouTube
from pytube.helpers import safe_filename
from pytube.exceptions import VideoPrivate
from waiting import wait
import time
import logging
import Hellpers as hell

""" Terminal Version
#Playlist-ID input
url = input("Enter a video or playlist URL: ")
if not url:
    print("You did not enter a video or playlist URL")
    quit()

#Directory input
directory = input("Enter file directory: ")
if not dir:
    print("You did not enter a directory")
    quit()

#choose to download video
choice = input("Download video? (y/n): ")
if choice == "y":
    download_video = True
elif choice == "n":
    download_video = False
else:
    print(f"Default video download is set to True")
choice = None

#choose to download audio
choice = input("Download audio? (y/n): ")
if choice == "y":
    download_audio = True
elif choice == "n":
    download_audio = False
else:
    print(f"Default audio download is set to True")
choice = None

#check if eather video or audio should be downloaded
if not (download_video or download_audio):
    print("What do you even want?!")
    quit()
"""

""" Terminal Version    
def check_url(url):
    #check if url is video or playlist and pick the video number from which to start
    #returns type ("playlist" or "video")
    if "playlist" in url:
        flag = "playlist"
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
                flag = "video"
                first_video = 0
                break
            elif choice == "p":
                flag = "playlist"
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
        flag = "video"
        first_video = 0
    else:
        print("This is not a video or playlist URL")
        quit()

    return flag, first_video, url
"""

class Downloader:

    def __init__(self, progressBar_video, download_info, callback):
        self.progressBar_video = progressBar_video
        self.download_info = download_info
        self.callback = callback
        self.logger = logging.getLogger("CipherDrive")
        self.error_count = 0
        self.warning_count = 0
        self.not_deleted_files = 0

    def progress_function(self, stream, chunk, bytes_remaining):
        filesize = stream.filesize
        current = ((filesize - bytes_remaining)/filesize)
        percent = ('{0:.1f}').format(current*100)
        
        self.progressBar_video.setValue(int(float(percent)))

        """ Terminal Version
        progress = int(50*current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
        sys.stdout.flush()
        """

    def update_download_info(self, url, number, length):
        self.download_info.setText("Currently working on: " + f"[{url}]" + str(number) + "/" + str(length))

        """ Terminal Version
        print(url)
        print("Currently working on: " + str(number) + "/" + str(length))
        """    

    def on_finished(self, start_time):
        
        """Terminal Version
        delta_time = time.time() - start_time
        delta_time_formated = time.strftime("%H:%M:%S", time.gmtime(delta_time))
        print(f"Download finished in {delta_time_formated}!")
        """
    
    def downloadVideo(self, links: list, video_paths: str, video_savenames: str, save_directory: str, startpoint: int = 0, playlist_lenght: int = 1):
        list_number = startpoint
        list_itemcounter = 0
        for x in range(startpoint ,playlist_lenght):
            list_number += 1
            self.update_download_info(links[x], list_number, len(links))
            #try downloading until it works (to catch some occurring connection errors)
            while True:
                try:
                    video = YouTube(links[x], on_progress_callback=self.progress_function)
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
                    self.logger.warning(f"YTCS - downloadVideo : Video [{links[x]}] is regional unavailable")
                    self.callback("video unavailable") #occurs only when regional unavailable?
                    self.warning_count += 1
                    return
                    break
                except Exception as e:
                    self.logger.error(f"YTCS - downloadVideo : {e}")
                    self.error_count += 1
                    continue
                break
            list_itemcounter += 1
        return video_paths, video_savenames

    def convertVideo(self, paths: list, titles: list, save_directory:str, startpoint: int = 0, playlist_length: int = 1):
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
                    mp4_vid.audio.write_audiofile(os.path.join(save_directory, save_video_title + ".mp3"))
                    mp4_vid.close()
            list_itemcounter += 1

    def deleteMP4(self, del_directory):
        for file in glob.glob(os.path.join(del_directory, "*.mp4")):
            while True:
                try:
                    os.remove(file)
                    break
                except Exception as e:
                    self.logger.warning(f"YTCS - deleteMP4 : {file} could not be deleted")
                    self.logger.error(f"YTCS - deleteMP4 : {e}")
                    self.error_count += 1
                    self.not_deleted_files += 1
                    pass

    def download_url(self, url, dir, download_video, download_audio, flag, first_video):
        video_paths = []
        video_savenames = []
        video_urls = []
        start_time = time.time()

        #case: is video
        if flag == "video":
            #get video title
            video = YouTube(url)
            video_title = safe_filename(video.title)
            #creat folder for video
            video_folder_directory = dir + "/" + video_title
            hell.create_dir(video_folder_directory)
            if download_video:
                #create video directory
                video_directory = video_folder_directory + "/" + video_title + "(Video)" + "/"
                hell.create_dir(video_directory)
            if download_audio:
                #create audio directory
                audio_directory = video_folder_directory + "/" + video_title + "(Audio)" + "/"
                hell.create_dir(audio_directory)
            video_urls.append(url)
            if download_video and download_audio:
                video_paths, video_savenames = self.downloadVideo(video_urls, video_paths, video_savenames, video_directory)
                self.convertVideo(video_paths, video_savenames, audio_directory)
            elif download_video:
                video_paths, video_savenames = self.downloadVideo(video_urls, video_paths, video_savenames, video_directory)
            elif download_audio:
                video_paths, video_savenames = self.downloadVideo(video_urls, video_paths, video_savenames, audio_directory)
                self.convertVideo(video_paths, video_savenames, audio_directory)
                self.deleteMP4(audio_directory)

        #case: is playlist
        elif flag == "playlist":
            #get playlist title
            playlist = Playlist(url)
            try:
                playlist_title = playlist.title
            except:
                self.callback("no access to playlist")
                return
            #create playlist directory
            playlist_directory = dir + "/" + playlist_title
            hell.create_dir(playlist_directory)
            if download_video:
                #create video directory
                video_directory = playlist_directory + "/" + playlist_title + " (Video)" + "/"
                hell.create_dir(video_directory)
            if download_audio:
                #create audio directory
                audio_directory = playlist_directory + "/" + playlist_title + " (Audio)" + "/"
                hell.create_dir(audio_directory)
            try:
                playlist_itemcount = playlist.length
                #gives error if playlist has only one video
            except:
                playlist_itemcount = 1
            video_urls = playlist.video_urls
            if download_video and download_audio:
                video_paths, video_savenames = self.downloadVideo(video_urls, video_paths, video_savenames, video_directory, first_video, playlist_itemcount)
                self.convertVideo(video_paths, video_savenames, audio_directory, first_video, playlist_itemcount)
            elif download_video:
                video_paths, video_savenames = self.downloadVideo(video_urls, video_paths, video_savenames, video_directory, first_video, playlist_itemcount)
            elif download_audio:
                video_paths, video_savenames = self.downloadVideo(video_urls, video_paths, video_savenames, audio_directory, first_video, playlist_itemcount)
                self.convertVideo(video_paths, video_savenames, audio_directory, first_video, playlist_itemcount)
                self.deleteMP4(audio_directory)

        else:
            self.logger.warning(f"YTCS - download_url : {url} was not a downloadable source")
            self.callback("url error")
            return

        self.on_finished(start_time)
        self.callback("finished", start_time, self.warning_count, self.error_count, self.not_deleted_files)
        
def check_url(url):
    #check if url is video or playlist
    if "playlist" in url:
        return "playlist"
    elif "watch" in url and "list" in url:
        return "playlist-video"
    elif "watch" in url and not "list" in url:
        return "video"
    else:
        return False