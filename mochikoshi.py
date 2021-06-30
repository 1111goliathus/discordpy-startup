import discord
import re

import re_YuniBot
# チャンネル情報
CHANNEL_ID = tomobot.get_channel_id("開発用")

# デバッグ用
# 個人鯖に飛ぶ
#CHANNEL_ID = tomobot.get_channel_id("tomobot")

TOKEN = re_YuniBot.get_token("yunibot")
client = discord.Client()

mochikoshi_list = {}
'''
    持ち越し時間の判定について、
    以下のパターンに一致するものを時刻の情報とする
    \d:\d\d (ex:0:45)
    \d\d\d  (ex:113) calcのみ
    \d\ds   (ex:53s) applyのみ
    \d\d    (ex:53) calcのみ

    3桁の数字を時刻判定するとTL内のダメ表記まで置換されてしまうので
    対応検討中
'''

'''
    既知のバグ：
        ・最後のUBの時間が同じ場合、その中で一番最初のものを除き消される
'''


def calc_sec(text):

    # 切り出して数字の部分のみ取り出す
    res = str(text).replace(":", "").replace('s', "")

    # 文字数を3文字に統一する
    if len(res) == 2:
        res = "0" + res

    # 時間を求める
    t = int(res[0]) * 60 + int(res[1:])

    return t

#  持ち越し時間を計算する関数
## text: 投稿されたテキスト


def calc_mochikoshi(text):

    # 正規表現を用いて存在を確認する
    patten = re.compile(r'(\d:\d\d)|(\d\d\d)|(\d\d)')
    result = re.match(patten, text.content)

    # 該当パターンが存在した場合
    if result:
        t = calc_sec(result.group(0))
        if int(t) <= 0 or int(t) > 90:
            raise Exception
        # 結果を記録する
        mochikoshi_list[text.author] = int(t)
        return t


def apply_mochikoshi(message):
    msg = str(message.content)

    # 正規表現を用いて存在を確認する
    patten = re.compile(r'(\d:\d\d)|(\d\ds)')
    result = re.match(patten, msg)

    # 正規表現に一致する部分のリストを取得
    l = re.findall(patten, msg)

    # リスト内の要素に対し、変換前と変換後の値の組を取得
    li = {}
    for i in l:
        for j in i:
            if j != '':
                t = mochikoshi_list[message.author] - (90 - calc_sec(j))

                # 1秒以上残る場合はリストに追加する
                if (t > 0):
                    rep = ""
                    if (t >= 60):
                        rep += "1:"
                        t -= 60
                    else:
                        rep += '0:'
                    if len(str(t)) == 1:
                        rep += '0'
                    rep += str(t)
                    li[j] = rep

    # 大きい方から置換すると同じものを複数回置換してしまう可能性があるため、
    # 小さい方からソートする
    li_sorted = sorted(li.items(), key=lambda x: x[0])
    print(li_sorted)

    # 置換処理
    for before, after in li_sorted:
        msg = msg.replace(before, after)

    # リストの先頭要素（最後のUB）以降を削除する
    msg = msg.split(li_sorted[0][1])[0] + str(li_sorted[0]
                                              [1]) + msg.split(li_sorted[0][1])[1].splitlines()[0]
    return msg


@client.event
async def on_message(message):
    channel = client.get_channel(CHANNEL_ID)

    # print(message.author)
    # 別チャンネルへの投稿
    if (message.channel.id != CHANNEL_ID):
        return
    # メッセージ送信者が自分自身の場合
    if (message.author.bot):
        return
    # リスト内に秒数が格納されていない場合
    if (message.author not in mochikoshi_list):
        try:
            # 入力された持ち越し時間を取得
            mochikoshi_time = calc_mochikoshi(message)

            # メッセージ送信
            await channel.send(f'{message.author.mention}' +
                               " 持ち越し時間:" +
                               str(mochikoshi_list[message.author]) +
                               "秒")
        except:
            await channel.send(f'{message.author.mention}' + "持ち越し時間の取得に失敗しました")
            if message.author in mochikoshi_list:
                del mochikoshi_list[message.author]
    else:
        try:
            # 変換後TLを取得
            tl = apply_mochikoshi(message)
            # メッセージ送信
            await channel.send(tl)
            del mochikoshi_list[message.author]
        except:
            await channel.send(f'{message.author.mention}' + "TL変換に失敗しました")
            if message.author in mochikoshi_list:
                del mochikoshi_list[message.author]

client.run(TOKEN)
