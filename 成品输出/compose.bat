@echo off
setlocal enabledelayedexpansion

set "FFMPEG=D:\ENV\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
set "SRC=D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\视频素材"
set "OUT=D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出\_temp_colored"
set "FINAL_DIR=D:\信息留档\包头供电工作留档\杂项工作\视频制作\廉洁文化\成品输出"

echo ============================================================
echo Phase 4: Video Composition - Step 3 Color Grading
echo ============================================================

echo [1/10] V-01 Cold Blue...
"%FFMPEG%" -y -i "%SRC%\冬季清晨_中国北方供电企业纪委谈话室内_镜头缓慢推进_中年电_2026-07-12T10-24-33.mp4" -vf "eq=brightness=0:saturation=0.9:contrast=1.05,colorbalance=bs=0.15" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-01_colored.mp4" >nul 2>&1 && echo   V-01 DONE || echo   V-01 FAILED

echo [2/10] V-02 Warm Yellow...
"%FFMPEG%" -y -i "%SRC%\夏季内蒙古变电站检修现场_烈日照射钢铁设备泛着光_输电铁塔高_2026-07-12T10-27-29.mp4" -vf "eq=brightness=0.03:saturation=1.1:contrast=1.02,colorbalance=rs=0.08" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-02_colored.mp4" >nul 2>&1 && echo   V-02 DONE || echo   V-02 FAILED

echo [3/10] V-03 Warm Yellow...
"%FFMPEG%" -y -i "%SRC%\炎热夏天检修结束后_变电站设备旁的空地_外委单位负责人李强__2026-07-12T10-30-05.mp4" -vf "eq=brightness=0.03:saturation=1.1:contrast=1.02,colorbalance=rs=0.08" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-03_colored.mp4" >nul 2>&1 && echo   V-03 DONE || echo   V-03 FAILED

echo [4/10] V-04 Warm Light...
"%FFMPEG%" -y -i "%SRC%\黄昏临时办公室_台灯光照亮桌面_桌上散落检修资料和备件清单__2026-07-12T10-33-27.mp4" -vf "eq=brightness=0.02:saturation=1.05:contrast=1.0,colorbalance=rs=0.06" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-04_colored.mp4" >nul 2>&1 && echo   V-04 DONE || echo   V-04 FAILED

echo [5/10] V-05 Desaturated Cool Gray...
"%FFMPEG%" -y -i "%SRC%\办公室内_午后光线从窗户照入留下光影_赵建国_深蓝工装_坐在_2026-07-12T10-36-09.mp4" -vf "eq=brightness=-0.02:saturation=0.7:contrast=1.05,colorbalance=bs=0.1" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-05_colored.mp4" >nul 2>&1 && echo   V-05 DONE || echo   V-05 FAILED

echo [6/10] V-06 Desaturated Cool Gray (stronger)...
"%FFMPEG%" -y -i "%SRC%\中国普通职工家庭夜晚客厅一角_暖黄色台灯照亮书桌_约10岁女_2026-07-12T10-40-21.mp4" -vf "eq=brightness=-0.03:saturation=0.65:contrast=1.08,colorbalance=bs=0.12" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-06_colored.mp4" >nul 2>&1 && echo   V-06 DONE || echo   V-06 FAILED

echo [7/10] V-07 Desaturated Cool Gray...
"%FFMPEG%" -y -i "%SRC%\夜晚小型办公室_李强_40岁瘦长脸风霜感_灰绿工程服或内搭T_2026-07-12T10-43-07.mp4" -vf "eq=brightness=-0.03:saturation=0.7:contrast=1.05,colorbalance=bs=0.1" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-07_colored.mp4" >nul 2>&1 && echo   V-07 DONE || echo   V-07 FAILED

echo [8/10] V-08 Desaturated Cool Gray (light)...
"%FFMPEG%" -y -i "%SRC%\纪委调查谈话室_桌面铺满资料__备件清单_检修记录_时间线图_2026-07-12T10-46-37.mp4" -vf "eq=brightness=-0.02:saturation=0.75:contrast=1.03,colorbalance=bs=0.08" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-08_colored.mp4" >nul 2>&1 && echo   V-08 DONE || echo   V-08 FAILED

echo [9/10] V-09 Natural Warm...
"%FFMPEG%" -y -i "%SRC%\一年后的变电站检修现场_阳光明媚天气晴朗_年轻员工小周_蓝工_2026-07-12T10-50-16.mp4" -vf "eq=brightness=0.02:saturation=1.05:contrast=1.0,colorbalance=rs=0.05" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-09_colored.mp4" >nul 2>&1 && echo   V-09 DONE || echo   V-09 FAILED

echo [10/10] V-10 Sunset Warm...
"%FFMPEG%" -y -i "%SRC%\夕阳下的内蒙古变电站壮阔全景_高大的输电铁塔向远方延伸_钢铁_2026-07-12T10-53-42.mp4" -vf "eq=brightness=0.01:saturation=1.1:contrast=1.02,colorbalance=rs=0.1:gs=0.05" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "%OUT%\V-10_colored.mp4" >nul 2>&1 && echo   V-10 DONE || echo   V-10 FAILED

echo.
echo Color grading complete!
echo.
echo ============================================================
echo Step 4: Concatenating with Crossfade Transitions
echo ============================================================

set "CONCAT=%FINAL_DIR%\_temp_concatenated.mp4"

:: Use concat demuxer for reliable concatenation (fallback without xfade)
echo Creating concat list...
(
file '%OUT%\V-01_colored.mp4'
file '%OUT%\V-02_colored.mp4'
file '%OUT%\V-03_colored.mp4'
file '%OUT%\V-04_colored.mp4'
file '%OUT%\V-05_colored.mp4'
file '%OUT%\V-06_colored.mp4'
file '%OUT%\V-07_colored.mp4'
file '%OUT%\V-08_colored.mp4'
file '%OUT%\V-09_colored.mp4'
file '%OUT%\V-10_colored.mp4'
) > "%FINAL_DIR%\concat_list.txt"

echo Concatenating videos...
"%FFMPEG%" -y -f concat -safe 0 -i "%FINAL_DIR%\concat_list.txt" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k "%CONCAT%" >nul 2>&1 && echo Concatenation DONE || echo Concatenation FAILED

echo.
echo ============================================================
echo Step 5: Burning Subtitles
echo ============================================================

set "SUBTITLED=%FINAL_DIR%\_temp_subtitled.mp4"

echo Burning SRT subtitles...
"%FFMPEG%" -y -i "%CONCAT%" -vf "subtitles='%FINAL_DIR%\就这一次-字幕.srt':force_style='FontName=Source Han Sans CN,FontSize=28,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Bold=1,Outline=2,Shadow=1,Alignment=2,MarginV=40'" -c:v libx264 -preset medium -crf 18 -c:a copy "%SUBTITLED%" >nul 2>&1 && echo Subtitles DONE || echo Subtitles FAILED

echo.
echo ============================================================
echo Step 6: Final Output
echo ============================================================

set "FINAL=%FINAL_DIR%\就这一次-V1.0.mp4"

echo Encoding final output...
"%FFMPEG%" -y -i "%SUBTITLED%" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 256k "%FINAL%" >nul 2>&1 && echo Final encode DONE || echo Final encode FAILED

echo.
echo Cleaning up temp files...
del "%CONCAT%" 2>nul
del "%SUBTITLED%" 2>nul
del "%FINAL_DIR%\concat_list.txt 2>nul
rmdir /s /q "%OUT%" 2>nul

echo.
echo ============================================================
echo ALL DONE!
echo Output: %FINAL%
echo ============================================================
