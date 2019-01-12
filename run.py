from os import rename
from os.path import join
from encode.codec import hls
from encode.codec import h265
from encode.codec import Concat
from operation.files import Values
from operation.files import Operation


def main():
    ops = Operation()
    args:         dict = Operation.do_parse_args()
    vcodec:       str = args['vcodec']
    acodec:       str = args['acodec']
    tag:          str = args['tag']
    size:         str = args['size']
    pix_fmt:      str = args['pix_fmt']
    threads:      int = args['threads']
    fps:          int = args['fps']
    bitrate:      int = args['bitrate']
    segment_time: int = args['segment_time']
    thumbnail:    bool = args['thumbnail']
    isjoin:       bool = args['concat']

    for f in ops.get_movie_list():
        fixed = ops.escape_chars(name=f)
        try:
            rename(src=f, dst=fixed)
        except OSError:
            raise OSError
        else:
            if isjoin:
                encode = Concat()
                encode.run()
                return
            elif args['vcodec'] == 'hls' or args['vcodec'] == 'm3u8':
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

            encode.run(thumbnail=thumbnail)


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
