import json
import wave

from io import BytesIO


from vosk import Model, KaldiRecognizer

from .base import ABCSpeechRecognizer


class VoskSpeechRecognizer(ABCSpeechRecognizer):

    _model: Model
    _chuncked: bool

    __chunck_size: int = 4096

    def __init__(self, *, path_to_model: str, chuncked: bool = True) -> None:
        """
        Распознавание речи на модели `Vosk`.

        chuncked -- Нужен для работы с большими аудиофайлами,
        что бы часовой аудиофайл грузился не сразу в ОЗУ, а читался частями.
        Размер частей можно указать через свойство `chnuk_size`

        :param path_to_model: Путь к папке модели
        :param chuncked: Для работы с большими аудиофайлами
        """

        self._model = Model(path_to_model)
        self._chuncked = chuncked

    @property
    def chunck_size(self) -> int:
        return self.__chunck_size

    @chunck_size.setter
    def chunck_size(self, value: int) -> None:
        self.__chunck_size = value

    @staticmethod
    def _chuncked_recognize(recognizer: KaldiRecognizer, audio: wave.Wave_read, chunck_size: int) -> str:
        result = ''

        while True:
            data = audio.readframes(chunck_size)

            if len(data) == 0:
                break

            if not recognizer.AcceptWaveform(data):
                continue

            d_res = json.loads(recognizer.Result())
            result += d_res.get('text', '') + ' '

        result += json.loads(recognizer.Result()).get('text', '')
        return result.strip()

    @staticmethod
    def _fulldata_recognize(recognizer: KaldiRecognizer, audio: wave.Wave_read) -> str:
        data = audio.readframes(audio.getnframes())
        recognizer.AcceptWaveform(data)
        result = json.loads(recognizer.FinalResult()).get('text', '')
        return result.strip()

    def recognize(self, bytes_audio: BytesIO) -> str:
        """
        :param bytes_audio: wav аудио в BytesIO
        :return: Текст
        """
        audio = wave.open(bytes_audio, 'rb')
        recognizer = KaldiRecognizer(self._model, audio.getframerate())

        if not self._chuncked:
            return self._fulldata_recognize(recognizer, audio)
        return self._chuncked_recognize(recognizer, audio, self.__chunck_size)
