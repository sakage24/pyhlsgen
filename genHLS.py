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
    arg_vcodec, arg_acodec = Operation.get_args(args=sys.argv)

    output_directory = os.path.join(
        Values.SOURCE_FILE_DIRECTORY.value,
        Values.DESTINATION_FILE_DIRECTORY.value)

    for f in manager.get_movie_list():
        vcodec = manager.get_movie_info(path=os.path.join(
            Values.SOURCE_FILE_DIRECTORY.value, f))
        acodec = 'copy'
        target_dir = os.path.join(output_directory,
                                  os.path.splitext(f)[0])

        if not os.path.exists(target_dir):
            if arg_vcodec:
                comm = h265.h265(source=f,
                                 dest=os.path.splitext(f)[0] + "_h265.mp4",
                                 vcodec=arg_vcodec,
                                 acodec=arg_acodec)
            else:
                manager.make_directory(
                    path=Values.DESTINATION_FILE_DIRECTORY.value)
                manager.make_directory(path=target_dir)
                comm = hls.hls(source=f, target_dir=target_dir,
                               vcodec=vcodec, acodec=acodec)

            if Values.PLATFORM.value == 'win32':
                subprocess.run(['chcp', '65001'], shell=True, encoding='utf-8')
                subprocess.run(comm, shell=True, encoding='utf-8')
            elif Values.PLATFORM.value == 'linux':
                subprocess.run(comm, shell=False, encoding='utf-8')
            else:
                print('対応していないディストリビューションで実行しています...\nプログラムを終了します。')
                sys.exit(1)
        else:
            print(f'{f}は既にありますのでスキップします...')


main()

if Values.PLATFORM.value == 'win32':
    input("\n\nすべての処理が完了しました...")
else:
    print("\n\nすべての処理が完了しました...")

