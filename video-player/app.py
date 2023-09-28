# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from fastapi import File, UploadFile

# @app.post("/upload/")
# async def upload_video(file: UploadFile):
#     # Save the uploaded video file to a directory on the server.
#     with open(file.filename, "wb") as video_file:
#         video_file.write(file.file.read())
#     return {"message": "Video uploaded successfully"}

# @app.get("/playback/{video_filename}", response_class=HTMLResponse)
# async def render_video_player(video_filename: str):
#     # Generate the URL for the uploaded video file.
#     video_url = f"/path/to/uploaded/videos/{video_filename}"
    
#     # Render the HTML page with the video player.
#     with open("video_player.html", "r") as html_file:
#         template = html_file.read()
#         rendered_template = template.replace("{{ video_url }}", video_url)
#         return rendered_template
