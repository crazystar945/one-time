# -*- coding: utf-8 -*-
"""Burn subtitles by setting cwd and using relative filename"""
import os, subprocess, sys

FFMPEG = r"D:\ENV\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
WORK_DIR = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出"
INPUT = "就这一次-V1.0.mp4"
SRT = "sub.srt"
OUTPUT = "就这一次-V1.0-带字幕.mp4"

# Verify files exist
for f in [os.path.join(WORK_DIR, INPUT), os.path.join(WORK_DIR, SRT)]:
    if not os.path.exists(f):
        print(f"ERROR: File not found: {f}")
        sys.exit(1)

print(f"Working dir: {WORK_DIR}")
print(f"Input: {INPUT}")
print(f"SRT: {SRT}")
print(f"Output: {OUTPUT}")

vf = (
    f"subtitles={SRT}"
    ":force_style="
    "'Fontname=Arial,"
    "FontSize=28,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,"
    "Bold=1,"
    "Outline=2,"
    "Shadow=1,"
    "Alignment=2,"
    "MarginV=40'"
)

cmd = [
    FFMPEG, "-y",
    "-i", INPUT,
    "-vf", vf,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "copy",
    OUTPUT
]

print("\nBurning subtitles (using relative path)...")
result = subprocess.run(cmd, capture_output=True, cwd=WORK_DIR)

if result.returncode == 0:
    out_path = os.path.join(WORK_DIR, OUTPUT)
    print("SUCCESS! Subtitles burned.")
    print(f"Output: {os.path.getsize(out_path)/1024/1024:.1f} MB")
else:
    print("FAILED!")
    err = result.stderr.decode('utf-8', errors='replace')
    print(err[-1500:])
