import os
import sys
import subprocess
from encode.hls import Values
from encode.hls import Manager
from encode.hls import CommandCreator as hls_command
from encode.h265 import CommandCreator as h265_command
from encode.files import Operation


def main():
    operation = Operation()
    manager = Manager()
    hls = hls_command()
    h265 = h265_command()
    vcodec, acodec = Operation.get_codecs(args=sys.argv)
    ext = operation.get_exts(codec=vcodec)

    output_directory = os.path.join(
        Values.SOURCE_FILE_DIRECTORY.value,
        Values.DESTINATION_FILE_DIRECTORY.value)

    for f in manager.get_movie_list():
        after_file_name = operation.escape_chars(name=f)
        try:
            os.rename(src=f, dst=after_file_name)
        except OSError:
            raise OSError
        else:
            f = after_file_name

            if vcodec:
                if os.path.exists(os.path.splitext(f)[0] + f"_{vcodec}{ext}"):
                    print("すでに存在するため、スキップします...")
                comm = h265.h265(source=f,
                                 dest=os.path.splitext(
                                     f)[0] + f"_{vcodec}{ext}",
                                 vcodec=vcodec,
                                 acodec=acodec,)
            else:
                target_dir = os.path.join(output_directory,
                                          os.path.splitext(f)[0])

                operation.make_directory(path=target_dir)
                comm = hls.hls(source=f, target_dir=target_dir,
                               vcodec=vcodec, acodec=acodec)

            if Values.PLATFORM.value == 'win32':
                subprocess.run(['chcp', '65001'],
                               shell=True, encoding='utf-8')
                subprocess.run(comm, shell=True, encoding='utf-8')
            elif Values.PLATFORM.value == 'linux':
                subprocess.run(comm, shell=False, encoding='utf-8')
            else:
                print('対応していないディストリビューションで実行しています...\nプログラムを終了します。')
                sys.exit(1)


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")
