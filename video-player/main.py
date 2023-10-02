from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from assemblyapi import transcribe_video
import os

# Import the transcribe_video function from transcribe-video.py


app = FastAPI()

@app.post("/upload/")
async def upload_video(file: UploadFile):
    # Define the path to the "videos" folder
    videos_folder = os.path.join("videos")

    # Ensure the "videos" folder exists; create it if it doesn't.
    os.makedirs(videos_folder, exist_ok=True)

    # Save the uploaded video file to the "videos" folder.
    video_path = os.path.join(videos_folder, file.filename)
    with open(video_path, "wb") as video_file:
        video_file.write(file.file.read())

    # Transcribe the uploaded video and save the transcript as an SRT file
    transcript_srt = transcribe_video(video_path)
    transcript_filename = os.path.splitext(file.filename)[0] + ".srt"
    transcript_path = os.path.join(videos_folder, transcript_filename)
    with open(transcript_path, "w") as transcript_file:
        transcript_file.write(transcript_srt)

    return {"message": "Video uploaded and transcribed successfully"}

@app.get("/playback/{video_filename}", response_class=HTMLResponse)
async def render_video_player(video_filename: str, request: Request):
    base_url = request.base_url
    video_url = f"{base_url}videos/{video_filename}"  # Updated URL path

    # Render the HTML page with the video player.
    with open("../index.html", "r") as html_file:
        template = html_file.read()
        rendered_template = template.replace("{{ video_url }}", video_url)
        return rendered_template

@app.get("/videos/", response_class=HTMLResponse)
async def list_videos(request: Request):
    # Define the path to the "videos" folder
    videos_folder = os.path.join("videos")

    # List all video files in the "videos" folder
    video_files = os.listdir(videos_folder)

    # Construct video URLs for all video files
    base_url = request.base_url
    video_urls = [f"{base_url}videos/{filename}" for filename in video_files]

    # Render the HTML page with a list of video URLs
    with open("../video_list.html", "r") as html_file:
        template = html_file.read()
        rendered_template = template.replace("{{ video_urls }}", "\n".join(video_urls))
        return rendered_template

@app.delete("/delete_video/{video_filename}")
async def delete_video(video_filename: str):
    # Define the path to the "videos" folder
    videos_folder = os.path.join("videos")

    # Construct the full path to the video file to be deleted
    video_path = os.path.join(videos_folder, video_filename)

    # Check if the video file exists
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    # Delete the video file
    os.remove(video_path)

    return {"message": f"Video '{video_filename}' deleted successfully"}
