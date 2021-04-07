from .base import BaseTranslator
from .google import GoogleTranslator, GoogleV2Translator
from .bing import BingTranslator
from .deepl import DeepLTranslator
from .reverso import ReversoTranslator
from .yandex import YandexTranslator


class Translator(BaseTranslator):
    """
    A grouped Translator
    """

    @property
    def supported_languages(self) -> list[str]:
        """
        Translator supports all the languages.
        """
        return super().supported_languages

    def __init__(
        self,
        translators: list[BaseTranslator] = [
            GoogleTranslator,
            GoogleV2Translator,
            BingTranslator,
            DeepLTranslator,
            ReversoTranslator,
            # YandexTranslator,
        ],
    ) -> None:
        """
        Initializes a generic `Translator`.

        Parameters
        ----------
        translators: list of Translators
            A list of Translators classes to sequentially try to execute (stops on the first sucess)
        """
        self.translators = translators

    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:
        # Iterate over each translator to try to translate
        for translator_class in self.translators:
            try:
                # Intantiate translator, and try to translate
                return translator_class()._translate(
                    text, destination_language, source_language
                )
            except Exception:
                # If an error ocurred, move to the next translator
                continue