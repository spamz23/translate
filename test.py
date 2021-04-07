from translatepy.translators import *
from translatepy.models import Translation


def test_translators_translation():
    """
    Tests that all `Translators` are correctly translating.
    """
    translators = [
        BingTranslator,
        DeepLTranslator,
        GoogleTranslator,
        GoogleV2Translator,
        ReversoTranslator,
        Translator,
        # YandexTranslator,
    ]

    for translator_class in translators:
        # Test every translator
        # Create a sample string (portuguese)
        sample_str = "Olá! Hoje está um belo dia para passear."

        # Intantiate the translator
        translator = translator_class()
        # Try every language supported in the translator
        for lang in translator.supported_languages:
            print(f"Trying translator {str(translator)} - lang {lang}")

            result = translator.translate(
                text=sample_str,
                destination_language=translator.get_language(lang).language.code,
            )

            # Check that result is a `Translation`
            assert isinstance(result, Translation)

            # Check if source language was correctly identified
            assert result.source_language == "pt"

            # Check that destination language is correct
            assert result.destination_language == lang


test_translators_translation()