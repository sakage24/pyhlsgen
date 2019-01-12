# pygenhls

This program converts video files of various formats quickly and easily into hls/m3u8 format.

This program is a wrapper program of [ffmpeg](https://ffmpeg.org/). Therefore, you must install the latest version of [ffmpeg](https://ffmpeg.org/) and greater than [python3.6](https://www.python.org).

## Usage

```bash
usage: run.py [-h] [-v VCODEC] [-a ACODEC] [--tag TAG] [--size SIZE]
[--threads THREADS] [--fps FPS] [--bitrate BITRATE]
[--pix_fmt PIX_FMT] [--segment_time SEGMENT_TIME] [--thumbnail]
[-c]
```

### * -> m3u8

1. Put in the source files in the same directory as the sctipts.
1. run script.
    - `py genhls.py`
    - run backgrounds
        - `nohup python3 genhls.py &`
1. `m3u8/YOUR_SOURCE_FILES` directory will be generated.

### * -> convert to other codecs

##### syntax

`py genhls.py "video_codec" "audio_codec(Optional)"`

#### example

##### convert to libx265(audio codec would copy.)

`py genhls.py libx265`

##### convert to libx265(audio codec would copy.)

`py genhls.py libx265 copy`

##### convert to libx264 and ac3 codecs.

`py genhls.py libx264 ac3`

## convert flow

- mp4(libx264) -> copy -> m3u8
- mp4(libx265) -> libx264 -> m3u8
- other codeces -> libx264 -> m3u8

## output

`./m3u8/YOUR_SOURCE__MOVIE_FILE__NAME/output.m3u8, stream-0000001.ts, ...`


## link

[Operation KIWI](https://www.kiwi-bird.xyz/)


I have been created [Hentai-Action-Games](http://www.dlsite.com/maniax/dlaf/=/link/work/aid/kiwibird/id/RJ205597.html).

