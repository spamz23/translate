import requests

from .base import BaseTranslator, Translation


class BaseGoogleTranslator(BaseTranslator):
    """
    Base abstract Google Translator
    """

    @property
    def supported_languages(self):
        return super().supported_languages


class GoogleTranslator(BaseGoogleTranslator):
    """
    Google Translation Implementation
    """

    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:

        # Make API requests
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl="
            + str(source_language)
            + "&tl="
            + str(destination_language)
            + "&q="
            + text
        )
        # Raise error if not sucess
        response.raise_for_status()
        # Extract translation
        translation = "".join([sentence[0] for sentence in response.json()[0]])
        # Return the translation
        return translation


class GoogleV2Translator(BaseGoogleTranslator):
    """
    Alternative Google Translation Implementation.
    This translator uses a different Google API endpoint.
    """

    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:
        # Make API request
        response = requests.get(
            "https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl="
            + str(source_language)
            + "&tl="
            + str(destination_language)
            + "&q="
            + text,
        )
        # Raise error if not sucess
        response.raise_for_status()
        # Extract translation
        translation = "".join(
            (sentence["trans"] if "trans" in sentence else "")
            for sentence in response.json()["sentences"]
        )
        # Return the translation
        return translation
