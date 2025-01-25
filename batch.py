import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from xp3 import XP3


def process_audio_files(folder: Path, speed: float):
    """处理文件夹中的所有 .ogg 文件"""
    for ogg_file in folder.rglob("*.ogg"):
        output_file = ogg_file.parent / f"temp_{ogg_file.name}"

        # 使用 ffmpeg 加速音频但不改变音高
        cmd = [
            "ffmpeg",
            "-i",
            str(ogg_file),
            "-filter:a",
            f"atempo={speed}",
            "-vn",
            str(output_file),
            "-y",  # 覆盖已存在的文件
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            # 替换原文件
            output_file.replace(ogg_file)
        except subprocess.CalledProcessError as e:
            print(f"处理 {ogg_file} 时出错: {e}")
            output_file.unlink(missing_ok=True)


def process_xp3(xp3_path: Path, encryption: str, speed: float):
    """处理单个 XP3 文件"""
    print(f"正在处理: {xp3_path}")

    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 解包 XP3
        print("正在解包...")
        with XP3(str(xp3_path), "r", silent=True) as xp3:
            xp3.extract(to=str(temp_path), encryption_type=encryption)

        # 处理音频文件
        print("正在处理音频文件...")
        process_audio_files(temp_path, speed)

        # 备份原文件
        backup_path = xp3_path.with_suffix(".xp3.bak")
        print(f"备份原文件到: {backup_path}")
        shutil.move(str(xp3_path), str(backup_path))

        # 重新打包
        print("正在重新打包...")
        with XP3(str(xp3_path), "w", silent=True, compressed=True) as xp3:
            xp3.add_folder(str(temp_path))

    print(f"完成处理: {xp3_path}\n")


def main():
    parser = argparse.ArgumentParser(description="批量处理 XP3 文件中的音频")
    parser.add_argument("folder", type=str, help="包含 XP3 文件的文件夹路径")
    parser.add_argument(
        "--encryption", "-e", type=str, default="none", help="XP3 文件的加密方式"
    )
    parser.add_argument(
        "--speed", "-s", type=float, default=1.5, help="音频加速倍率 (默认: 1.5)"
    )

    args = parser.parse_args()
    folder_path = Path(args.folder)

    if not folder_path.exists():
        print(f"错误: 文件夹 {folder_path} 不存在")
        return

    # 查找所有 XP3 文件
    xp3_files = list(folder_path.rglob("*.xp3"))
    if not xp3_files:
        print(f"在 {folder_path} 中没有找到 XP3 文件")
        return

    print(f"找到 {len(xp3_files)} 个 XP3 文件")
    for xp3_file in xp3_files:
        process_xp3(xp3_file, args.encryption, args.speed)


if __name__ == "__main__":
    main()
