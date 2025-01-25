### xp3 格式批量音频加速

[文章链接](https://absx.pages.dev/articles/speedup.html)

batch.py 可以批量加速 XP3 文件中的音频文件。使用方法：

```sh
python batch.py <folder> --speed <speed>
python batch.py <folder> --speed <speed> --encryption <encryption>
# 更多参数请使用 python batch.py -h 查看
```

不过根据测试，xp3.py 可能无法解包第二版本的 XP3 文件(?)，例如 空に刻んだパラレログラム。所以根据情况，可能需要自行使用 GARbro 解包后，再修改脚本进行加速。

---

（基于 [Galgamer-org/krkr-xp3](https://github.com/Galgamer-org/krkr-xp3) 制作，README.md 原文：）

# KiriKiri .XP3 archive repacking and extraction tool COMMAND LINE! You can use it in GitHub Actions!

Based on original script by Edward Keyes, ed-at-insani-dot-org, 2006-07-08, http://www.insani.org/tools/  
and SmilingWolf, https://bitbucket.org/SmilingWolf/xp3tools-updated

Based on Python 3 rewrite, Awakening

Enhanced by Kiriha!

## Introduction

Extracts an .XP3 archive to a directory of files, and
packs a directory of files into an .XP3 archive, including any
subdirectory structure.

Uses Numpy (if available) to speed up decryption/encryption.

## Features

Adapt multiple encryption schemes, you can add your own encryption scheme easily!

Please see game_list.py for more information.
