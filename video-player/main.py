from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile
import os

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
    
    return {"message": "Video uploaded successfully"}

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