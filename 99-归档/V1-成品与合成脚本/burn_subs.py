#!/usr/bin/env python3
"""Burn subtitles into video with proper path handling"""
import os, subprocess, sys

FFMPEG = r"D:\ENV\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
INPUT = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出\就这一次-V1.0.mp4"
OUTPUT = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出\就这一次-V1.0-带字幕.mp4"
SRT = r"D:\subtitles.srt"

# Verify files exist
for f in [INPUT, SRT]:
    if not os.path.exists(f):
        print(f"ERROR: File not found: {f}")
        sys.exit(1)

print(f"Input: {os.path.getsize(INPUT)/1024/1024:.1f} MB")
print(f"SRT: {SRT}")
print(f"Output: {OUTPUT}")

# Build command
vf = (
    f"subtitles='{SRT}'"
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

print("\nBurning subtitles...")
result = subprocess.run(cmd, capture_output=True)

if result.returncode == 0:
    print("SUCCESS! Subtitles burned.")
    print(f"Output: {os.path.getsize(OUTPUT)/1024/1024:.1f} MB")
else:
    print("FAILED!")
    print(result.stderr.decode('utf-8', errors='replace')[-1000:])
