from enum import Enum
from typing import Union, Optional


class SentenceType(Enum):
    # speaking stage
    FIRST = "FIRST"  # first sentence
    MIDDLE = "MIDDLE"  # Talking
    LAST = "LAST"  # last sentence


class ContentType(Enum):
    # Content type
    TEXT = "TEXT"  # text content
    FILE = "FILE"  # File content
    ACTION = "ACTION"  # action content


class InterfaceType(Enum):
    # Interface type
    DUAL_STREAM = "DUAL_STREAM"  # Dual flow
    SINGLE_STREAM = "SINGLE_STREAM"  # single stream
    NON_STREAM = "NON_STREAM"  # non-streaming


class TTSMessageDTO:
    def __init__(
        self,
        sentence_id: str,
        # speaking stage
        sentence_type: SentenceType,
        # Content type
        content_type: ContentType,
        # Content details, usually text or audio lyrics that need to be converted
        content_detail: Optional[str] = None,
        # If the content type is a file, you need to pass in the file path
        content_file: Optional[str] = None,
    ):
        self.sentence_id = sentence_id
        self.sentence_type = sentence_type
        self.content_type = content_type
        self.content_detail = content_detail
        self.content_file = content_file
