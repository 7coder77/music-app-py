import os
import pygame
from ytmusicapi import YTMusic
import yt_dlp
# from playsound import playsound

# Initialize YTMusic
ytmusic = YTMusic()

# Search for a song
search_query = input("Enter song name:-")
search_results = ytmusic.search(search_query, filter="songs")
if not search_results:
    print("Song not found!")
    exit()

# Get the song details
song = search_results[0]
title = song["title"]
video_id = song["videoId"]

print(f"Fetching: {title}")

# Use yt-dlp to download or fetch the audio URL
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'temp_song.%(ext)s',  # Save file as temp_song.<ext>
    'quiet': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
    audio_url = info['url']

# Download the file locally (required for pygame)
audio_file = "temp_song.mp3"
with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': audio_file}) as ydl:
    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

# Initialize pygame and play the audio
pygame.mixer.init()

try:
    # playsound("temp_song.mp3")
    # pygame.mixer.music.load(audio_file)
    print(f"Playing: {title}")
    # pygame.mixer.music.play()

    # Wait until the music finishes
    # while pygame.mixer.music.get_busy():
        # pass
finally:
    # Cleanup: Remove the temporary audio file
    # if os.path.exists(audio_file):
    #     os.remove(audio_file)
    print("Playback finished.")
