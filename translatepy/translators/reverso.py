import requests

from translatepy.translators.base import (
    BaseTranslator,
)
from translatepy.exceptions import TranslationError
from translatepy.models import Language


class ReversoTranslator(BaseTranslator):
    """
    Reverso Translation Implementation
    """

    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:

        # Check if source language is 'auto'
        # If so use the Reverso API to detect the language first
        if source_language == "auto":
            source_language = self.detect_language(text)

        # Make the API request
        response = requests.post(
            "https://api.reverso.net/translate/v1/translation",
            json={
                "format": "text",
                "from": source_language,
                "to": destination_language,
                "input": text,
                "options": {
                    "origin": "reversodesktop",
                    "sentenceSplitter": False,
                    "contextResults": False,
                    "languageDetection": True,
                },
            },
        )
        # Raise error if not sucess
        response.raise_for_status()
        # Extract translation
        translation = response.json()["translation"][0]
        # Return the translation
        return translation

    @property
    def supported_languages(self):
        """
        Property that returns a list of Reverso's
        supported languages.
        """
        return [
            "german",
            "arabic",
            "chinese",
            "spanish",
            "french",
            "hebrew",
            "dutch",
            "english",
            "italian",
            "japanese",
            "polish",
            "portuguese",
            "romanian",
            "russian",
            "turkish",
        ]

    def detect_language(self, text: str) -> Language:
        """
        Gives back the language of the given text
        Args:
          text:
        Returns:
            str --> the language code
            None --> when an error occurs
        """
        try:
            response = requests.post(
                "https://api.reverso.net/translate/v1/translation",
                json={
                    "input": str(text),
                    "from": "eng",
                    "to": "fra",
                    "format": "text",
                    "options": {
                        "origin": "reversodesktop",
                        "sentenceSplitter": False,
                        "contextResults": False,
                        "languageDetection": True,
                    },
                },
            )
            response.raise_for_status()
            detected_language = response.json()["languageDetection"]["detectedLanguage"]
        except Exception as ex:
            raise TranslationError from ex

        return detected_language

    def _language_fixes(self, language: str) -> str:
        """
        Language fixes for Reverso's Translator.
        """
        # If 'auto' return the same
        if language == "auto":
            return language
        # Now check for all the Reverso languages
        # German
        if language == "de":
            return "ger"
        # Arabic
        if language == "ar":
            return "arab"
        # Chinese
        if language == "ch":
            return "chi"
        # Spanish
        if language == "es":
            return "spa"
        # French
        if language == "fr":
            return "fra"
        # Hebrew
        if language == "iw":
            return "heb"
        # Dutch
        if language == "nl":
            return "dut"
        # English
        if language == "en":
            return "eng"
        # Italian
        if language == "it":
            return "ita"
        # Japanase
        if language == "ja":
            return "jpn"
        # Polish
        if language == "pl":
            return "pol"
        # Portuguese
        if language == "pt":
            return "por"
        # Romanian
        if language == "ro":
            return "rum"
        # Russian
        if language == "ru":
            return "rus"
        # Turkish
        if language == "tr":
            return "tur"
        # If got here, raise Error
        raise ValueError(language)