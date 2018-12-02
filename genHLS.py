import os
import sys
import subprocess
from info.movie import Source
from info.movie import Manager


def rename_file(name: str) -> str:
    fixed = ""
    for n in name:
        if ord(n) > 128:
            fixed += '_'
        else:
            fixed += n
    return fixed


def get_dict_by_filesize(file_list: list) -> dict:
    file_info = []
    for f in file_list:
        file_info.append((f, os.path.getsize(f)))
    return dict(file_info)


def get_vcodec(ext: str) -> str:
        return "libx264"


def get_acodec(ext: str) -> str:
    if ".iso" in ext:
        return "ac3"
    else:
        return "copy"


def make_dir(*, p):
    if not os.path.exists(p):
        os.makedirs(p)
        os.chmod(p, 0o705)
        print(f'{p}を作成しました...')


def main():
    make_dir(p=Source.DESTINATION_FILE_DIRECTORY.value)
    manager = Manager()
    working_directory = os.path.join(Source.SOURCE_FILE_DIRECTORY.value, Source.DESTINATION_FILE_DIRECTORY.value)

    for f in manager.get_movie_list():
        replace_file_name = rename_file(name=f.replace(' ', '_'))
        file_ext = os.path.splitext(f)[1].lower()
        try:
            os.rename(f, replace_file_name)
        except OSError as e:
            print(f'RENAME中にエラーが発生しました...\n対象ファイル: {f}\nエラー内容: {e}')
        else:
            vcodec = get_vcodec(ext=file_ext)
            acodec = get_acodec(ext=file_ext)
            if vcodec == "unknown":
                print("本スクリプトは、このタイプのファイルにはまだ対応していません！")
                print(f"ファイル名: {f}")
                continue
            target_dir = os.path.join(Source.DESTINATION_FILE_DIRECTORY.value, f.replace(' ', '_'))

            if not os.path.exists(target_dir):
                make_dir(p=target_dir)
                comm = f"ffmpeg -i {os.path.join(working_directory, replace_file_name)}" \
                    f"-max_muxing_queue_size 1024 -c:v {vcodec} -vbsf h264_mp4toannexb "\
                    f"-c:a {acodec} -ar 44100 -pix_fmt yuv420p -map 0:0 -map 0:1 "\
                    f"-f segment -segment_format mpegts -segment_time 10 "\
                    f"-segment_list {os.path.join(target_dir, 'output.m3u8')} " \
                    f"{os.path.join(target_dir, 'stream-%06d.ts')}"
                comm = comm.split(" ")

                if Source.PLATFORM.value == 'win32':
                    subprocess.run(['chcp', '65001'], shell=True, encoding='utf-8')
                    subprocess.run(comm, shell=True, encoding='utf-8')
                elif Source.PLATFORM.value == 'linux':
                    subprocess.run(comm, shell=False, encoding='utf-8')
                else:
                    print('対応していないディストリビューションで実行しています...\nプログラムを終了します。')
                    sys.exit(1)
            else:
                print(f'{f}は既にありますのでスキップします...')

        finally:
            os.rename(replace_file_name,  f)
            print(f"処理が終わったので、元のファイル名にRENAME完了...{os.path.join(working_directory, f)}")

    if Source.PLATFORM.value == 'win32':
        input("\n\nすべての処理が完了しました...")


main()
