#!/bin/sh

# extract h264 video track only to .mp4
gpac -i bbb.mp4 @#CodecID=avc -o bbb.avc.mp4

# convert audio track to aac mono 48kHz
gpac -graph -i bbb.mp4 resample:osr=48k:och=1 ffenc:c=aac @ -o bbb.mono.mp4
