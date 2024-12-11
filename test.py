import os
import pygame
from ytmusicapi import YTMusic
import yt_dlp

ytmusic = YTMusic()

search_query = input("Enter song name:-")
search_results = ytmusic.search(search_query, filter="songs")
if not search_results:
    print("Song not found!")
    exit()

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

audio_file = "temp_song.mp3"
with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': audio_file}) as ydl:
    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
print("song added with name 'temp_song.mp3'")
