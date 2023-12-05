import json
import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg

from plug.plugins.beatsaber.fun import make_pic
from plug.plugins.beatsaber.fun import get_info

# 响应器
ss_matcher = on_command("ws", priority=5)
bl_matcher = on_command("bl", priority=6)
set_acc_matcher = on_command("setacc", priority=7)


# set_bg_matcher = on_command("setbg", priority=8)


@ss_matcher.handle()
async def get_ss(bot: Bot, event: Event):
    qq_num = str(event.get_user_id())
    acc = ""
    # 获得账号
    with open(r'get-beastsaber-score\plugins\beatsaber\data\account\account.json', 'r') as f:
        params = json.load(f)
        if qq_num in params:
            acc = params[qq_num]
            await ss_matcher.send(Message(f"少女祈祷中..."))
            # 爬取用户json
            get_info.get_json(acc)
            # 提取hash列表
            hash_list = get_info.get_hash()
            # 获取key
            get_info.get_key(hash_list)
            # 处理用户头像
            get_info.get_avatar(acc)
            # 处理歌曲封面
            get_info.get_cover(hash_list)
            # 生成图片
            make_pic.make_pic(acc)
            # 图片位置
            with open(f"get-beastsaber-score/plugins/beatsaber/data/img/score.png", "rb") as pic:
                img = pic.read()
            # 发送图片
            await ss_matcher.finish(MessageSegment.image(img))
        else:
            await ss_matcher.finish(Message(f"你还没有绑定账号！请使用/setacc命令进行绑定"))


@set_acc_matcher.handle()
async def set_ss(bot: Bot, event: Event, args: Message = CommandArg()):
    qq_num = str(event.get_user_id())
    acc = str(args.extract_plain_text())
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Cookie": "connect.sid=s%3AqYAU3jtpRZMGaeGQ0krE6abunAuDB8Nt.jzGieagN8PqokqeRpnHgYlwI5SUW7MwObk%2BSNlLCASA"}
    res = requests.get(f'https://scoresaber.com/api/player/{acc}/scores?page=1&sort=top', headers=header)
    if res.status_code == 200:
        f = open(r'get-beastsaber-score/plugins/beatsaber/data/account/account.json', 'r')
        params = json.load(f)
        f.close()
        if qq_num in params:
            await set_acc_matcher.finish(Message(f"你已经绑定了{params[qq_num]}为你的账号"))
        else:
            params[qq_num] = acc
            with open(r'get-beastsaber-score/plugins/beatsaber/data/account/account.json', 'w') as f:
                json.dump(params, f)
            await set_acc_matcher.finish(Message("绑定成功!"))
    else:
        await set_acc_matcher.finish(Message(f"绑定失败，请检查格式和账号是否正确，绑定示范：\n/setacc 123456789（这串数字是你的ss或者bl用户代码）"))

# @set_bl_matcher.handle()
# async def set_ss(bot: Bot, event: Event):
#     try:
#         qq_num = str(event.get_user_id())
#         ss_acc = str(event.get_plaintext().strip())
#         f = open(r'data\account\account.json', 'r')
#         params = json.load(f)
#         f.close()
#         if qq_num in params:
#             await set_bl_matcher.finish(Message(f"你已经绑定了{params[qq_num]}为你的bl账号"))
#         else:
#             params[qq_num] = "num"
#             with open(r'data\account\account.json', 'w') as f:
#                 json.dump(params, f)
#             await set_bl_matcher.finish(Message("绑定成功!"))
#     except Exception as e:
#         print(e)
#         await ss_matcher.finish(Message(f"发生错误，请联系管理员{e}"))

# @set_bg_matcher.handle()
# async def set_bg(bot: Bot, event: Event, args: Message = CommandArg()):
#     qq_num = str(event.get_user_id())
#     pic = args.()
