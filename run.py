from os import rename
from os.path import join
from sys import argv
from encode.codec import hls
from encode.codec import h265
from operation.files import Values
from operation.files import Operation


def main():
    ops = Operation()
    args = Operation.do_parse_args()
    vcodec = args['vcodec']
    acodec = args['acodec']
    tag = args['tag']
    size = args['size']
    thumbnail = args['thumbnail']
    threads = args['threads']
    fps = args['fps']
    bitrate = args['bitrate']
    pix_fmt = args['pix_fmt']
    segment_time = args['segment_time']

    for f in ops.get_movie_list():
        fixed = ops.escape_chars(name=f)
        try:
            rename(src=f, dst=fixed)
        except OSError:
            raise OSError
        else:
            if args['vcodec'] == 'hls' or args['vcodec'] == 'm3u8':
                print('hls or m3u8形式のエンコードにはlibx264のみ利用しています...')
                encode = hls(
                    source=fixed,
                    dest=join('m3u8', fixed),
                    vcodec='libx264',
                    acodec=acodec,
                    tag=tag,
                    size=size,
                    threads=threads,
                    fps=fps,
                    bitrate=bitrate,
                    pix_fmt=pix_fmt,
                    segment_time=segment_time,
                )
            else:
                encode = h265(
                    source=fixed,
                    dest=join(vcodec, fixed),
                    vcodec=vcodec,
                    acodec=acodec,
                    tag=tag,
                    size=size,
                    threads=threads,
                    fps=fps,
                    bitrate=bitrate,
                    pix_fmt=pix_fmt,
                    segment_time=segment_time,
                )

            encode.run(thumbnail=True)


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
