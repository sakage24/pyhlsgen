import sys
import os
from enum import Enum


class Source(Enum):
    PLATFORM: str = sys.platform
    ALLOWED_EXTENSION: tuple = ('.mp4', '.m4v', '.mkv', '.wmv', '.avi', '.flv', '.mov', '.mpeg', '.asf')
    SOURCE_FILE_DIRECTORY: str = '.'
    DESTINATION_FILE_DIRECTORY: str = 'm3u8'


class Manager(object):
    def __init__(self):
        pass

    def get_movie_list(self):
        try:
            return self.extension_filter(lists=os.listdir(Source.SOURCE_FILE_DIRECTORY.value))
        except OSError:
            raise FileNotFoundError

    @staticmethod
    def extension_filter(lists: list) -> list:
        """
        ALLOWED_EXTENSIONにあるファイル拡張子に基づいてフィルタリングして、「リスト」で返す
        :param lists:
        :return allowed:
        """
        allowed = []
        for extension in lists:
            if os.path.splitext(extension)[1] in Source.ALLOWED_EXTENSION.value:
                allowed.append(extension)
        return allowed

    def get_movie_info(self, path: str) -> dict:
        """
        ffmpeg -i "path"　で出力されるデータを辞書形式にパースして返します
        """
        pass
