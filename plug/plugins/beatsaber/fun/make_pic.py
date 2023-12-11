from PIL import Image, ImageDraw, ImageFont
import os
import json
import re


def make_pic(account, up="get-beastsaber-score/plugins/beatsaber/"):
    # 账户
    acc = str(account)

    # 获取用户信息
    with open(f"{up}data/info/user.json", "r", encoding="utf-8") as f:
        user_dict = json.load(f)

    # 获取hash-key对应表
    with open(f"{up}data/info/hash_key.json", "r", encoding="utf-8") as f:
        hash_key_dict = json.load(f)

    # 获取歌曲信息
    with open(f"{up}data/info/page1.json", "r", encoding="utf-8") as f:
        page1_dict = json.load(f)

    with open(f"{up}data/info/page2.json", "r", encoding="utf-8") as f:
        page2_dict = json.load(f)

    with open(f"{up}data/info/page3.json", "r", encoding="utf-8") as f:
        page3_dict = json.load(f)

    with open(f"{up}data/info/page4.json", "r", encoding="utf-8") as f:
        page4_dict = json.load(f)

    # 页面列表
    page_list = [page1_dict, page2_dict, page3_dict, page4_dict]

    # 字体
    font_name = ImageFont.truetype(font=f'{up}data/font/STHUPO.TTF', size=165)
    font_song = ImageFont.truetype(font=f'{up}data/font/impact.ttf', size=34)
    font_pp = ImageFont.truetype(font=f'{up}data/font/impact.ttf', size=145)
    font_rank = ImageFont.truetype(font=f'{up}data/font/FZYTK.TTF', size=28)

    # 创建一个空白图像
    image = Image.new('RGBA', (2560, 1700), color=(160, 160, 160, 0))

    # 整体圆角蒙版效果
    # image.paste(Image.open(f"{up}data/img/upper_musk.png"), (0, 0))
    # 绘图对象
    draw = ImageDraw.Draw(image)

    # 数据块规格
    y_start_height = 560
    x_start_weight = 120
    y_end_height = 100
    x_end_weight = 120
    block_height = 140
    block_weight = 420
    between_h = 40
    between_w = 62
    head_height = 360
    head_weight = 1400
    y_head_start_height = (y_start_height - head_height) // 2
    x_head_start_weight = x_start_weight

    # 头部色块
    image_head = Image.new('RGBA', (head_weight, head_height), color=(0, 0, 0, 160))
    # 歌曲块色块
    image_fill = Image.new('RGBA', (block_weight, block_height), color=(0, 0, 0, 225))

    # 构建背景
    if os.path.exists(f"{up}data/img/back/{acc}.jpg"):
        image.paste(Image.open(f"{up}data/img/back/{acc}.jpg"), (0, 0))
    else:
        image.paste(Image.open(f"{up}data/img/back/default.jpg"), (0, 0))

    # 构建头部
    image.paste(image_head, (
        x_head_start_weight, y_head_start_height, x_head_start_weight + head_weight, y_head_start_height + head_height),
                Image.open(f"{up}data/img/musk/head_musk.png"))
    # 构建头像
    image.paste(Image.open(f"{up}data/img/avatar.jpg"), (
        x_head_start_weight, y_head_start_height, x_head_start_weight + head_height, y_head_start_height + head_height),
                Image.open(f"{up}data/img/musk/avatar_musk.png"))

    # 写名字
    draw.text(xy=(x_head_start_weight + head_height + 30, y_head_start_height + 25), text=user_dict["name"],
              fill=(200, 255, 255),
              font=font_name)

    # 写pp
    user_pp = user_dict["pp"]
    draw.text(xy=(x_head_start_weight + head_height + 30, y_head_start_height + 40 + 140),
              text=str("%.2f" % user_pp) + " PP",
              fill=(0, 50, 80),
              font=font_pp)

    # 写国家和排名

    # 装饰
    # image.paste(Image.open(f"data/img/DLX1.png"), (1260, 150), Image.open(f"data/img/DLX1.png"))

    # 循环构建歌曲块
    page = 0
    count = 0

    # 注意先竖后横
    while x_start_weight < 2560 - x_end_weight:
        y_start_height = 560
        while y_start_height < 1700 - y_end_height:

            # 当前歌曲json
            if count <= 7:
                current_page = page_list[page]
            else:
                page += 1
                count = 0
                current_page = page_list[page]
            current_song = current_page["playerScores"][count]
            count += 1
            # 构建圆角半透明底板
            image.paste(image_fill,
                        (x_start_weight, y_start_height, x_start_weight + block_weight, y_start_height + block_height),
                        Image.open(f"{up}data/img/musk/song_musk.png"))
            # 构建封面
            path = current_song["leaderboard"]["songHash"]
            image.paste(Image.open(f"{up}data/info/cover//{path}.png"),
                        (x_start_weight, y_start_height, x_start_weight + block_height, y_start_height + block_height),
                        Image.open(f"{up}data/img/musk/cover_musk.png"))
            # 等级
            # if current_song["score"]["level"] == 0:
            #     image.paste(Image.open(f"{up}data/img/Rank_SS.png"),
            #             (x_start_weight - 40, y_start_height - 40),
            #             Image.open(f"{up}data/img/Rank_SS.png"))

            # 难度

            # 是否fc
            if current_song["score"]["fullCombo"]:
                image.paste(Image.open(f"{up}data/img/FC.png"),
                            (x_start_weight - 120 + block_weight - 10, y_start_height - 52 + block_height),
                            Image.open(f"{up}data/img/FC.png"))

            # 文字部分
            # 歌名，超出17字符长度的部分要截去
            song_name = current_song["leaderboard"]["songName"]
            re_song_name = r"(.+)\s[^\s]+"
            while len(song_name) > 17:
                song_name = re.search(re_song_name, song_name).group(1)
                # print(song_name)
                continue
            draw.text(xy=(x_start_weight + block_height + 25, y_start_height + 10),
                      text=song_name,
                      fill=(220, 220, 255), font=font_song)
            # rank
            draw.text(xy=(x_start_weight + block_height + 25, y_start_height + 52),
                      text="RANK " + str(current_song["leaderboard"]["stars"]),
                      fill=(10, 90, 210),
                      font=font_rank)
            # 准度
            # draw.text(xy=(x_start_weight + block_height + 170, y_start_height + 55), text=info_list[4][4] + "%", fill=(0, 160, 160),
            #           font=font2)

            # key
            draw.text(xy=(x_start_weight + block_height + 170, y_start_height + 52), text="! " + hash_key_dict[current_song["leaderboard"]["songHash"]],
                      fill=(46, 210, 231),
                      font=font_rank)

            # 歌曲pp
            pp = current_song["score"]["pp"]
            draw.text(xy=(x_start_weight + block_height + 25, y_start_height + 85),
                      text=str("%.2f" % pp) + "PP", fill=(280, 160, 280),
                      font=font_song)

            y_start_height += block_height + between_h
        x_start_weight += block_weight + between_w

    image.save(rf'{up}data/img/score.png')
    image.show()


if __name__ == '__main__':
    make_pic(76561199085587690, up="../")
