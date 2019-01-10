from os import rename
from os.path import join
from sys import argv
from encode.codec import hls
from encode.codec import h265
from operation.files import Values
from operation.files import Operation


def main():
    ops = Operation()

    for f in ops.get_movie_list():
        fixed = ops.escape_chars(name=f)
        try:
            rename(src=f, dst=fixed)
        except OSError:
            raise OSError
        else:
            vcodec, acodec = Operation.get_codecs(argv)
            if len(argv) <= 1:
                encode = hls(
                    source=fixed,
                    dest=join('m3u8', fixed),
                    vcodec=vcodec,
                    acodec=acodec,
                )
            else:
                encode = h265(
                    source=fixed,
                    dest=join(vcodec, fixed),
                    vcodec=vcodec,
                    acodec=acodec,
                )
            encode.run()


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
