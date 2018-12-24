class CommandCreator(object):
    def h265(self, source: str, dest: str, vcodec: str = "libx265", acodec: str = "copy", tag: str = "hvc1", bitrate: int = 44100, pix_fmt: str = "yuv420p") -> list:
        return f"ffmpeg -i {source} -c:v {vcodec} -tag:v {tag} -c:a {acodec} -ar {bitrate} -pix_fmt {pix_fmt} {dest}".split(" ")
