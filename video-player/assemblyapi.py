import assemblyai as aai

def transcribe_video(video_path):
    aai.settings.api_key = "0d4e9fc7fc6f48c9b366b5382ef285fd"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_path)
    return transcript.export_subtitles_srt()
