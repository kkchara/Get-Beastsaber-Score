from plug.plugins.beatsaber.fun import make_pic
from plug.plugins.beatsaber.fun import get_info

acc = input("your SS account：")

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
