import assemblyai as aai

def transcribe_video(video_path):
    aai.settings.api_key = "/"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_path)
    return transcript.export_subtitles_srt()
