class CommandCreator(object):
    def h265(self, source: str, dest: str) -> list:
        return f"ffmpeg -i {source} -c:v libx265 -tag:v hvc1 {dest}".split(" ")

