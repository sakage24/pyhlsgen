from os import rename
from os.path import join
from codec import hls, Others
from files import Values, Operation


def main():
    ops = Operation()
    args = ops.do_parse_args()
    thumbnail: bool = False
    for f in ops.get_movie_list():
        fixed = ops.escape_chars(name=f)
        try:
            rename(src=f, dst=fixed)
        except OSError:
            raise OSError
        else:
            if args['hls']:
                # hls形式のストリーミングファイルを作成
                encode = hls(source=f, dest=fixed)
            else:
                # 他のコーデック形式への変換
                encode = Others(source=f, dest=fixed)
        try:
            encode.run()
        except KeyboardInterrupt:
            print('ユーザにより処理が中断されました...')


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
