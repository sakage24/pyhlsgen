from os.path import exists
from os.path import join
from os.path import splitext
from os import listdir
from os import makedirs
from os import chmod
from sys import platform
from enum import Enum
from subprocess import run
from argparse import ArgumentParser
import cv2


class Crop(object):
    def thumbnail(self,
                  source: str,
                  target_dir: str,
                  ss: int = '00:00:08',
                  size: str = '256x192',
                  output_file_name: str = "thumbnail_%06d.jpg",
                  platform: str = "linux"):
        output_dir: str = join(target_dir, 'thumbnails')
        command = f"ffmpeg -i {source} -f image2 -ss {ss} "\
                  f"-vframes 1 -s {size} {join(output_dir, output_file_name)}"
        command = command.split(" ")

        try:
            if not exists(path=output_dir):
                makedirs(output_dir, mode=0o705)
        except OSError:
            return False
        else:
            if platform == "linux":
                run(command, shell=False, encoding='utf-8')
            elif platform == "win32":
                run(command, shell=True, encoding='utf-8')
            else:
                return False


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


class Operation(object):
    @staticmethod
    def do_parse_args() -> dict:
        parser = ArgumentParser(description='You can use some arguments.')
        parser.add_argument('-v', '--vcodec',
                            default='libx265', type=str)
        parser.add_argument('-a', '--acodec',
                            default='copy',    type=str)
        parser.add_argument(
            '--tag',                default='hvc1',    type=str)
        parser.add_argument(
            '--size',               default='640x480', type=str)
        parser.add_argument(
            '--threads',            default=2,         type=int)
        parser.add_argument(
            '--fps',                default=30,        type=int)
        parser.add_argument(
            '--bitrate',            default=44100,     type=int)
        parser.add_argument(
            '--pix_fmt',            default='yuv420p', type=str)
        parser.add_argument('--segment_time',
                            default=10,        type=int)
        parser.add_argument('--thumbnail',          action='store_true')
        parser.add_argument('-c', '-j', '--concat', action='store_true')
        return vars(parser.parse_args())

    @staticmethod
    def get_movie_sec(path: str) -> int:
        v = cv2.VideoCapture(path)
        frame = v.get(cv2.CAP_PROP_FRAME_COUNT)  # フレーム数を取得する
        fps = v.get(cv2.CAP_PROP_FPS)           # FPS を取得する
        return frame // fps

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
                chmod(path, 0o700)
            except OSError:
                print(f"{path}ディレクトリの作成に失敗しました...")
                return False
            else:
                return True
        else:
            print(f"{path}はすでに存在します...")
            return False

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
                lists=listdir(Values.SOURCE_FILE_DIRECTORY.value))
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
            if splitext(extension)[1] in \
               Values.ALLOWED_EXTENSION.value:
                yield extension
