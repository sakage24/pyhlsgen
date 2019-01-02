from os.path import exists
from os import chmod
from os import makedirs
from sys import argv


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
            vcodec = 'copy'
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
                elif n == '（' or n == '【':
                    fixed += '('
                elif n == '）' or n == '】':
                    fixed += ')'
                elif n == '～':
                    fixed += '~'
                else:
                    fixed += n

            except TypeError:
                print(fixed)
                raise TypeError
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
                return False
            else:
                return True
        else:
            return False
