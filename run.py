from os import rename
from os.path import join
from codec import hls, Others, Concat
from files import Values, Operation


def main():
    ops = Operation()
    args:         dict = Operation.do_parse_args()
    vcodec:       str = args['vcodec']
    acodec:       str = args['acodec']
    tag:          str = args['tag']
    size:         str = args['size']
    pix_fmt:      str = args['pix_fmt']
    limit_size:   str = args['limit_size']
    threads:      int = args['threads']
    fps:          int = args['fps']
    bitrate:      int = args['bitrate']
    segment_time: int = args['segment_time']
    thumbnail:    bool = args['thumbnail']
    noaudio:      bool = args['noaudio']
    hls_encode:   bool = args['hls']
    isjoin:       bool = args['concat']

    for f in ops.get_movie_list():
        fixed = ops.escape_chars(name=f)
        try:
            rename(src=f, dst=fixed)
        except OSError:
            raise OSError
        else:
            if isjoin:
                # 動画の結合
                encode = Concat(
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
                encode.run()
                return
            elif hls_encode:
                # hls形式のストリーミングファイルを作成
                thumbnail = True
                encode = hls(
                    source=fixed,
                    dest=join('m3u8', fixed),
                    vcodec=vcodec,
                    acodec=acodec,
                    tag=tag,
                    size=size,
                    threads=threads,
                    fps=fps,
                    bitrate=bitrate,
                    pix_fmt=pix_fmt,
                    segment_time=segment_time,
                    limit_size=limit_size,
                )
            else:
                # 他のコーデック形式への変換
                encode = Others(
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

            encode.run(thumbnail=thumbnail, noaudio=noaudio)


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
