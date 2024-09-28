from abc import ABC, abstractmethod
from io import BytesIO


class ABCSpeechRecognizer(ABC):

    @abstractmethod
    def recognize(self, bytes_audio: BytesIO) -> str:
        ...
