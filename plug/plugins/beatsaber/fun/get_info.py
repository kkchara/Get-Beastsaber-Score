import json
import warnings
from PIL import Image
import requests
import time
import re
import os
import asyncio
import aiohttp


def get_json(acc, up="get-beastsaber-score/plugins/beatsaber/"):
    warnings.filterwarnings("ignore")
    page = 1
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Cookie": "connect.sid=s%3AqYAU3jtpRZMGaeGQ0krE6abunAuDB8Nt.jzGieagN8PqokqeRpnHgYlwI5SUW7MwObk%2BSNlLCASA"}
    while page <= 3:
        top_res = requests.get(f'https://scoresaber.com/api/player/{acc}/scores?page={page}&sort=top',
                               headers=header, verify=False)
        data = top_res.text
        with open(f"{up}data/info/page{page}.json", "w", encoding="utf-8") as f:
            f.write(str(data))
        page += 1

    time.sleep(0.2)

    recent_res = requests.get(f'https://scoresaber.com/api/player/{acc}/scores?page=1&sort=recent', headers=header,
                              verify=False)
    data = recent_res.text
    with open(f"{up}data/info/page4.json", "w", encoding="utf-8") as f:
        f.write(str(data))

    time.sleep(0.2)

    full_res = requests.get(f'https://scoresaber.com/api/player/{acc}/full', headers=header)
    full_data = full_res.text
    with open(f"{up}data/info/user.json", "w", encoding="utf-8") as f:
        f.write(str(full_data))


# async def async_get(url, header):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=header) as response:
#             return await response.text()
#
#
# async def as_get_json(acc, up="get-beastsaber-score/plugins/beatsaber/"):
#     page = 1
#     header = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
#         "Cookie": "connect.sid=s%3AqYAU3jtpRZMGaeGQ0krE6abunAuDB8Nt.jzGieagN8PqokqeRpnHgYlwI5SUW7MwObk%2BSNlLCASA"}
#     while page <= 3:
#         url = f'https://scoresaber.com/api/player/{acc}/scores?page={page}&sort=top'
#         top_res = await async_get(url, header)
#         data = top_res
#         with open(f"{up}data/info/page{page}.json", "w", encoding="utf-8") as f:
#             f.write(data)
#         page += 1
#
#     await asyncio.sleep(0.1)
#
#     url = f'https://scoresaber.com/api/player/{acc}/scores?page=1&sort=recent'
#     recent_res = await async_get(url, header)
#     data = recent_res
#     with open(f"{up}data/info/page4.json", "w", encoding="utf-8") as f:
#         f.write(data)
#
#     await asyncio.sleep(0.1)
#
#     url = f'https://scoresaber.com/api/player/{acc}/full'
#     full_res = await async_get(url, header)
#     full_data = full_res
#     with open(f"{up}data/info/user.json", "w", encoding="utf-8") as f:
#         f.write(full_data)


def get_avatar(scc, up="get-beastsaber-score/plugins/beatsaber/"):
    warnings.filterwarnings("ignore")
    avatar_info = requests.get(f'https://cdn.scoresaber.com/avatars/{scc}.jpg', verify=False)
    with open(f"{up}data/img/avatar.jpg", "wb") as f:
        f.write(avatar_info.content)
    image = Image.open(f"{up}data/img/avatar.jpg")
    resized_image = image.resize((360, 360))
    resized_image.save(f"{up}data/img/avatar.jpg")


def get_hash(up="get-beastsaber-score/plugins/beatsaber/"):
    hash_list = []
    for i in range(1, 5):
        with open(f"{up}data/info/page{i}.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            for j in data["playerScores"]:
                hash_list.append(j["leaderboard"]["songHash"])
    # print(hash_list[31])
    return hash_list


def get_cover(hash_list, up="get-beastsaber-score/plugins/beatsaber/"):
    warnings.filterwarnings("ignore")
    for h in hash_list:
        if os.path.exists(f"{up}/data/info/cover/{h}.png"):
            continue
        else:
            cover_info = requests.get(f'https://cdn.scoresaber.com/covers/{h}.png', verify=False)
            with open(f"{up}/data/info/cover/{h}.png", "wb") as f:
                f.write(cover_info.content)
            image = Image.open(f"{up}/data/info/cover/{h}.png")
            resized_image = image.resize((140, 140))
            resized_image.save(f"{up}/data/info/cover/{h}.png")

    # 解析
    # 保存头像和歌曲封面(名称为hash)到文件夹，保存昵称，pp，国家排名和前24首最佳和前6首最近的（key/hash）与难度到json)


def get_key(hash_list: list, up="get-beastsaber-score/plugins/beatsaber/"):
    warnings.filterwarnings("ignore")
    f = open(f"{up}/data/info/hash_key.json", "r", encoding="utf-8")
    hash_data = json.load(f)
    for h in hash_list:
        if h in hash_data.keys():
            continue
        else:
            key_info = requests.get(f'https://beatsaver.com/api/maps/hash/{h}')
            # print(key_info.text)
            key = re.search(r'[0-9a-f][0-9a-f][0-9a-f][0-9a-f]+', key_info.text)
            # print(key.group(0))
            # print(type(data))
            hash_data[h] = key.group(0)
    f.close()
    with open(f"{up}/data/info/hash_key.json", "w", encoding="utf-8") as f:
        json.dump(hash_data
                  , f)


if __name__ == '__main__':
    time1 = time.time()
    get_json("76561199085587690", up="../")
    print(time.time() - time1)

    time2 = time.time()
    hash_test = get_hash(up="../")
    print(time.time() - time2)

    time3 = time.time()
    get_key(hash_test, up="../")
    print(time.time() - time3)

    time4 = time.time()
    get_avatar("76561199085587690", up="../")
    print(time.time() - time4)

    time5 = time.time()
    get_cover(hash_test, up="../")
    print(time.time() - time5)
