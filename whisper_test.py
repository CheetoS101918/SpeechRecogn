import whisper

# Правильный код для вашего бота:
model = whisper.load_model("small")  
result = model.transcribe("voices/input.ogg", language="ru")
print(result['text'])



