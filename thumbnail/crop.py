from subprocess import run
from os import makedirs
from os.path import exists
from os.path import join
from os.path import dirname


class Image(object):
    def on_call_message(self,
                        source: str,
                        ss: int,
                        framerate: float,
                        output_file_name: str,
                        platform: str):
        print(
            f"""
                サムネイルの撮影を開始しています...。

                - ソースファイル: {source}
                - タイミング: {ss}秒に1枚
                - フレームレート: {1/framerate}
                - 保存先: {output_file_name}
                - プラットフォーム(OS): {platform}

            """
        )

    def create_thumbnail(self,
                         source: str,
                         target_dir: str,
                         ss: int = 10,
                         frame_per_second: float = 0.03,
                         output_file_name: str = "thumbnail_%06d.jpg",
                         platform: str = "Linux",
                         ):
        output_dir: str = join(target_dir, 'thumbnails')
        command = f"ffmpeg -i {source} "\
                  f"-ss {ss} -r {frame_per_second} "\
                  f"-f image2 "\
                  f"{join(output_dir, output_file_name)}"
        command = command.split(" ")

        try:
            if not exists(path=output_dir):
                makedirs(output_dir, mode=0o700)
        except OSError:
            return False
        else:
            self.on_call_message(source=source,
                                 ss=ss,
                                 framerate=frame_per_second,
                                 output_file_name=output_file_name,
                                 platform=platform)
            if platform == "Linux":
                run(command, shell=False, encoding='utf-8')
            elif platform == "win32":
                run(command, shell=True, encoding='utf-8')
            else:
                return False


if __name__ == '__main__':
    image = Image()
    image.create_thumbnail(
        source="test/output.m3u8",
    )
