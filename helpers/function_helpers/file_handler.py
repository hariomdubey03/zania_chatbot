from abc import ABC, abstractmethod
import PyPDF2
from io import BytesIO
import json
from typing import Any


# File type checker
class FileTypeChecker:
    def __init__(self, allowed_types=None):
        if allowed_types is None:
            allowed_types = ["application/pdf", "application/json"]
        self.allowed_types = allowed_types

    def check(self, content_type: str):
        if content_type not in self.allowed_types:
            raise ValueError(
                f"File type '{content_type}' is not allowed."
            )
        return content_type


# Interface for extracting text from files
class ContentExtractor(ABC):
    @abstractmethod
    def extract_content(self, file_obj: BytesIO) -> str:
        pass


class JSONContentExtractor(ContentExtractor):
    def extract_content(
        self, file_obj: BytesIO, as_text: bool = True
    ) -> object:
        content = json.dumps(json.load(file_obj))

        return content


class JSONContentExtractorAsObject(ContentExtractor):
    def extract_content(self, file_obj: BytesIO) -> object:
        content = json.load(file_obj)

        return content


# PDF file text extractor
class PDFContentExtractor(ContentExtractor):
    def extract_content(
        self, file_obj: BytesIO, as_text: bool = True
    ) -> str:
        raw_content = ""
        pdf_reader = PyPDF2.PdfReader(file_obj)
        for page in pdf_reader.pages:
            raw_content += page.extract_text()
        return raw_content


class ExtractorFactory:
    def __init__(self, as_text: str = True):
        self.extractors = {
            "application/pdf": PDFContentExtractor,
            "application/json": (
                JSONContentExtractor
                if as_text
                else JSONContentExtractorAsObject
            ),
        }

    def get_content_extractor(self, content_type: str):
        extractor_class = self.extractors.get(content_type)
        if not extractor_class:
            raise ValueError(
                f"File type '{content_type}' is not allowed."
            )
        return extractor_class()


# Main FileHandler class
class FileContentExtractor:
    def __init__(self, factory: ExtractorFactory):
        self.factory = factory

    def process_file(self, file_obj: BytesIO, content_type: str):
        extractor = self.factory.get_content_extractor(
            content_type=content_type
        )
        raw_content = extractor.extract_content(file_obj=file_obj)

        return raw_content


class ConvertFileObject:
    def __init__(self, content: Any) -> None:
        self.content = content

    def to_json_file(self) -> BytesIO:
        json_data = json.dumps(self.content)
        file_obj = BytesIO(json_data.encode("utf-8"))
        return file_obj
