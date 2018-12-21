# pygenhls

This program converts video files of various formats quickly and easily into hls/m3u8 format.

This program is a wrapper program of [ffmpeg](https://ffmpeg.org/). Therefore, you must install the latest version of [ffmpeg](https://ffmpeg.org/) and greater than [python3.6](https://www.python.org).

## Usage

1. Put in the source files in the same directory as the sctipts.
1. run script.
    - `py genhls.py`
    - run backgrounds
        - `nohup python3 genhls.py &`
1. `m3u8/YOUR_SOURCE_FILES` directory will be generated.

## convert flow

- mp4(libx264) -> copy -> m3u8
- mp4(libx265) -> libx264 -> m3u8
- other codeces -> libx264 -> m3u8

## output

`./m3u8/YOUR_SOURCE__MOVIE_FILE__NAME/output.m3u8, stream-0000001.ts, ...`


## link

[Operation KIWI](https://www.kiwi-bird.xyz/)


I have been created [Hentai-Action-Games](http://www.dlsite.com/maniax/dlaf/=/link/work/aid/kiwibird/id/RJ205597.html).

