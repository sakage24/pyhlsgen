from subprocess import run
import os


class Image(object):
    def create_thumbnail(self,
                         source: str,
                         ss: int = 10,
                         frame_per_second: float = 0.03,
                         output_dir: str = "images",
                         output_file_name: str = "thumbnail_%06d.jpg",
                         platform: str = "Linux",
                         ):
        command = f"ffmpeg -i {source} "\
                  f"-ss {ss} -r {frame_per_second} "\
                  f"-f image2 "\
                  f"{os.path.join(output_dir, output_file_name)}"
        command = command.split(" ")

        try:
            if not self.check_exist_dir(dst=output_dir):
                os.makedirs(output_dir, mode=0o700)
        except OSError:
            return False
        else:
            if platform == "Linux":
                run(command, shell=False, encoding='utf-8')
            elif platform == "win32":
                run(command, shell=True, encoding='utf-8')
            else:
                return False

    def check_exist_dir(self, dst: str) -> bool:
        if os.path.exists(dst):
            return True
        else:
            return False


if __name__ == '__main__':
    image = Image()
    image.create_thumbnail(source="衣装がずれてブラジャー丸出しダンス_-_TOKYO_Motion_libx265.mp4")
