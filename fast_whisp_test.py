from faster_whisper import WhisperModel
import threading

# def faster_transcribe(file_id):
#     # compute_type="int8" — магия оптимизации (сжимает модель, чтобы работала быстрее на CPU)
#     model_size = "large-v3"
#     model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=2)

#     print("Загрузка модели завершена. Начинаю расшифровку...")

#     # beam_size=5 — стандарт для хорошего качества
#     segments, info = model.transcribe(f"voices/{file_id}.ogg",
#         beam_size=5,
#         language='ru'
#         )

#     chunks = []

#     # Результат выдается сегментами (частями)
#     for segment in segments:
#         print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
#         chunks.append(segment.text)
    
#     return chunks



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
                    cpu_threads=3
                )
                print("✅ Модель загружена!")
        
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
        for segment in segments:
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
            chunks.append(segment.text)
        
        return chunks


# Создаём глобальный экземпляр
processor = WhisperProcessor()