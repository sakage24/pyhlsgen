from subprocess import run
from os.path import join
from operation.files import Values
from operation.files import Crop
from operation.files import Operation


class Default(object):
    def hls(self,
            source: str,
            target_dir: str,
            size: str = 'hd480',
            fps: int = 60,
            vcodec: str = "libx264",
            acodec: str = "copy",
            threads: int = 2,
            tag: str = "hvc1",
            bitrate: int = 44100,
            segment_time: int = 10,
            pix_fmt: str = "yuv420p",
            ) -> list:

        crop = Crop()
        crop.thumbnail(source=source, target_dir=target_dir)
        comm = f"ffmpeg -i "\
               f"{join(Values.SOURCE_FILE_DIRECTORY.value, source)} "\
               f"-max_muxing_queue_size 1024 "\
               f"-c:v {vcodec} -tag:v {tag} -s {size} -r {fps} "\
               f"-vbsf h264_mp4toannexb "\
               f"-pix_fmt {pix_fmt} -map 0:0 -map 0:1 "\
               f"-c:a {acodec} -ar {bitrate} "\
               f"-threads {threads} "\
               f"-f segment -segment_format mpegts "\
               f"-segment_time {segment_time} "\
               f"-segment_list {join(target_dir, 'output.m3u8')} " \
               f"{join(target_dir, 'stream-%06d.ts')}"
        return comm.split(" ")

    def run(self,
            name: str,
            vcodec: str = 'libx264',
            acodec: str = 'copy',
            tag: str = 'hvc1'):
        dirs = './m3u8'
        output = join(dirs, name)
        ops = Operation()
        ops.make_directory(output)
        command = self.hls(
            source=name,
            target_dir=output,
            vcodec=vcodec,
            acodec=acodec,
            tag=tag,
        )
        if Values.PLATFORM.value == 'win32':
            run(['chcp', '65001'],
                shell=True,
                encoding='utf-8')
            run(command, shell=True, encoding='utf-8')
        elif Values.PLATFORM.value == 'linux':
            run(command, shell=False, encoding='utf-8')
