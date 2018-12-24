import os
import sys
import subprocess
from encode.hls import Values
from encode.hls import Manager
from encode.h265 import CommandCreator


def main():
    if len(sys.argv) > 1:
        arg_codec = sys.argv[1]
    else:
        arg_codec = sys.argv[1]

    manager = Manager()
    command_creator = CommandCreator()
    manager.make_directory(path=Values.DESTINATION_FILE_DIRECTORY.value)
    working_directory = os.path.join(Values.SOURCE_FILE_DIRECTORY.value, Values.DESTINATION_FILE_DIRECTORY.value)

    for f in manager.get_movie_list():
        vcodec = manager.get_movie_info(path=os.path.join(Values.SOURCE_FILE_DIRECTORY.value, f))
        acodec = 'copy'
        target_dir = os.path.join(working_directory, os.path.splitext(f)[0])

        if not os.path.exists(target_dir):
            if arg_codec:
                comm = command_creator.h265(source=f, dest=os.path.splitext(f)[0] + ".mp4")
            else:
                manager.make_directory(path=target_dir)
                comm = f"ffmpeg -i {os.path.join(Values.SOURCE_FILE_DIRECTORY.value, f)} "\
                    f"-max_muxing_queue_size 1024 -c:v {vcodec} -tag:v hvc1 -vbsf h264_mp4toannexb "\
                    f"-c:a {acodec} -ar 44100 -pix_fmt yuv420p -map 0:0 -map 0:1 "\
                    f"-f segment -segment_format mpegts -segment_time 10 "\
                    f"-segment_list {os.path.join(target_dir, 'output.m3u8')} " \
                    f"{os.path.join(target_dir, 'stream-%06d.ts')}"

            comm = comm.split(" ")
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

