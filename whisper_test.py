import whisper


def speech_to_text(file_id):
    model = whisper.load_model("small")  
    result = model.transcribe(f"voices/{file_id}.ogg", language="ru", fp16=False)
    return result['text']




