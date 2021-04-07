"""
Module containing various models for holding informations.
"""


class Translation:
    """
    Class that holds the result of a Translation.
    """

    def __init__(self, translator, source_language, destination_language, translation):
        self.translator = str(translator)
        self.source_language = source_language
        self.destination_language = destination_language
        self.translation = translation

    def __str__(self) -> str:
        return str(self.__dict__)


class Language:
    """
    Class that holds information about a Language.
    """

    def __init__(self, name: str, code: str) -> None:
        self.name = name
        self.code = code

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return self.__str__()


class LanguageSearch:
    """
    Class that holds the result of a Language search.

    Contains 4 elements:
        - `input`: The original text query.
        - `language`: The found `Language`.
        - `similarity`: Level of similarity between `input` and `language.name`.
    """

    def __init__(
        self,
        input: str,
        name: str,
        code: str,
        similarity: float,
    ) -> None:
        self.input = input
        self.language = Language(name, code)
        self.similarity = similarity

    def __str__(self) -> str:
        return str(self.__dict__)