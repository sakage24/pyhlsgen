from subprocess import run, PIPE
from os.path import join, splitext
from files import Values, Operation, Crop
from sys import platform
from re import search


class Default(object):
    def __init__(self, source, dest):
        args = Operation.do_parse_args()
        self.source: str = source
        self.dest: str = dest
        self.size: str = args['size']
        self.vcodec: str = args['vcodec']
        self.acodec: str = args['acodec']
        self.tag: str = args['tag']
        self.pix_fmt: str = args['pix_fmt']
        self.command: str = ""
        self.segment_time = args['segment_time']
        self.limit_size = args['limit_size']
        self.threads: int = args['threads']
        self.fps: int = args['fps']
        self.bitrate: int = args['bitrate']
        self.ishls: bool = args['hls']
        self.noaudio: bool = args['noaudio']
        self.thumbnail: bool = args['thumbnail']

    @staticmethod
    def get_video_size(path: str,
                       ffmpeg_bin_path: str = "/usr/bin/ffmpeg") -> tuple:
        command: list = f"{ffmpeg_bin_path} -i {path}".split()
        try:
            from cv2 import VideoCapture, \
                            CAP_PROP_FRAME_WIDTH, \
                            CAP_PROP_FRAME_HEIGHT
        except ImportError:
            # ffmpeg -iコマンドを使って手動で探索を試みる
            if platform == "linux":
                result = run(command,
                             shell=False,
                             encoding='utf-8',
                             stderr=PIPE)
            elif platform == "win32":
                result = run(command,
                             shell=True,
                             encoding='utf-8',
                             stderr=PIPE)
            for i in result.stderr.split():
                if search(pattern=r"^[0-9]+x[0-9]+$", string=i):
                    return tuple(i.split('x'))
            raise VideoSizeNotFoundError
        else:
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

    def run(self):
        output = join(self.vcodec, splitext(self.source)[0])
        self.dest = output
        ops = Operation()
        ops.make_directory(output)
        if self.thumbnail:
            crop = Crop()
            crop.thumbnail(source=self.source, target_dir=output)
        if Values.SOURCE_FILE_DIRECTORY.value == 'win32':
            shell = True
        else:
            shell = False

        self.subprocess_run(command=self.command_create(noaudio=self.noaudio),
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


class VideoSizeNotFoundError(Exception):
    pass
