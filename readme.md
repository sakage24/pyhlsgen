# pyhlsgen

## `pyhlsgen`は`python`を利用して複雑な`ffmpeg`のコマンドを簡略化するラッパープログラムです。

- このプログラムの実行には[ffmpeg](https://ffmpeg.org/)が必要です。また、各種エンコーダもインストールされている必要があります。
- 実行には[python3.6](https://www.python.org)以上の最新バージョンが望ましいです。
- This program is a wrapper program of [ffmpeg](https://ffmpeg.org/). Therefore, you must install the latest version of [ffmpeg](https://ffmpeg.org/) and greater than [python3.6](https://www.python.org)

## requirements

以下の外部モジュールが必要になるので`pip`を使って外部モジュールをインストールして下さい。
環境によっては権限の問題によりインストールが困難になる場合があるので、その場合は`--user`オプションを付与して下さい。

```
pip install -U pip setuptools [--user]
pip install opencv-python [--user]
```

### Windows

`ffmpeg.exe`が存在するディレクトリに**PATH**を通して下さい。

### Ubuntu

```bash
sudo apt install ffmpeg
```

### CentOS

`yum`からインストールした`ffmpeg`はバージョンがかなり古く、おそらく期待する動作をしないでしょう...。そのため、自身で`ffmpeg`と関連するコーデックをコンパイルしてインストールする必要があります。

## Usage

動画ファイルと同じディレクトリで`run.py`を実行して下さい。

```bash
> python run.py --help
>----------------------<
usage: run.py [-h] [-v VCODEC] [-a ACODEC] [--tag TAG] [--size SIZE]
              [--threads THREADS] [--fps FPS] [--bitrate BITRATE]
              [--pix_fmt PIX_FMT] [--segment_time SEGMENT_TIME] [--thumbnail]
              [--noaudio] [--hls] [-c]

You can use some arguments.

optional arguments:
  -h, --help            show this help message and exit
  -v VCODEC, --vcodec VCODEC
  -a ACODEC, --acodec ACODEC
  --tag TAG
  --size SIZE
  --threads THREADS
  --fps FPS
  --bitrate BITRATE
  --pix_fmt PIX_FMT
  --segment_time SEGMENT_TIME
  --thumbnail
  --noaudio
  --hls
  -c, -j, --concat
usage: run.py [-h] [-v VCODEC] [-a ACODEC] [--tag TAG] [--size SIZE]
>----------------------<
```

### デフォルトのパラメーター

```
'-v', '--vcodec', default='libx265'
'-a', '--acodec', default='copy',
'--tag', default='copy',  # libx265でエンコードする場合、hvc1に設定すると良いです。
'--size',　# デフォルトでは、元動画ファイルのheight, widthをセット。 # e.g. 1270x780, 720x480, hd720, hd480...
'--threads', default=2,  # エンコードに利用するcpuコア数。
'--fps', default=30,
'--bitrate', default=44100,
'--pix_fmt', default='yuv420p',
'--segment_time', default=10,
'--thumbnail'  # thumbnailを同時に生成する。
'--noaudio'  # 音声ファイルを無視する。
'--hls' m3u8形式の疑似ストリーミングファイルへと変換する。
'-c', '-j', '--concat' 動画の結合(不安定)
```

### e.g. h265形式へのエンコード

```bash
py run.py --tag hvc1
```

### e.g. hls形式へのエンコード

`hls`へのエンコードは何故か`libx265`コーデックを利用するとおかしな動作を起こすので、`libx264`を利用しています。

```bash
py run.py -v libx264 --hls
```

### e.g. h265形式へのエンコード + 動画サムネイルの生成

```bash
py run.py --tag hvc1 --thumbnail

```

## サークル紹介

### Operation KIWI

- サークル代表 kiwi
- [ 公式サイト](https://www.opskiwi.work/)
- [Twitter](https://twitter.com/Ops_kiwi/)
