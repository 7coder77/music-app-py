from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from ytmusicapi import YTMusic
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

# Initialize YTMusic
ytmusic = YTMusic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

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

@app.get("/get_songId/{id}")
async def get_song_by_id(id: str):
    print("song requested for",id)
    video_id = id
    audio_file = f"temp_song_{video_id}.mp3"  # Unique filename

    # yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": audio_file,
        "quiet": True,
    }

    # Download the audio
    try:
        print("test")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        
        print(f"Song downloaded: {audio_file}")

        # Return file response & schedule deletion after response is sent
        return FileResponse(audio_file, media_type="audio/mpeg", filename=audio_file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download song: {str(e)}")

@app.get("/search_song/")
async def search_song(query: str):
    """Search for a song on YouTube Music and return top results."""
    
    try:
        search_results = ytmusic.search(query, filter="songs")  # Search for songs

        if not search_results:
            raise HTTPException(status_code=404, detail="No songs found.")

        # Extract required details from the results
        results = [
            {
                "title": song["title"],
                "artist": song["artists"][0]["name"] if "artists" in song else "Unknown",
                "videoId": song["videoId"],
                "duration": song.get("duration", "Unknown"),
                "thumbnail": song["thumbnails"][-1]["url"] if "thumbnails" in song else None,
            }
            for song in search_results[:10]  # Return top 10 results
        ]

        return search_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching songs: {str(e)}")

def delete_file(file_path):
    """Delete file after response is sent."""
    def delete():
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {e}")

    return delete
