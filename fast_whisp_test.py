from faster_whisper import WhisperModel
import threading
import logging


logger = logging.getLogger(__name__) 


class WhisperProcessor:
    def __init__(self):
        self.model = None
        self._lock = threading.Lock()
    
    def load_model(self):
        with self._lock:
            if self.model is None:
                logger.info("🔄 Загрузка модели Whisper...")
                self.model = WhisperModel(
                   'medium',
                    device="cpu", 
                    compute_type="int8", 
                    cpu_threads=4,
                    download_root='/app/whisper_models'
                )
                logger.info("✅ Модель загружена!")
            else:
                logger.info("Mодель уже загружена!")
        
    def transcribe(self, file_id):
        try:
            if self.model is None:
                self.load_model()
            
            logger.info(f"🔊 Начинаю расшифровку {file_id}...")
            
            segments, info = self.model.transcribe(
                f"voices/{file_id}.ogg",
                beam_size=5,
                language='ru',
                vad_filter=True
            )
            
            chunks = []
            for segment in segments:
                logger.debug(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
                chunks.append(segment.text)

            logger.info(f'successfully transcribed {file_id}')            
            return chunks

        except Exception as e:
            return [f'an error occured: {e}']

processor = WhisperProcessor()