from subprocess import run
from os import chmod, scandir
from os.path import join, splitext
from operation.files import Values, Operation, Crop
from datetime import datetime
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


class Default(object):
    def __init__(self,
                 size: str,
                 vcodec: str,
                 acodec: str,
                 tag: str,
                 pix_fmt: str,
                 threads: int,
                 fps: int,
                 bitrate: int,
                 segment_time: int,
                 source: str = '',
                 dest: str = '',
                 limit_size: str = '',
                 file_name: str = '',
                 concat_name: str = '',):
        self.source: str = source
        self.dest: str = dest
        self.size: str = size
        self.vcodec: str = vcodec
        self.acodec: str = acodec
        self.tag: str = tag
        self.pix_fmt: str = pix_fmt
        now = str(datetime.now()).translate(
            str.maketrans({'-': '_', ' ': '_', '.': '_'})
        )
        self.file_name: str = file_name if file_name else f"{now}.txt"
        self.concat_name: str = concat_name if concat_name else f"{now}.mp4"
        self.command: str = ""
        self.segment_time = segment_time
        self.limit_size = limit_size
        self.threads: int = threads
        self.fps: int = fps
        self.bitrate: int = bitrate

    def get_video_size(self, path: str) -> tuple:
        video = VideoCapture(path)
        width = int(video.get(CAP_PROP_FRAME_WIDTH))
        height = int(video.get(CAP_PROP_FRAME_HEIGHT))
        return width, height

    def subprocess_run(self,
                       command: str,
                       shell: bool,
                       encoding: str = "utf-8"):
        if Values.PLATFORM.value == 'win32':
            run(['chcp', '65001'],
                shell=shell,
                encoding=encoding)
        run(command, shell=shell, encoding=encoding)

    def run(self, thumbnail: bool = False, noaudio: bool = False):
        output = join(self.vcodec, splitext(self.source)[0])
        ops = Operation()
        ops.make_directory(output)
        self.dest = output
        if thumbnail:
            crop = Crop()
            crop.thumbnail(source=self.source, target_dir=output)
        if Values.SOURCE_FILE_DIRECTORY.value == 'win32':
            shell = True
        else:
            shell = False

        self.subprocess_run(command=self.command_create(noaudio=noaudio),
                            shell=shell,
                            encoding='utf-8')

    def do_extension_fix_iso(self, source: str, dest: str) -> str:
        name, ext = splitext(source)
        if '.iso' == ext.lower():
            source = name + '.mp4'
        return join(dest, source)


class Others(Default):
    def command_create(self, noaudio: bool = False):
        media_map: str = "-map 0:v" if noaudio else "-map 0:v -map: 0:a"
        if self.size:
            video_size: str = self.size
        else:
            video_size: tuple = self.get_video_size(path=self.source)

        if isinstance(video_size, tuple):
            video_size: str = f"{video_size[0]}x{video_size[1]}"  # e.g.640x480

        dest = self.do_extension_fix_iso(source=self.source, dest=self.dest)
        command = f"ffmpeg -i {self.source} "\
                  f"-c:v {self.vcodec} -tag:v {self.tag} "\
                  f"-s {video_size} -r {self.fps} "\
                  f"-c:a {self.acodec} -ar {self.bitrate} "\
                  f"-threads {self.threads} "\
                  f"-pix_fmt {self.pix_fmt} "\
                  f"{media_map} "\
                  f"{dest}"
        return command.split(" ")


class hls(Default):
    def command_create(self, noaudio: bool = False):
        media_map: str = "-map 0:v" if noaudio else "-map 0:v -map: 0:a"
        if self.size:
            video_size: str = self.size
        else:
            video_size: tuple = self.get_video_size(path=self.source)

        if isinstance(video_size, tuple):
            video_size: str = f"{video_size[0]}x{video_size[1]}"  # e.g.640x480

        command = f"ffmpeg -i "\
            f"{join(Values.SOURCE_FILE_DIRECTORY.value, self.source)} "\
            f"-max_muxing_queue_size 1024 "\
            f"-c:v {self.vcodec} -tag:v {self.tag} "\
            f"-fs {self.limit_size} " \
            f"-s {video_size} -r {self.fps} "\
            f"-vbsf h264_mp4toannexb "\
            f"-pix_fmt {self.pix_fmt} {media_map} "\
            f"-c:a {self.acodec} -ar {self.bitrate} "\
            f"-threads {self.threads} "\
            f"-f segment -segment_format mpegts "\
            f"-segment_time {self.segment_time} "\
            f"-segment_list {join(self.dest, 'output.m3u8')} " \
            f"{join(self.dest, 'stream-%06d.ts')}"
        return command.split(" ")


class Concat(Default):
    def __get_movie_list(self, path: str = '.') -> iter:
        """
        結合する動画一覧を返す
        """
        with scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.')\
                   and entry.is_file()\
                   and splitext(entry.name)[1]\
                   in Values.ALLOWED_EXTENSION.value:
                    yield (entry.name)

    def write_concat_text(self, path: str = '.'):
        with open(file=join(path, self.file_name),
                  mode='wt',
                  encoding='utf-8') as fp:
            movie = []
            for i in self.__get_movie_list(path=path):
                movie.append(i)

            # 昇順でソートしてからテキストファイルに書き込みする
            [fp.write(f"file '{i}'\n") for i in sorted(movie)]
        try:
            chmod(self.file_name, 0o700)
        except OSError:
            pass

    def command_create(self, noaudio: bool = False):
        media_map: str = "-map 0:v" if noaudio else "-map 0:v -map: 0:a"
        if self.size:
            video_size: str = self.size
        else:
            video_size: tuple = self.get_video_size(path=self.source)

        if isinstance(video_size, tuple):
            video_size: str = f"{video_size[0]}x{video_size[1]}"  # e.g.640x480

        self.write_concat_text()
        command = f"""
                    ffmpeg -f concat -safe 0 -i {self.file_name} \
                    -c:v {self.vcodec} -tag:v {self.tag} \
                    -s {video_size} -r {self.fps} \
                    -pix_fmt {self.pix_fmt} \
                    -c:a {self.acodec} -ar {self.bitrate} \
                    -c:s copy \
                    {media_map} -map 0:s? \
                    -threads {self.threads} \
                    {self.concat_name}
                   """

        # リスト内の空白、改行コードを削除する。文字列に\nがあれば空白に置換する
        filled = [i.replace('\n', '')
                  for i in command.split(" ") if i and i != '\n']
        return filled
