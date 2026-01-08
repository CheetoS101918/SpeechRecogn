from faster_whisper import WhisperModel


def faster_transcribe():
    # compute_type="int8" — магия оптимизации (сжимает модель, чтобы работала быстрее на CPU)
    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=2)

    print("Загрузка модели завершена. Начинаю расшифровку...")

    # beam_size=5 — стандарт для хорошего качества
    segments, info = model.transcribe("voices/AwACAgIAAxkBAAICrWleLTYbIhPRyPTnJwFdhBonrjQeAAI8hgACuhDZSiE7AQ3JVbldOAQ.ogg",
        beam_size=5,
        language='ru'
        )

    # Результат выдается сегментами (частями)
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

faster_transcribe()