import requests
import random
from time import time

from .base import BaseTranslator


class YandexTranslator(BaseTranslator):
    """
    Yandex Translator
    """

    pass

    # def __init__(self) -> None:
    #     super().__init__()
    #     self._base_url = "https://translate.yandex.net/api/v1/tr.json/"

    # def refreshSID(self) -> bool:
    #     """
    #     Refreshes the SID used for requests to Yandex Translation API

    #     See issue #4 for more information
    #     Randomness is used to prevent bot detection
    #     Args:
    #     Returns:
    #         Bool --> wether it succeded or not
    #     """
    #     try:
    #         if (
    #             time() - self._last_tried > self._check_increment
    #         ):  # if the duration between the last time we tried to get the SID and now is greater than 10 minutes for the first pass
    #             data = requests.get(
    #                 "https://translate.yandex.com/", headers=self._headers
    #             ).text
    #             sid_position = data.find("Ya.reqid = '")
    #             if sid_position != -1:
    #                 data = data[sid_position + 12 :]
    #                 self._sid = data[: data.find("';")]
    #                 self._sid_cache.write(self._sid)

    #                 self._check_increment = (
    #                     self._check_increment / 2 + random.randint(0, 1000) / 1000
    #                 )  # decrementing because it might work decremented
    #                 self._last_tried = time()  # maybe keep that in a file
    #                 self._last_tried_cache.write(self._last_tried)
    #                 return True
    #             else:
    #                 self._check_increment = (
    #                     self._check_increment * 2 + random.randint(0, 1000) / 1000
    #                 )  # incrementing the waiting time
    #                 self._last_tried = time()  # maybe keep that in a file
    #                 self._last_tried_cache.write(self._last_tried)
    #         # else
    #         # do nothing as we know that yandex will rate-limit us if we ping them too much
    #         return False
    #     except:
    #         return False

    # @property
    # def supported_languages(self) -> list[str]:
    #     """
    #     Yandex supports all the languages
    #     """
    #     return super().supported_languages

    # def _translate(
    #     self,
    #     text: str,
    #     destination_language: str,
    #     source_language: str,
    # ) -> str:
    #     # Make API request
    #     url = (
    #         self._base_url
    #         + "translate?id="
    #         + self._sid
    #         + "-0-0&srv=tr-text&lang="
    #         + str(source_language)
    #         + "-"
    #         + str(destination_language)
    #         + "&reason=auto&format=text"
    #     )

    #     response = requests.get(
    #         url,
    #         data={
    #             "text": text,
    #         },
    #     )
    #     # Raise error if not sucess
    #     response.raise_for_status()

    #     # Extract translation
    #     translation = response.json()["text"][0]

    #     return translation