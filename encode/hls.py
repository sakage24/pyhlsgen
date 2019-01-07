from os.path import join
from operation.files import Values


class CommandCreator(object):
    def hls(self,
            source: str,
            target_dir: str,
            size: str = 'hd720',
            fps: int = 24,
            vcodec: str = "libx264",
            acodec: str = "ac3",
            threads: int = 2,
            tag: str = "hvc1",
            bitrate: int = 44100,
            segment_time: int = 10,
            pix_fmt: str = "yuv420p",
            ) -> list:

        comm = f"ffmpeg -i "\
               f"{join(Values.SOURCE_FILE_DIRECTORY.value, source)} "\
               f"-max_muxing_queue_size 1024 "\
               f"-c:v {vcodec} -tag:v {tag} -s {size} -r {fps} -vbsf h264_mp4toannexb "\
               f"-pix_fmt {pix_fmt} -map 0:0 -map 0:1 "\
               f"-c:a {acodec} -ar {bitrate} "\
               f"-threads {threads} "\
               f"-f segment -segment_format mpegts "\
               f"-segment_time {segment_time} "\
               f"-segment_list {join(target_dir, 'output.m3u8')} " \
               f"{join(target_dir, 'stream-%06d.ts')}"
        return comm.split(" ")
