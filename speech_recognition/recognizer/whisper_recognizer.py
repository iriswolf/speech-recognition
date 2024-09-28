import os
import tempfile

from io import BytesIO
from typing import Literal, Optional

import whisper

from .base import ABCSpeechRecognizer


class WhisperSpeechRecognizer(ABCSpeechRecognizer):

    def __init__(
        self,
        model_name: Literal[
            'tiny',
            'base',
            'small',
            'medium',
            'large'
        ],
        in_memory: bool = False
    ) -> None:
        self._model = whisper.load_model(model_name, in_memory=in_memory)

    def _recognize(self, bytes_audio: BytesIO, whisper_kwargs):
        # Создаем временный WAV-файл для передачи в Whisper
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
            temp_audio_file.write(bytes_audio.read())
            temp_audio_file_path = temp_audio_file.name
        try:
            # Распознаем речь
            result = self._model.transcribe(temp_audio_file_path, **whisper_kwargs)
        finally:
            # Удаляем временный файл
            os.remove(temp_audio_file_path)
        return result.get('text', '').strip()

    def recognize(
        self,
        bytes_audio: BytesIO,
        *,
        lang: str = 'ru',
        whisper_kwargs: Optional[dict] = None
    ) -> str:
        whisper_kwargs = whisper_kwargs or {}
        whisper_kwargs.setdefault('lang', 'ru')

        return self._recognize(bytes_audio, whisper_kwargs)
