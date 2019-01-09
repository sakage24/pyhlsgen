from os import rename
from sys import argv
from encode.hls import Default as hls_command
from encode.h265 import Default as h265_command
from operation.files import Values
from operation.files import Operation


def main():
    ops = Operation()
    hls = hls_command()
    h265 = h265_command()

    for f in ops.get_movie_list():
        fixed = ops.escape_chars(name=f)
        try:
            rename(src=f, dst=fixed)
        except OSError:
            raise OSError
        else:
            if len(argv) <= 1:
                hls.run(name=fixed)
            else:
                h265.run(name=fixed)


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
