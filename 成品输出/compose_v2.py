#!/usr/bin/env python3
"""Direct ffmpeg execution for video composition - handles Unicode paths"""
import os, subprocess, shutil, sys, tempfile

FFMPEG = r"D:\ENV\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
SRC = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\视频素材"
OUT_DIR = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出"
TEMP_COLOR = os.path.join(OUT_DIR, "_temp_colored")
FINAL_OUT = os.path.join(OUT_DIR, "就这一次-V1.0.mp4")
SRT_FILE = os.path.join(OUT_DIR, "就这一次-字幕.srt")

os.makedirs(TEMP_COLOR, exist_ok=True)

# Source files in order
FILES = [
    ("V-01", "冬季清晨_中国北方供电企业纪委谈话室内_镜头缓慢推进_中年电_2026-07-12T10-24-33.mp4", "eq=brightness=0:saturation=0.9:contrast=1.05,colorbalance=bs=0.15"),
    ("V-02", "夏季内蒙古变电站检修现场_烈日照射钢铁设备泛着光_输电铁塔高_2026-07-12T10-27-29.mp4", "eq=brightness=0.03:saturation=1.1:contrast=1.02,colorbalance=rs=0.08"),
    ("V-03", "炎热夏天检修结束后_变电站设备旁的空地_外委单位负责人李强__2026-07-12T10-30-05.mp4", "eq=brightness=0.03:saturation=1.1:contrast=1.02,colorbalance=rs=0.08"),
    ("V-04", "黄昏临时办公室_台灯光照亮桌面_桌上散落检修资料和备件清单__2026-07-12T10-33-27.mp4", "eq=brightness=0.02:saturation=1.05:contrast=1.0,colorbalance=rs=0.06"),
    ("V-05", "办公室内_午后光线从窗户照入留下光影_赵建国_深蓝工装_坐在_2026-07-12T10-36-09.mp4", "eq=brightness=-0.02:saturation=0.7:contrast=1.05,colorbalance=bs=0.1"),
    ("V-06", "中国普通职工家庭夜晚客厅一角_暖黄色台灯照亮书桌_约10岁女_2026-07-12T10-40-21.mp4", "eq=brightness=-0.03:saturation=0.65:contrast=1.08,colorbalance=bs=0.12"),
    ("V-07", "夜晚小型办公室_李强_40岁瘦长脸风霜感_灰绿工程服或内搭T_2026-07-12T10-43-07.mp4", "eq=brightness=-0.03:saturation=0.7:contrast=1.05,colorbalance=bs=0.1"),
    ("V-08", "纪委调查谈话室_桌面铺满资料__备件清单_检修记录_时间线图_2026-07-12T10-46-37.mp4", "eq=brightness=-0.02:saturation=0.75:contrast=1.03,colorbalance=bs=0.08"),
    ("V-09", "一年后的变电站检修现场_阳光明媚天气晴朗_年轻员工小周_蓝工_2026-07-12T10-50-16.mp4", "eq=brightness=0.02:saturation=1.05:contrast=1.0,colorbalance=rs=0.05"),
    ("V-10", "夕阳下的内蒙古变电站壮阔全景_高大的输电铁塔向远方延伸_钢铁_2026-07-12T10-53-42.mp4", "eq=brightness=0.01:saturation=1.1:contrast=1.02,colorbalance=rs=0.1:gs=0.05"),
]

def run_ffmpeg(cmd_args, description):
    """Run ffmpeg command and return success"""
    full_cmd = [FFMPEG] + cmd_args
    print(f"  {description}...", end=" ", flush=True)
    result = subprocess.run(full_cmd, capture_output=True)
    if result.returncode == 0:
        print("OK")
        return True
    else:
        print(f"FAILED")
        err = result.stderr.decode('utf-8', errors='replace')[-300:]
        print(f"    Error: {err}")
        return False

print("=" * 60)
print("Phase 4 Video Composition")
print("=" * 60)
print(f"FFmpeg: {FFMPEG}")
print()

# Step 1: Color grade all videos
print("[Step 1/4] Color grading (10 clips)...")
colored_files = []
for i, (vid, fname, vfilter) in enumerate(FILES):
    src_path = os.path.join(SRC, fname)
    out_path = os.path.join(TEMP_COLOR, f"{vid}_colored.mp4")
    
    success = run_ffmpeg([
        "-y", "-i", src_path,
        "-vf", vfilter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ], f"[{i+1}/10] {vid}")
    
    if success:
        colored_files.append(out_path)
    else:
        # Fallback: use original
        colored_files.append(src_path)
        print(f"    Using original for {vid}")

print()
colored_count = sum(1 for f in colored_files if "_colored" in f)
print(f"  Color graded: {colored_count}/10")

# Step 2: Concatenate
print("\n[Step 2/4] Concatenating videos...")
concat_file = os.path.join(OUT_DIR, "_temp_concat.mp4")
list_file = os.path.join(OUT_DIR, "_concat_list.txt")

with open(list_file, "w", encoding="utf-8") as f:
    for cf in colored_files:
        f.write(f"file '{cf}'\n")

success = run_ffmpeg([
    "-y",
    "-f", "concat", "-safe", "0",
    "-i", list_file,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    concat_file
], "Concatenation")

if not success:
    print("  CRITICAL: Concatenation failed!")
    sys.exit(1)

# Step 3: Burn subtitles
print("\n[Step 3/4] Burning subtitles...")
subtitled_file = os.path.join(OUT_DIR, "_temp_subtitled.mp4")

style = (
    "FontName=Source Han Sans CN,"
    "FontSize=28,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,"
    "Bold=1,"
    "Outline=2,"
    "Shadow=1,"
    "Alignment=2,"
    "MarginV=40"
)

success = run_ffmpeg([
    "-y",
    "-i", concat_file,
    "-vf", f"subtitles='{SRT_FILE}':force_style='{style}'",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "copy",
    subtitled_file
], "Subtitle burn")

if not success:
    print("  WARNING: Subtitle burn failed! Outputting without subtitles.")
    subtitled_file = concat_file

# Step 4: Final encode
print("\n[Step 4/4] Final encoding...")
success = run_ffmpeg([
    "-y",
    "-i", subtitled_file,
    "-c:v", "libx264", "-preset", "slow", "-crf", "17",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    "-c:a", "aac", "-b:a", "256k",
    FINAL_OUT
], "Final output")

if not success:
    print("  Final encode failed, copying intermediate file...")
    shutil.copy2(subtitled_file, FINAL_OUT)

# Cleanup
print("\n[Cleanup] Removing temp files...")
for tf in [list_file, concat_file]:
    if os.path.exists(tf):
        os.remove(tf)
if subtitled_file != concat_file and os.path.exists(subtitled_file):
    os.remove(subtitled_file)
if os.path.exists(TEMP_COLOR):
    shutil.rmtree(TEMP_COLOR)

# Result
print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)
if os.path.exists(FINAL_OUT):
    size_mb = os.path.getsize(FINAL_OUT) / (1024*1024)
    print(f"\nOutput: {FINAL_OUT}")
    print(f"Size: {size_mb:.1f} MB")
else:
    print("\nERROR: Output file not created!")
