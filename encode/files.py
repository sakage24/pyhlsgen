import os
from os.path import exists
from os import chmod
from os import makedirs
from sys import argv
from sys import platform
from enum import Enum


class Values(Enum):
    """
    グローバルで使える変数一覧
    """
    PLATFORM: str = platform
    ALLOWED_EXTENSION: tuple = (
        '.mp4', '.m4v', '.mkv', '.wmv',
        '.avi', '.flv', '.mov', '.mpeg',
        '.asf', '.vob')
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
            result = self.extension_filter(
                lists=os.listdir(Values.SOURCE_FILE_DIRECTORY.value))
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
            if os.path.splitext(extension)[1] in \
               Values.ALLOWED_EXTENSION.value:
                yield extension


class Operation(object):
    @staticmethod
    def get_codecs(args: list = argv) -> tuple:
        if len(args) > 2:
            vcodec = args[1]
            acodec = args[2]
        elif len(args) > 1:
            vcodec = args[1]
            acodec = 'copy'
        else:
            vcodec = 'hls'
            acodec = 'copy'
        return (vcodec, acodec)

    @staticmethod
    def get_exts(codec: str) -> str:
        codecs = {
            'flv1': '.flv',
            'h264': '.mp4',
            'h265': '.mp4',
            'hevc': '.mp4',
            'hvc1': '.mp4',
            'libx264': '.mp4',
            'libx265': '.mp4',
            'mjpeg': '.jpeg',
            'mpeg1video': '.mpg',
            'mpeg2video': '.vob',
            'msvideo1': '.avi',
            'vp3': '.mkv',
            'vp6': '.mkv',
            'vp6a': '.flv',
            'vp6f': '.flv',
            'vp7': '.avi',
            'vp8': '.webm',
            'vp9': '.webm',
            'wmv1': '.wmv',
            'wmv2': '.wmv',
            'wmv3': '.wmv',
            'hls': '.m3u8',
        }

        if codec in codecs:
            return codecs[codec]
        else:
            return 'copy'

    @staticmethod
    def escape_chars(name: str) -> str:
        """
        エラーが出そうな文字列を置換して返す

        Parameters
        ----------
        name: str
            変換前のファイル名。
        Returns
        -------
        fixed: str
            変換後のファイル名。
        """
        chars: tuple = (' ', '　', '＿', '\\', '￥',)
        fixed: str = ""

        for n in name:
            try:
                if n in chars:
                    fixed += '_'
                elif 0x2600 <= ord(n) <= 0x26ff or n == '？':
                    fixed += '_'
                elif n == '（' or n == '【':
                    fixed += '('
                elif n == '）' or n == '】':
                    fixed += ')'
                elif n == '～':
                    fixed += '~'
                elif n == '＝':
                    fixed += '='
                elif n == '×':
                    fixed += 'x'
                elif n == '＃':
                    fixed += '#'
                elif n == '！':
                    fixed += '!'
                else:
                    fixed += n

            except TypeError as e:
                print(e)
        return fixed

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
        if not exists(path):
            try:
                makedirs(path)
                chmod(path, 0o705)
            except OSError:
                print(f"{path}ディレクトリの作成に失敗しました...")
                return False
            else:
                return True
        else:
            print(f"{path}はすでに存在します...")
            return False
