from io import BytesIO

from pydub import AudioSegment


def normalize_audio(_bytes: BytesIO, channels: int = 1, frame_rate: int = 16_000) -> BytesIO:
    """
    Нормализует аудио для модели.
    Большинство моделей требуют что бы аудио было в моно и 16 kHz

    - `audio.set_channels(1)` -- делает моно, т.е 1 канал
    - `audio.set_frame_rate(16000)` -- приводит к 16 kHz

    :param _bytes: аудио в любом формате в байтах
    :type _bytes: BytesIO
    :param channels: Количество каналов
    :type channels: int
    :param frame_rate: Герцовка
    :type frame_rate: int
    :return: Аудио в байтах в wav формате
    :rtype: BytesIO
    """

    export = BytesIO()

    audio = AudioSegment.from_file(_bytes)
    audio = audio.set_channels(channels)
    audio = audio.set_frame_rate(frame_rate)
    audio.export(export, format='wav')
    export.seek(0)

    return export