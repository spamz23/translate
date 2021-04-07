import requests
from .base import BaseTranslator


class BingTranslator(BaseTranslator):
    """
    Microsoft Bing Translation's APIs Implementation
    """

    @property
    def supported_languages(self) -> list[str]:
        """
        Bing supports all the languages.
        Call the parent method
        """
        return super().supported_languages

    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:

        # Make API request
        response = requests.post(
            "https://www.bing.com/ttranslatev3",
            headers={
                "Host": "www.bing.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Referer": "https://www.bing.com/",
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
            },
            params={
                "IG": "839D27F8277F4AA3B0EDB83C255D0D70",
                "IID": "translator.5033.3",
            },
            data={
                "text": str(text),
                "fromLang": source_language,
                "to": destination_language,
            },
        )
        # Raise error if not successful
        response.raise_for_status()
        # Extract the translation
        translation = response.json()[0]["translations"][0]["text"]
        # Return the translation
        return translation

    def _language_fixes(self, language: str) -> str:
        """
        Language fixes for Bing's Translator.
        """
        # If 'auto' change to 'auto-detect'
        if language == "auto":
            return "auto-detect"
        return language
