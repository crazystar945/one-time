# -*- coding: utf-8 -*-
"""Burn subtitles using moviepy - works around ffmpeg path bug"""
import os, sys

sys.path.insert(0, r"D:\ENV\python\Lib\site-packages")

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

FFMPEG = r"D:\ENV\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
change_settings({"FFMPEG_BINARY": FFMPEG})

INPUT = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出\就这一次-V1.0.mp4"
OUTPUT = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出\就这一次-V1.0-带字幕.mp4"

SUBTITLES = [
    (1.0, 4.5, "\u8c03\u67e5\u4eba\u5458\uff1a\u201cXX\u53d8\u7535\u7ad9\u90a3\u6b21\u68c0\u4fee\uff0c\u5907\u4ef6\u6570\u91cf\u662f\u4f60\u786e\u8ba4\u7684\u5427\uff1f\u201d"),
    (7.0, 10.0, "\u8d75\u5efa\u56fd\uff1a\u201c\u5e72\u68c0\u4fee\u7684\u4eba\uff0c\u4e0d\u80fd\u5acc\u9ebb\u70e6\u3002\u201d"),
    (11.5, 14.5, "\u8d75\u5efa\u56fd\uff1a\u201c\u6807\u51c6\u4e0d\u80fd\u6709\u4f8b\u5916\u3002\u201d"),
    (15.0, 18.0, "\u674e\u5f3a\uff1a\u201c\u8d75\u5e08\u5085\uff0c\u8f9b\u82e6\u4e00\u5929\u4e86\u3002\u559d\u53e3\u6c34\u3002\u201d"),
    (19.0, 21.0, "\u8d75\u5efa\u56fd\uff1a\u201c\u8c22\u8c22\u3002\u201d"),
    (22.0, 25.5, "\u674e\u5f3a\uff1a\u201c\u8fd9\u6279\u5907\u4ef6\u4ee5\u540e\u80af\u5b9a\u80fd\u7528\u3002\u5c31\u8fd9\u4e00\u6b21\u3002\u201d"),
    (27.0, 28.5, "\u2026\u2026"),
    (34.0, 37.5, "\u5c0f\u5468\uff1a\u201c\u5e08\u5085\uff0c\u4f60\u4ee5\u524d\u6559\u6211\u7684\u89c4\u77e9\uff0c\u8fd8\u7b97\u6570\u5417\uff1f\u201d"),
    (39.0, 42.0, "\u5973\u513f\uff1a\u201c\u7238\u7238\uff0c\u4f60\u4e0d\u662f\u8bf4\u505a\u4eba\u8981\u8bda\u5b9e\u5417\uff1f\u201d"),
    (43.5, 46.5, "\u5973\u513f\uff1a\u201c\u90a3\u4f60\u5de5\u4f5c\u7684\u65f6\u5019\uff0c\u4e5f\u4e00\u76f4\u8bf4\u771f\u8bdd\u5417\uff1f\u201d"),
    (53.0, 57.0, "\u8c03\u67e5\u4eba\u5458\uff1a\u201c\u4f60\u6ca1\u6709\u62ff\u94b1\u3002\u4f46\u5907\u4ef6\u6d88\u8017\u786e\u8ba4\u662f\u4f60\u7684\u804c\u8d23\u3002\u4f8e\u4e86\u8def\u3002\u201d"),
    (58.5, 62.5, "\u8c03\u67e5\u4eba\u5458\uff1a\u201c\u4fdd\u62a4\u7684\u4e0d\u662f\u4e00\u4e2a\u670b\u53cb\u3002\u4f60\u5f71\u54cd\u7684\u662f\u6240\u6709\u9075\u5b88\u89c4\u5219\u7684\u4eba\u3002\u201d"),
    (64.0, 68.0, "\u8d75\u5efa\u56fd\uff1a\u201c\u6211\u6ca1\u6709\u62ff\u94b1\u2026\u2026\u4f46\u6211\u5229\u7528\u5c97\u4f4d\u4fbf\u5229\uff0c\u5f71\u54cd\u4e86\u516c\u6b63\u3002\u201d"),
    (72.0, 74.5, "\u59d1\u59d1\u4eba\u5458\uff1a\u201c\u8d75\u5e08\u5085\uff0c\u4ee5\u524d\u2026\u2026\u201d"),
    (75.5, 79.0, "\u8d75\u5efa\u56fd\uff1a\u201c\u4ee5\u524d\u7684\u9519\u8bef\uff0c\u4e0d\u80fd\u6210\u4e3a\u4eca\u5929\u7684\u89c4\u77e9\u3002\u201d"),
    (80.5, 84.0, "\u8d75\u5efa\u56fd\uff1a\u201c\u5de5\u4f5c\u4e0a\u7684\u4e8b\u60c5\uff0c\u6ca1\u6700\u719f\u4eba\u3002\u201d"),
    (88.0, 95.0, "\u6ca1\u6709\u4e00\u4e2a\u4eba\u89c9\u5f97\u81ea\u5df1\u8150\u8d25\u3002\n\u4e8e\u662f\uff0c\u8150\u8d25\u53d1\u751f\u4e86\u3002"),
    (96.0, 104.0, "\u8150\u8d25\u5f88\u5c11\u5f00\u59cb\u4e8e\u4e00\u6b21\u5de8\u5927\u7684\u9519\u8bef\u3002\n\u66f4\u591a\u65f6\u5019\uff0c\u5f00\u59cb\u4e8e\u4e00\u53e5\uff1a\n\u201c\u5c31\u8fd9\u4e00\u6b21\u3002\u201d"),
]

print("Loading video...")
video = VideoFileClip(INPUT)
w, h = video.size
print(f"Video size: {w}x{h}, Duration: {video.duration:.1f}s")

print("Creating subtitle clips...")
subtitle_clips = []
for idx, (start, end, text) in enumerate(SUBTITLES):
    if start >= video.duration:
        continue
    txt_clip = (
        TextClip(
            text,
            fontsize=28,
            font="SimHei",
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(w * 0.85), None),
            align="center",
        )
        .set_position(("center", h * 0.82))
        .set_start(start)
        .set_end(min(end, video.duration))
    )
    subtitle_clips.append(txt_clip)
    print(f"  [{idx+1}/{len(SUBTITLES)}] {start:.1f}-{end:.1f}s")

print("Compositing...")
final = CompositeVideoClip([video] + subtitle_clips)

print(f"Writing output to {OUTPUT}...")
final.write_videofile(
    OUTPUT,
    codec="libx264",
    audio_codec="aac",
    fps=24,
    preset="medium",
    threads=4,
    verbose=False,
    logger=None
)

print("\nDONE!")
print(f"Output: {os.path.getsize(OUTPUT)/1024/1024:.1f} MB")
video.close()
final.close()
