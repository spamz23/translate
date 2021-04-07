from translatepy.translators.yandex import YandexTranslator
from translatepy.translators import (
    GoogleV2Translator,
    GoogleTranslator,
    BingTranslator,
    ReversoTranslator,
    Translator,
    DeepLTranslator,
)
from translatepy.models import Translation


t = BingTranslator()
print(t.get_language("Fren"))
print(
    t.translate(
        "Olá bom dia. Tudo bem com o senhor? Hoje vou até a uma loja nova.",
        destination_language=t.get_language("Fren").language,
    )
)
