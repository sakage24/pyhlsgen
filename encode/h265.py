from subprocess import run
from os.path import join
from operation.files import Values
from operation.files import Operation


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

    def run(self,
            name: str,
            vcodec: str = 'libx265',
            acodec: str = 'copy',
            tag: str = 'hvc1'):
        dirs = vcodec
        output = join(dirs, name)
        ops = Operation()
        ops.make_directory(dirs)
        command = self.h265(
            source=name,
            dest=output,
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
