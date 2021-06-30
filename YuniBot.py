def get_token(name):
    if name != 'yunibot':
        return False
    else:
        return ("ODU5NjI2OTgwMzQxMTg2NTky.YNvcAw.YF7KLa-xAhkxxsS5HDdn5wpIXQk")


def get_channel_id(name):
    if name == "yunibot":
        return (859617039470952448)
        # ごら鯖のテスト用テキストチャンネル
    if name == "開発用":
        return (859615934250221618)
        # 同好会のテスト用チャンネル
    if name == "TL変換":
        return (859615934250221618)
        # 同好会の実稼働チャンネル
    return False
