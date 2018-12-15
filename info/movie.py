import sys
import os
from enum import Enum
from subprocess import Popen
from subprocess import PIPE


class Source(Enum):
    """
    グローバルで使える変数一覧
    """
    PLATFORM: str = sys.platform
    ALLOWED_EXTENSION: tuple = ('.mp4', '.m4v', '.mkv', '.wmv', '.avi', '.flv', '.mov', '.mpeg', '.asf')
    SOURCE_FILE_DIRECTORY: str = '.'
    DESTINATION_FILE_DIRECTORY: str = 'm3u8'


class Manager(object):
    """
    メディアファイルの取得、保存用のフォルダ作成などいろいろやる

    """
    def __init__(self):
        pass

    def get_movie_list(self) -> iter:
        """
        実質的にextension_filter関数のラッパー関数。
        media/以下のファイル一覧を含むジェネレータを返します。
        Parameters
        -----------
        Returns
        -----------
            result: list
        Raises
        -----------
            FileNotFoundError
                対象ディレクトリが存在しない可能性が微レ存
        """
        try:
            result = self.extension_filter(lists=os.listdir(Source.SOURCE_FILE_DIRECTORY.value))
        except OSError:
            raise FileNotFoundError
        else:
            return result

    @staticmethod
    def extension_filter(lists: list) -> iter:
        """
        ALLOWED_EXTENSIONにあるファイル拡張子に基づいてフィルタリングして、ジェネレータを返す
        Parameters
        ------------
            lists: list
                処理前のリスト。

        Returns
        -----------
            allowed: list
                処理結果のリスト。

        """
        for extension in lists:
            if os.path.splitext(extension)[1] in Source.ALLOWED_EXTENSION.value:
                yield extension


    def select_vcodec(self, codec: str) -> str:
        if 'h264' in codec:
            return 'copy'
        elif 'h265' in codec:
            return 'libx264'
        else:
            return 'libx264'

    def get_movie_info(self, path: str) -> str:
        """
        ffmpeg -i "path"　で出力されるデータから、動画のコーデックに関する情報を抽出して返します
        """
        from pprint import pprint
        command = f"ffmpeg -i {path}".split(' ')
        information = Popen(command, encoding="utf-8", shell=False, stdout=PIPE, stderr=PIPE)
        _, stderr_data = information.communicate()
        for text in stderr_data.strip().split("\n"):
            if "Stream" in text:
                return self.select_vcodec(codec=text)

    @staticmethod
    def make_directory(path: str) -> bool:
        """
        渡されたpathに対してos.makedirs()を実行します。
        Parameters
        ----------
            path: str
                作成するディレクトリのパス
        Returns
        ----------
            True
                ディレクトリの作成、権限の変更が成功した
            False
                上記が失敗した場合、パスが存在しない場合

        """
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                os.chmod(path, 0o705)
            except OSError:
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def get_replace_character(name: str) -> str:
        """
        ascii文字列以外は'_'に置換して返す

         Parameters
        ----------
        name: str
            変換前のファイル名。
        Returns
        -------
        fixed: str
            変換後のファイル名。
        """
        fixed = ""
        for n in name:
            try:
                fixed += '_' if ord(n) > 128 else n
            except TypeError:
                raise TypeError

        return fixed

if __name__ == '__main__':
    pass

