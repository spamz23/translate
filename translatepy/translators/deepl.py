from time import time
import requests

from .base import BaseTranslator, Translation


class DeepLTranslator(BaseTranslator):
    """
    A DeepL API Implementation
    """

    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:

        # Prepare the API payload
        payload = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": [
                    {
                        "kind": "default",
                        "raw_en_sentence": str(text),
                        "raw_en_context_before": [],
                        "raw_en_context_after": [],
                        "preferred_num_beams": 4,
                        "quality": "fast",
                    }
                ],
                "lang": {
                    "user_preferred_langs": ["JA", "FR", "EN"],
                    "source_lang_user_selected": str(source_language),
                    "target_lang": str(destination_language),
                },
                "priority": -1,
                "commonJobParams": {},
                "timestamp": int(time()),
            },
            "id": 63710028,
        }
        # Make the API request
        response = requests.post(
            "https://www2.deepl.com/jsonrpc",
            json=payload,
        )

        # Raise error if not sucess
        response.raise_for_status()

        # Extract the translation
        translation = response.json()["result"]["translations"][0]["beams"][0][
            "postprocessed_sentence"
        ]

        # Return the translation
        return translation

    @property
    def supported_languages(self) -> list[str]:
        """
        Property that returns a list of DeepL's
        supported languages.
        """
        return [
            "bulgarian",
            "chinese",
            "czech",
            "danish",
            "dutch",
            "english",
            "estonian",
            "finnish",
            "french",
            "german",
            "greek",
            "hungarian",
            "italian",
            "japanese",
            "latvian",
            "lithuanian",
            "polish",
            "portuguese",
            "romanian",
            "russian",
            "slovak",
            "slovenian",
            "spanish",
            "swedish",
        ]

    def _language_fixes(self, language: str) -> str:
        """
        Language fixes for DeepL's Translator.
        """
        # If 'auto' return the same
        if language == "auto":
            return language

        # DeepL uses a uppercase version
        # of the ISO-639-1 codes
        # https://www.deepl.com/docs-api/translating-text/
        return language.upper()