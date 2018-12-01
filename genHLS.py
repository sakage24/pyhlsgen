import os
import sys
import subprocess
import shutil


class movieInfoManager(object):
    def __init__(self):
        pass


    def get_movie_info(self, path: str) -> dict:
        """
        ffmpeg -i "path"　で出力されるデータを辞書形式にパースして返します
        """
        pass


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
    arg = sys.argv[1] if sys.argv[1:] else ""
    platform = sys.platform
    allow_ext = ('.mp4', '.m4v', '.mkv', '.wmv', '.avi', '.flv', '.mov', '.mpeg', '.asf')
    work_dir, dist_dir = '.', 'm3u8'
    base_dir = os.path.join(work_dir, dist_dir)
    make_dir(p=base_dir)

    file_list = []
    for x in os.listdir(work_dir):
        if os.path.isfile(os.path.join(work_dir, x)) and\
        os.path.splitext(x)[1].lower() in allow_ext and\
        (x != '.' or x != '..'):
            file_list.append(x)

    all_size_info = get_dict_by_filesize(file_list=file_list)
    # ファイルの小さいものから順にエンコードしていくようにソートする
    file_list = [files[0] for files in sorted(all_size_info.items(), key=lambda x: x[1], reverse=False)]
    print()
    [print('- ' + x) for x in file_list]
    print(f'\n変換元の動画ディレクトリ: \'{work_dir}\'')
    print(f'変換先の動画ディレクトリ: \'{dist_dir}\'\n')
    if arg == '--auto' or arg == '-a':
        command = ""
    else:
        command = False

    if command:
        print(f'入力キー: \'{command}\'\n処理を終了します...')
        shutil.rmtree(base_dir)
        sys.exit(0)
    else:
        for f in file_list:
            replace_file_name = rename_file(name=f.replace(' ', '_'))
            file_name = os.path.splitext(f)[0]
            file_ext = os.path.splitext(f)[1].lower()
            try:
                os.rename(os.path.join(work_dir, f), os.path.join(work_dir, replace_file_name))
            except OSError as e:
                print(f'RENAME中にエラーが発生しました...\n対象ファイル: {f}\nエラー内容: {e}')
            else:
                vcodec = get_vcodec(ext=file_ext)
                acodec = get_acodec(ext=file_ext)
                if vcodec == "unknown":
                    print("本スクリプトは、このタイプのファイルにはまだ対応していません！")
                    print(f"ファイル名: {f}")
                    continue
                target_dir = os.path.join(base_dir, f.replace(' ', '_'))

                if not os.path.exists(target_dir):
                    make_dir(p=target_dir)
                    comm = f"ffmpeg -i {os.path.join(work_dir, replace_file_name)} -max_muxing_queue_size 1024 -c:v {vcodec} -vbsf h264_mp4toannexb "\
                        f"-c:a {acodec} -ar 44100 -pix_fmt yuv420p -map 0:0 -map 0:1 -f segment -segment_format mpegts -segment_time 10 "\
                        f"-segment_list {os.path.join(target_dir, 'output.m3u8')} " \
                        f"{os.path.join(target_dir, 'stream-%06d.ts')}"
                    comm = comm.split(" ")

                    if platform == 'win32':
                        subprocess.run(['chcp', '65001'], shell=True, encoding='utf-8')
                        subprocess.run(comm, shell=True, encoding='utf-8')
                    elif platform == 'linux':
                        subprocess.run(comm, shell=False, encoding='utf-8')
                    else:
                        print('対応していないディストリビューションで実行しています...\nプログラムを終了します。')
                        sys.exit(1)
                else:
                    print(f'{f}は既にありますのでスキップします...')

            finally:
                os.rename(os.path.join(work_dir, replace_file_name), os.path.join(work_dir, f))
                print(f"処理が終わったので、元のファイル名にRENAME完了...{os.path.join(work_dir, f)}")

    if platform == 'win32':
        input("\n\nすべての処理が完了しました...")


main()
