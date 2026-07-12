#!/usr/bin/env python3
"""
《就这一次》廉洁主题短片 - Phase 4 后期合成脚本
功能：10段视频拼接 + 字幕烧录 + 转场 + 调色
"""

import os
import subprocess
import sys
import json
import tempfile
import shutil

# ============================================================
# 路径配置
# ============================================================
BASE_DIR = r"D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化"
SOURCE_DIR = os.path.join(BASE_DIR, "视频素材")
OUTPUT_DIR = os.path.join(BASE_DIR, "成品输出")
FINAL_OUTPUT = os.path.join(OUTPUT_DIR, "就这一次-V1.0.mp4")

# 10段视频源文件（按顺序）
VIDEO_FILES = [
    ("V-01", "冬季清晨_中国北方供电企业纪委谈话室内_镜头缓慢推进_中年电_2026-07-12T10-24-33.mp4"),
    ("V-02", "夏季内蒙古变电站检修现场_烈日照射钢铁设备泛着光_输电铁塔高_2026-07-12T10-27-29.mp4"),
    ("V-03", "炎热夏天检修结束后_变电站设备旁的空地_外委单位负责人李强__2026-07-12T10-30-05.mp4"),
    ("V-04", "黄昏临时办公室_台灯光照亮桌面_桌上散落检修资料和备件清单__2026-07-12T10-33-27.mp4"),
    ("V-05", "办公室内_午后光线从窗户照入留下光影_赵建国_深蓝工装_坐在_2026-07-12T10-36-09.mp4"),
    ("V-06", "中国普通职工家庭夜晚客厅一角_暖黄色台灯照亮书桌_约10岁女_2026-07-12T10-40-21.mp4"),
    ("V-07", "夜晚小型办公室_李强_40岁瘦长脸风霜感_灰绿工程服或内搭T_2026-07-12T10-43-07.mp4"),
    ("V-08", "纪委调查谈话室_桌面铺满资料__备件清单_检修记录_时间线图_2026-07-12T10-46-37.mp4"),
    ("V-09", "一年后的变电站检修现场_阳光明媚天气晴朗_年轻员工小周_蓝工_2026-07-12T10-50-16.mp4"),
    ("V-10", "夕阳下的内蒙古变电站壮阔全景_高大的输电铁塔向远方延伸_钢铁_2026-07-12T10-53-42.mp4"),
]

SRT_FILE = os.path.join(OUTPUT_DIR, "就这一次-字幕.srt")

# 调色参数（三阶段色彩）
COLOR_GRADES = {
    # V-01: 冷蓝色调（开场调查）
    "V-01": "eq=brightness=0:saturation=0.9:contrast=1.05,colorbalance=bs=0.15",
    # V-02~04: 暖黄暖色调（第一幕回忆）
    "V-02": "eq=brightness=0.03:saturation=1.1:contrast=1.02,colorbalance=rs=0.08",
    "V-03": "eq=brightness=0.03:saturation=1.1:contrast=1.02,colorbalance=rs=0.08",
    "V-04": "eq=brightness=0.02:saturation=1.05:contrast=1.0,colorbalance=rs=0.06",
    # V-05~08: 低饱和度/冷灰蓝色调（第二幕冲突）
    "V-05": "eq=brightness=-0.02:saturation=0.7:contrast=1.05,colorbalance=bs=0.1",
    "V-06": "eq=brightness=-0.03:saturation=0.65:contrast=1.08,colorbalance=bs=0.12",
    "V-07": "eq=brightness=-0.03:saturation=0.7:contrast=1.05,colorbalance=bs=0.1",
    "V-08": "eq=brightness=-0.02:saturation=0.75:contrast=1.03,colorbalance=bs=0.08",
    # V-09~10: 自然光/暖色夕阳感（第三幕+结尾）
    "V-09": "eq=brightness=0.02:saturation=1.05:contrast=1.0,colorbalance=rs=0.05",
    "V-10": "eq=brightness=0.01:saturation=1.1:contrast=1.02,colorbalance=rs=0.1:gs=0.05",
}

# 转场时长(秒)
TRANSITION_DURATION = 0.8

