import sys
import os
from enum import Enum
from subprocess import Popen
from subprocess import PIPE


class Values(Enum):
    """
    グローバルで使える変数一覧
    """
    PLATFORM: str = sys.platform
    ALLOWED_EXTENSION: tuple = (
        '.mp4', '.m4v', '.mkv', '.wmv',
        '.avi', '.flv', '.mov', '.mpeg',
        '.asf', '.vob')
    SOURCE_FILE_DIRECTORY: str = '.'
    DESTINATION_FILE_DIRECTORY: str = 'm3u8'


class CommandCreator(object):
    def hls(self, source: str, target_dir: str,
            vcodec: str = "libx264",
            acodec: str = "copy") -> list:
        comm = f"ffmpeg -i "\
            f"{os.path.join(Values.SOURCE_FILE_DIRECTORY.value, source)} "\
            f"-max_muxing_queue_size 1024 "\
            f"-c:v {vcodec} -tag:v hvc1 -vbsf h264_mp4toannexb "\
            f"-c:a {acodec} -ar 44100 -pix_fmt yuv420p -map 0:0 -map 0:1 "\
            f"-f segment -segment_format mpegts -segment_time 10 "\
            f"-segment_list {os.path.join(target_dir, 'output.m3u8')} " \
            f"{os.path.join(target_dir, 'stream-%06d.ts')}"
        return comm.split(" ")


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
        command = f"ffmpeg -i {path}".split(' ')
        information = Popen(command, encoding="utf-8",
                            shell=False, stdout=PIPE, stderr=PIPE)
        _, stderr_data = information.communicate()
        for text in stderr_data.strip().split("\n"):
            if "Stream" in text:
                return self.select_vcodec(codec=text)


if __name__ == '__main__':
    pass
