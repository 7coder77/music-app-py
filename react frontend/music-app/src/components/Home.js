import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Home({ newData }) {
  const [videos, setVideos] = useState([]);
  const [audioSrc, setAudioSrc] = useState(null);

  // Update videos state whenever newData prop changes
  useEffect(() => {
    console.log(videos);
    if (Array.isArray(newData)) {
      setVideos(newData);
    }
  }, [newData]);

  const renderSong = async (video) => {
    try {
      console.log("Fetching song for video ID:", video.videoId);
      
      const response = await axios.get(`http://127.0.0.1:8000/get_songId/${video.videoId}`, {
        responseType: "blob", // Get the file as a binary blob
      });

      // Create a URL for the received audio file
      const audioUrl = URL.createObjectURL(response.data);
      setAudioSrc(audioUrl);
      
      console.log("Audio ready to play:", audioUrl);
    } catch (error) {
      console.error("Error fetching audio:", error);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="mb-4 text-center">Select a video</h1>
      <div className="row">
        {videos.map((video) => (
          <div
            className="col-md-2 mb-4"
            key={video.id}
            onClick={() => renderSong(video)}
          >
            <div className="card h-100">
              <img
                src={video.thumbnails[1].url}
                className="card-img-top"
                alt={video.title}
              />
              <div className="card-body">
                <h5 className="card-title">{video.name}</h5>
                <p className="card-text">
                  Click below to watch the video or listen to the audio!
                </p>
                <button className="btn btn-primary">Play Audio</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Audio Player */}
      {audioSrc && (
        <div className="mt-4 text-center">
          <h3>Now Playing</h3>
          <audio controls autoPlay>
            <source src={audioSrc} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
}