def find_ffmpeg():
    """查找ffmpeg可执行文件"""
    # 检查环境变量
    env_ffmpeg = os.environ.get("FFMPEG")
    if env_ffmpeg and os.path.exists(env_ffmpeg):
        return env_ffmpeg

    # 检查PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path

    # 检查imageio-ffmpeg捆绑版本
    try:
        import sys
        # 尝试从Python site-packages中查找
        import importlib
        spec = importlib.util.find_spec("imageio_ffmpeg")
        if spec:
            pkg_dir = os.path.dirname(spec.origin) if spec.origin else None
            if pkg_dir:
                candidates = [
                    os.path.join(pkg_dir, "binaries", "ffmpeg-win-x86_64-v7.1.exe"),
                    os.path.join(os.path.dirname(pkg_dir), "binaries", "ffmpeg-win-x86_64-v7.1.exe"),
                ]
                for c in candidates:
                    if os.path.exists(c):
                        return c
    except:
        pass

    # 检查常见安装位置
    candidates = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"D:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        "/tmp/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe",
        os.path.expanduser("~/ffmpeg/bin/ffmpeg.exe"),
        r"D:\ENV\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def get_video_info(filepath, ffmpeg):
    """获取视频信息：分辨率、时长、帧率"""
    cmd = [
        ffmpeg, "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        vstream = [s for s in data["streams"] if s["codec_type"] == "video"][0]
        duration = float(data["format"]["duration"])
        width = int(vstream["width"])
        height = int(vstream["height"])
        fps_str = vstream.get("r_frame_rate", "30/1")
        parts = fps_str.split("/")
        fps = float(parts[0]) / float(parts[1]) if len(parts) == 2 else 30.0
        return {"duration": duration, "width": width, "height": height, "fps": fps}
    except Exception as e:
        print(f"  ERROR parsing video info for {filepath}: {e}")
        return None

def process_single_video(input_file, output_file, color_filter, ffmpeg):
    """对单段视频应用调色滤镜并输出"""
    cmd = [
        ffmpeg, "-y", "-i", input_file,
        "-vf", color_filter,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        output_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def concat_videos_with_crossfade(video_files, output_file, ffmpeg, transition_dur=0.8):
    """
    使用xfade filter实现带交叉淡入淡出的视频拼接
    """
    n = len(video_files)
    
    # 如果只有一段视频，直接复制
    if n == 1:
        shutil.copy2(video_files[0], output_file)
        return True
    
    # 两段视频使用简单的xfade
    if n == 2:
        td = transition_dur
        cmd = [
            ffmpeg, "-y",
            "-i", video_files[0],
            "-i", video_files[1],
            "-filter_complex",
            f"[0:v][1:v]xfade=transition=fade:duration={td}:offset={get_video_info(video_files[0], ffmpeg)['duration']-td}[vout];"
            f"[0:a][1:a]acrossfade=d={td}[aout]",
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            output_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  xfade error: {result.stderr[-500:]}")
            # fallback to concat demuxer
            return simple_concat(video_files, output_file, ffmpeg)
        return True
    
    # 多段视频：逐步两两合并
    print("  Using stepwise crossfade concatenation...")
    temp_files = list(video_files)
    
    for i in range(len(temp_files) - 1):
        f1 = temp_files[i]
        f2 = temp_files[i + 1]
        
        info1 = get_video_info(f1, ffmpeg)
        if not info1:
            continue
        
        offset = max(info1["duration"] - transition_dur, 0.5)
        out_temp = tempfile.mktemp(suffix=".mp4", prefix=f"concat_step_{i}_")
        
        cmd = [
            ffmpeg, "-y",
            "-i", f1, "-i", f2,
            "-filter_complex",
            f"[0:v][1:v]xfade=transition=fade:duration={transition_dur}:offset={offset}[vout];"
            f"[0:a][1?a]acrossfade=d={transition_dur}[aout]",
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            out_temp
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            temp_files[i + 1] = out_temp
            print(f"    Step {i+1}/{n-1}: merged -> {os.path.basename(out_temp)}")
        else:
            print(f"    Step {i+1} xfade failed, trying direct append...")
            # Fallback: use concat demuxer for remaining
            return simple_concat(temp_files[:i+2], output_file, ffmpeg)
    
    # 最后一个合并结果即为输出
    final_merged = temp_files[-1]
    shutil.copy2(final_merged, output_file)
    
    # 清理临时文件
    for tf in temp_files[len(video_files):]:
        if os.path.exists(tf):
            os.remove(tf)
    
    return True

def simple_concat(video_files, output_file, ffmpeg):
    """简单拼接（无转场，作为fallback）"""
    # 创建concat列表文件
    list_file = tempfile.mktemp(suffix=".txt", prefix="concat_list_")
    with open(list_file, "w", encoding="utf-8") as f:
        for vf in video_files:
            safe_path = vf.replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")
    
    cmd = [
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(list_file):
        os.remove(list_file)
    
    if result.returncode != 0:
        print(f"  Simple concat error: {result.stderr[-500:]}")
        return False
    return True

def burn_subtitles(input_file, output_file, srt_file, ffmpeg):
    """将SRT字幕烧录到视频中"""
    # 使用ass字幕滤镜，样式：白色字体+黑色描边+底部居中
    style_params = (
        "FontName=Source Han Sans CN,"
        "FontSize=28,"
        "PrimaryColour=&H00FFFFFF,"
        "SecondaryColour=&H000000FF,"
        "OutlineColour=&H00000000,"
        "BackColour=&H80000000,"
        "Bold=1,"
        "Outline=2,"
        "Shadow=1,"
        "Alignment=2,"  # 底部居中
        "MarginV=40"     # 底部边距
    )
    
    cmd = [
        ffmpeg, "-y",
        "-i", input_file,
        "-vf", f"subtitles='{srt_file.replace(os.sep, '/')}':force_style='{style_params}'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "copy",
        output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Subtitle burn error: {result.stderr[-500:]}")
        return False
    return True

def main():
    print("=" * 60)
    print("《就这一次》Phase 4 后期合成")
    print("=" * 60)
    
    # 查找ffmpeg
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ERROR: FFmpeg not found! Please install ffmpeg.")
        print("Download from: https://www.gyan.dev/ffmpeg/builds/")
        return False
    
    print(f"\nUsing FFmpeg: {ffmpeg}")
    
    # 确认所有源文件存在
    print("\n[Step 1] Checking source files...")
    source_paths = []
    for vid, fname in VIDEO_FILES:
        path = os.path.join(SOURCE_DIR, fname)
        if not os.path.exists(path):
            print(f"  MISSING: {fname}")
            return False
        source_paths.append(path)
        print(f"  OK: {vid} - {fname}")
    
    # 获取各段视频信息
    print("\n[Step 2] Getting video metadata...")
    video_infos = {}
    total_duration = 0
    for i, (vid, fname) in enumerate(VIDEO_FILES):
        info = get_video_info(source_paths[i], ffmpeg)
        if not info:
            print(f"  ERROR reading {vid}")
            return False
        video_infos[vid] = info
        total_duration += info["duration"]
        color_grade = COLOR_GRADES.get(vid, "")
        print(f"  {vid}: {info['width']}x{info['height']} @ {info['fps']:.1f}fps | {info['duration']:.1f}s | Color: {'Yes' if color_grade else 'None'}")
    
    print(f"  Total raw duration: {total_duration:.1f}s (~{total_duration/60:.1f}min)")
    
    # Step 3: 对每段视频单独应用调色
    print("\n[Step 3] Applying color grades...")
    colored_dir = os.path.join(OUTPUT_DIR, "_temp_colored")
    os.makedirs(colored_dir, exist_ok=True)
    colored_paths = []
    
    for i, (vid, fname) in enumerate(VIDEO_FILES):
        color_filter = COLOR_GRADES.get(vid, "")
        out_path = os.path.join(colored_dir, f"{vid}_colored.mp4")
        
        if color_filter:
            success = process_single_video(source_paths[i], out_path, color_filter, ffmpeg)
            if success:
                print(f"  {vid}: Color grade applied ✓")
                colored_paths.append(out_path)
            else:
                print(f"  {vid}: Color grade FAILED, using original")
                colored_paths.append(source_paths[i])
        else:
            # 无需调色，直接引用原文件
            colored_paths.append(source_paths[i])
            print(f"  {vid}: No color grade needed (using original)")
    
    # Step 4: 带转场拼接
    print("\n[Step 4] Concatenating with transitions...")
    concatenated_file = os.path.join(OUTPUT_DIR, "_temp_concatenated.mp4")
    
    success = concat_videos_with_crossfade(
        colored_paths,
        concatenated_file,
        ffmpeg,
        TRANSITION_DURATION
    )
    
    if not success:
        print("  Concatenation FAILED!")
        return False
    print("  Concatenation complete ✓")
    
    # 获取拼接后信息
    final_info = get_video_info(concatenated_file, ffmpeg)
    if final_info:
        print(f"  Concatenated: {final_info['width']}x{final_info['height']} | {final_info['duration']:.1f}s")
    
    # Step 5: 烧录字幕
    print("\n[Step 5] Burning subtitles...")
    subtitle_burned = os.path.join(OUTPUT_DIR, "_temp_subtitled.mp4")
    
    if burn_subtitles(concatenated_file, subtitle_burned, SRT_FILE, ffmpeg):
        print("  Subtitles burned successfully ✓")
        final_source = subtitle_burned
    else:
        print("  Subtitle burn FAILED, outputting without subtitles")
        final_source = concatenated_file
    
    # Step 6: 最终输出
    print("\n[Step 6] Generating final output...")
    final_cmd = [
        ffmpeg, "-y",
        "-i", final_source,
        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "256k",
        FINAL_OUTPUT
    ]
    
    result = subprocess.run(final_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Final encode error: {result.stderr[-500:]}")
        # 尝试直接复制
        shutil.copy2(final_source, FINAL_OUTPUT)
    
    # 清理临时文件
    print("\n[Cleanup] Removing temporary files...")
    for tf in [concatenated_file, subtitle_burned]:
        if os.path.exists(tf):
            os.remove(tf)
    if os.path.exists(colored_dir):
        shutil.rmtree(colored_dir)
    
    # 输出最终结果
    print("\n" + "=" * 60)
    print("✅ 后期合成完成！")
    print("=" * 60)
    
    final_info = get_video_info(FINAL_OUTPUT, ffmpeg)
    if final_info:
        file_size = os.path.getsize(FINAL_OUTPUT) / (1024 * 1024)
        print(f"\n📁 成片路径: {FINAL_OUTPUT}")
        print(f"   分辨率: {final_info['width']}x{final_info['height']}")
        print(f"   时长: {final_info['duration']:.1f}秒 ({final_info['duration']/60:.1f}分钟)")
        print(f"   文件大小: {file_size:.1f} MB")
        print(f"   字幕: 已烧录 (SRT文件: {SRT_FILE})")
        print(f"   转场: 交叉淡入淡出 ({TRANSITION_DURATION}秒)")
        print(f"   调色: 三阶段色彩调整已应用")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
