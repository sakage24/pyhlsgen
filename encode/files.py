from os.path import exists
from os import chmod
from os import makedirs
from sys import argv


class Operation(object):
    @staticmethod
    def get_codecs(args: list = argv) -> tuple:
        if len(args) > 2:
            vcodec = args[1]
            acodec = args[2]
        elif len(args) > 1:
            vcodec = args[1]
            acodec = 'copy'
        else:
            vcodec = ''
            acodec = ''
        return (vcodec, acodec)

    @staticmethod
    def escape_chars(name: str) -> str:
        """
        エラーが出そうな文字列を置換して返す

         Parameters
        ----------
        name: str
            変換前のファイル名。
        Returns
        -------
        fixed: str
            変換後のファイル名。
        """
        chars: tuple = (' ', '　', '＿', '\\', '￥',)
        fixed: str = ""

        for n in name:
            try:
                if n in chars:
                    fixed += '_'
                elif n == '（' or n == '【':
                    fixed += '('
                elif n == '）' or n == '】':
                    fixed += ')'
                elif n == '～':
                    fixed += '~'
                else:
                    fixed += n

            except TypeError:
                print(fixed)
                raise TypeError
        return fixed

    @staticmethod
    def make_directory(path: str) -> bool:
        """
        渡されたpathに対してos.makedirs()を実行します。
        Parameters
        ----------
            path: str
                作成するディレクトリのパス
        Returns
        ----------
            True
                ディレクトリの作成、権限の変更が成功した
            False
                上記が失敗した場合、パスが存在しない場合

        """
        if not exists(path):
            try:
                makedirs(path)
                chmod(path, 0o705)
            except OSError:
                return False
            else:
                return True
        else:
            return False
