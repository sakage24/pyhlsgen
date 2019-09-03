from os import listdir, mkdir
from os.path import exists, join
from subprocess import run


ss = "00:00:15"
size = "256x192"
thumbnail_dir = "thumbnails"
thumbnail_name = "thumbnail_%06d.jpg"
dir_list: list = [i for i in listdir() if i != __file__]
for i in dir_list:
    thumbnail_path = join(i, thumbnail_dir)
    source: str = join(i, 'output.m3u8')
    if not exists(thumbnail_path):
        try:
            mkdir(thumbnail_path, 0o755)
        except FileExistsError:
            pass

        command: list = f"ffmpeg -i {source} -f image2 -ss {ss} -vframes 1 -s \
                         {size} {join(thumbnail_path, thumbnail_name)}".split()
        result = run(command)
        print(result.stdout)
