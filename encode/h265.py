class Default(object):
    def h265(self,
             source: str,
             dest: str,
             threads: int = 2,
             size: str = 'hd720',
             fps: int = 60,
             vcodec: str = "libx265",
             acodec: str = "copy",
             tag: str = "hvc1",
             bitrate: int = 44100,
             pix_fmt: str = "yuv420p",
             ) -> list:

        command = f"ffmpeg -i {source} -c:v {vcodec} -tag:v {tag} "\
                  f"-s {size} -r {fps} "\
                  f"-c:a {acodec} -ar {bitrate} "\
                  f"-threads {threads} "\
                  f"-pix_fmt {pix_fmt} "\
                  f"{dest}"
        return command.split(" ")
