from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from ytmusicapi import YTMusic
import yt_dlp
import os

app = FastAPI()

# Initialize YTMusic
ytmusic = YTMusic()

# Endpoint to fetch the song
@app.get("/get_song/")
async def get_song(song_name: str):

    search_query = song_name
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
    audio_file="temp_song.mp3"
    if os.path.exists("temp_song.mp3"):
        return FileResponse(audio_file, media_type="audio/mpeg", filename=audio_file)
    else:
        raise HTTPException(status_code=500, detail="Failed to download song")

    # Cleanup: Remove the downloaded file
    @app.on_event("shutdown")
    def cleanup_temp_files():
        if os.path.exists(audio_file):
            os.remove(audio_file)
