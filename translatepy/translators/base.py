from abc import ABC, abstractmethod, abstractproperty

import Levenshtein

from translatepy.utils.utils import get_key
from translatepy.exceptions import TranslationError, UnknownLanguage

from ..models import Translation, LanguageSearch, Language


class BaseTranslator(ABC):
    """
    Base abstract class for a translator
    """

    def translate(
        self, text: str, destination_language: str, source_language: str = "auto"
    ) -> Translation:
        """
        Translates text from a given language to another specific language.

        Parameters
        ----------
        text: str
            The text to be translated.
        destination_language: str or `Language`
            If str it expects the language code that the `text` should be translated to. Use `.supported_languages`
            to check the list of languages that a `Translator` supports, and use `.get_language` to
            search for a language of the `Translator`, and find it's code.
        source_language: str or `Language`, optional, default='auto'
            If str it expects the code of the language that the `text` is written in. When using the default value (`auto`),
            the `Translator` will try to find the language automatically.

        Returns
        -------
        Translation
            A `Translation` object with the results of the translation.

        """

        # Validate the languages
        # We save the values in new variables, so at the end
        # of this method, we still have acess to the original codes.
        # With this we can use the original codes to build the response,
        # this makes the code transformation transparent to the user.
        dest_code = self._validate_and_fix_lang(destination_language)
        source_code = self._validate_and_fix_lang(source_language)

        try:
            # Call the private concrete implementation of the Translator to get the translation
            translation = self._translate(
                text,
                dest_code,
                source_code,
            )
            # Return a `Translation` object
            return Translation(
                translator=str(self),
                source_language=source_language,
                destination_language=destination_language,
                translation=translation,
            )

        except Exception as exc:
            raise TranslationError from exc

    @abstractmethod
    def _translate(
        self, text: str, destination_language: str, source_language: str
    ) -> str:
        """
        Private method that concrete Translators must implement to hold the concrete
        logic for the translations. Receives the validated parameters and must
        return a translation (str).
        """

    def __str__(self) -> str:
        """
        String representation of a translator.
        Returns the class name without 'Translator'
        """
        class_name = self.__class__.__name__.split("Translator")[0]
        return "Translator" if class_name == "" else class_name

    @property
    def _codes(self):
        """
        Property that returns a `dict` containing all the possible languages.
        The values are the language name, and the keys are the language code.
        """
        return {
            "automatic": "auto",
            "afrikaans": "af",
            "albanian": "sq",
            "amharic": "am",
            "arabic": "ar",
            "armenian": "hy",
            "azerbaijani": "az",
            "basque": "eu",
            "belarusian": "be",
            "bengali": "bn",
            "bosnian": "bs",
            "bulgarian": "bg",
            "catalan": "ca",
            "cebuano": "ceb",
            "chichewa": "ny",
            "chinese": "zh-CN",
            "chinese (simplified)": "zh-CN",
            "chinese (traditional)": "zh-TW",
            "corsican": "co",
            "croatian": "hr",
            "czech": "cs",
            "danish": "da",
            "dutch": "nl",
            "english": "en",
            "esperanto": "eo",
            "estonian": "et",
            "filipino": "tl",
            "finnish": "fi",
            "french": "fr",
            "frisian": "fy",
            "galician": "gl",
            "georgian": "ka",
            "german": "de",
            "greek": "el",
            "gujarati": "gu",
            "haitian": "ht",
            "creole": "ht",
            "haitian creole": "ht",
            "hausa": "ha",
            "hawaiian": "haw",
            "hebrew": "iw",
            "hindi": "hi",
            "hmong": "hmn",
            "hungarian": "hu",
            "icelandic": "is",
            "igbo": "ig",
            "indonesian": "id",
            "irish": "ga",
            "italian": "it",
            "japanese": "ja",
            "javanese": "jw",
            "kannada": "kn",
            "kazakh": "kk",
            "khmer": "km",
            "korean": "ko",
            "kurdish": "ku",
            "kurdish (kurmanji)": "ku",
            "kyrgyz": "ky",
            "lao": "lo",
            "latin": "la",
            "latvian": "lv",
            "lithuanian": "lt",
            "luxembourgish": "lb",
            "macedonian": "mk",
            "malagasy": "mg",
            "malay": "ms",
            "malayalam": "ml",
            "maltese": "mt",
            "maori": "mi",
            "marathi": "mr",
            "mongolian": "mn",
            "myanmar": "my",
            "burmese": "my",
            "myanmar (burmese)": "my",
            "nepali": "ne",
            "norwegian": "no",
            "odia": "or",
            "pashto": "ps",
            "persian": "fa",
            "polish": "pl",
            "portuguese": "pt",
            "punjabi": "pa",
            "romanian": "ro",
            "russian": "ru",
            "samoan": "sm",
            "scots": "gd",
            "gaelic": "gd",
            "scots gaelic": "gd",
            "serbian": "sr",
            "sesotho": "st",
            "shona": "sn",
            "sindhi": "sd",
            "sinhala": "si",
            "slovak": "sk",
            "slovenian": "sl",
            "somali": "so",
            "spanish": "es",
            "sundanese": "su",
            "swahili": "sw",
            "swedish": "sv",
            "tajik": "tg",
            "tamil": "ta",
            "telugu": "te",
            "thai": "th",
            "turkish": "tr",
            "ukrainian": "uk",
            "urdu": "ur",
            "uyghur": "ug",
            "uzbek": "uz",
            "vietnamese": "vi",
            "welsh": "cy",
            "xhosa": "xh",
            "yiddish": "yi",
            "yoruba": "yo",
            "zulu": "zu",
        }

    @abstractproperty
    def supported_languages(self) -> list[str]:
        """
        Abstract property that returns a list of language
        names that the `Translator` supports.

        Defaults to all the languages.
        """
        return self._codes.keys()

    def get_language(self, language: str) -> LanguageSearch:
        """
        Given a `language` name searches for the most similar
        language of the **supported languages**, of the concrete `Translator`.

        Uses the `Levenshtein` distance for finding the closest match.

        Parameters
        ----------
        language: str
            The language name.

        Returns
        -------
        LanguageSearch
            A `LanguageSearch` object populated with the closest match.
        """
        # First check if already a language code (instead of a name)
        if language in self._codes.values():
            return language

        # Otherwise find the languag with highest Levenshein similarity ratio,
        # inside the Translator supported languages
        matching_key = max(
            self.supported_languages, key=lambda k: Levenshtein.ratio(language, k)
        )
        # Return a Language object
        return LanguageSearch(
            input=language,
            name=matching_key,
            code=self._codes[matching_key],
            similarity=round(Levenshtein.ratio(language, matching_key), 2),
        )

    def _validate_and_fix_lang(self, language) -> str:

        # First check if `lang`
        # is instance of `Language`
        if isinstance(language, Language):
            # If so extract the real language code
            language = language.code

        # Then check if languages codes are valid codes
        if not language in self._codes.values():
            raise UnknownLanguage(f"Unknown language code '{language}'")

        # Then check if languages codes correspond
        # to valid supported languages of translator

        # 1. Get the name of language corresponding to the code
        lang_name = get_key(self._codes, language)

        # 2. Check if the name is in supported languages, except 'auto'
        if not lang_name in self.supported_languages and language != "auto":
            # Check if we are dealing with `source_language`, and
            # it's value is 'auto'. In this case we allow it
            raise UnknownLanguage(
                f"The language code '{language}' does not match with any supported language of the {str(self)} Translator. Please check supported languages with `.supported_languages`."
            )

        # Now we check if must apply language patching.
        # This means transforming the language codes
        # so they are compatible with the API that the
        # concrete Translator uses
        fixing_method = getattr(self, "_language_fixes", None)
        return fixing_method(language) if fixing_method else language
