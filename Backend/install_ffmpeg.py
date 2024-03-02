import subprocess
# ระบุทางเข้าถึง FFmpeg ที่ติดตั้งไว้
ffmpeg_path = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"

# ตรวจสอบเวอร์ชันของ FFmpeg
subprocess.run([ffmpeg_path, "-version"])
