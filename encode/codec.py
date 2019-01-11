from subprocess import run
from os.path import join
from os.path import splitext
from operation.files import Values
from operation.files import Operation
from operation.files import Crop


class Default(object):
    def __init__(self,
                 source: str,
                 dest: str,
                 threads: int = 0,
                 fps: int = 0,
                 size: str = 'hd480',
                 vcodec: str = "",
                 acodec: str = "",
                 tag: str = "",
                 bitrate: int = "",
                 pix_fmt: str = "",
                 segment_time: int = 0,
                 ):
        self.source: str = source
        self.dest: str = dest
        self.size: str = size
        self.threads: int = threads if source else 2
        self.fps: int = fps if fps else 24
        self.vcodec: str = vcodec if vcodec else "libx264"
        self.acodec: str = acodec if acodec else "copy"
        self.tag: str = tag if tag else "hvc1"
        self.bitrate: int = bitrate if bitrate else 44100
        self.pix_fmt: str = pix_fmt if pix_fmt else "yuv420p"
        self.segment_time: int = segment_time if segment_time else 10
        self.command: str = ""

    def subprocess_run(self,
                       command: str,
                       shell: bool,
                       encoding: str = "utf-8"):
        if Values.PLATFORM.value == 'win32':
            run(['chcp', '65001'],
                shell=shell,
                encoding=encoding)
        run(command, shell=shell, encoding=encoding)

    def run(self, thumbnail=False):
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

        self.subprocess_run(command=self.command_create(),
                            shell=shell)


class h265(Default):
    def command_create(self):
        command = f"ffmpeg -i {self.source} -c:v {self.vcodec} -tag:v {self.tag} "\
                  f"-s {self.size} -r {self.fps} "\
                  f"-c:a {self.acodec} -ar {self.bitrate} "\
                  f"-threads {self.threads} "\
                  f"-pix_fmt {self.pix_fmt} "\
                  f"{join(self.dest, self.source)}"
        return command.split(" ")


class hls(Default):
    def command_create(self):
        command = f"ffmpeg -i "\
            f"{join(Values.SOURCE_FILE_DIRECTORY.value, self.source)} "\
            f"-max_muxing_queue_size 1024 "\
            f"-c:v {self.vcodec} -tag:v {self.tag} -s {self.size} -r {self.fps} "\
            f"-vbsf h264_mp4toannexb "\
            f"-pix_fmt {self.pix_fmt} -map 0:0 -map 0:1 "\
            f"-c:a {self.acodec} -ar {self.bitrate} "\
            f"-threads {self.threads} "\
            f"-f segment -segment_format mpegts "\
            f"-segment_time {self.segment_time} "\
            f"-segment_list {join(self.dest, 'output.m3u8')} " \
            f"{join(self.dest, 'stream-%06d.ts')}"
        return command.split(" ")
