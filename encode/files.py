from sys import argv


class Operation(object):
    def get_args(self, args: list = argv) -> tuple:
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
    def rename_space_to_under(name: str) -> str:
        """
        エラーが出そうな文字列を'_'に置換して返す

         Parameters
        ----------
        name: str
            変換前のファイル名。
        Returns
        -------
        fixed: str
            変換後のファイル名。
        """
        chars: tuple = (
            ' ', '　', '！', '？',
            '＿', '（', '）', '～',
            'ー', '＝', '￥', '\\',
            '【', '】',
        )
        fixed = ""
        for n in name:
            try:
                fixed += '_' if n in chars else n
            except TypeError:
                raise TypeError

        return fixed
