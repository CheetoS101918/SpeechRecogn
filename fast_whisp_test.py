from faster_whisper import WhisperModel
import threading


class WhisperProcessor:
    def __init__(self):
        self.model = None
        self._lock = threading.Lock()
    
    def load_model(self):
        with self._lock:
            if self.model is None:
                print("🔄 Загрузка модели Whisper...")
                self.model = WhisperModel(
    #                    "large-v3", 
                   'medium',
                    device="cpu", 
                    compute_type="int8", 
                    cpu_threads=8
                )
                print("✅ Модель загружена!")
            else:
                print("модель уже загружена!")
        
    def transcribe(self, file_id):
        """Транскрибация с уже загруженной моделью"""
        if self.model is None:
            self.load_model()
        
        print(f"🔊 Начинаю расшифровку {file_id}...")
        
        segments, info = self.model.transcribe(
            f"voices/{file_id}.ogg",
            beam_size=5,
            language='ru',
            vad_filter=True
        )
        
        chunks = []
        try:
            for segment in segments:
                print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
                chunks.append(segment.text)
            return chunks
        except Exception as e:
            return [f'an error occured: {e}']


# Создаём глобальный экземпляр
processor = WhisperProcessor()