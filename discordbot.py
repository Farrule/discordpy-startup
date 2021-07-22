"""
＿/＿/＿/＿/＿/＿/＿/＿/
＿/   ver 2.3.5β   ＿/
_/＿/＿/＿/＿/＿/＿/＿/
"""
# TODO: コマンドフィックス変更
# TODO: バージョン変更
# TODO: import os の追加 os.environへの変更

import discord
import re
import sys
import asyncio
import os


client = discord.Client()
# TODO:os.environ['DISCORD_BOT_TOKEN']
TOKEN = os.environ['DISCORD_BOT_TOKEN']
flag = True
o_flag = True
b_count = 0
m_count = 0

# UNICODE
ONE = '\N{Large Red Circle}'
TWO = '\N{Large Blue Circle}'
THREE = '\N{Large Yellow Circle}'
FOUR = '\N{Large Green Circle}'
FIVE = '\N{Large Orange Circle}'
SIX = '\N{Large Purple Circle}'
SEVEN = '\N{Large Brown Circle}'
EIGHT = '\N{Medium Black Circle}'
NINE = '\N{Medium White Circle}'
CANCEL = '\N{SQUARED CL}'
ERROR = '\N{WARNING SIGN}'

# リアクションリスト
REACTION_LIST = [
    ONE, TWO, THREE, FOUR, FIVE,
    SIX, SEVEN, EIGHT, NINE]

# メンバーリスト
MEMBER_LIST = []

# help_Embed
help = discord.Embed(
    title='募集用bot 「@bot_chan」の使い方',
    description='募集したい内容を、人数を設定して募集をかけることが出きるbotです。\n'
    '各コマンドの使い方は以下を御参照ください。\n',
    color=discord.Color.red())
# help !at使い方
help.add_field(
    name=':loudspeaker: 各コマンドの使い方\n',
    value=':pushpin:***募集を募るコマンド***\n'
    '   募集の際に使うこのbotの基本となるコマンド\n'
    '\n'
    '   ***記述方法***\n'
    '   **!at 「募集要項」 「人数」**\n'
    '\n'
    '   ※各要素に必ず半角スペースを１つ設けてください。\n'
    '   ※鍵かっこをつける必要はありません。\n'
    '   ※合計９人まで募集をかけられます。\n'
    '   ※それぞれの参加ボタンが押された時点で募集を終了します。\n'
    '\n'
    ':pushpin:***バグ対応用コマンド***\n'
    '   コマンド実行時などにバグが発生した際に一時的な対策として使うコマンド\n'
    '\n'
    '   ***記述方法***\n'
    '   **!atre**\n',
    inline=False)
# help リアクションについて
help.add_field(
    name=':loudspeaker: リアクションについて\n',
    value='このbotではリアクションを用いて\n'
    '__参加ボタン__を(例 :red_circle:)\n'
    '__募集中止ボタン__を(:cl:)として扱っています。\n'
    '\n'
    ':pushpin:参加ボタンについて\n'
    '   人数に応じてボタンが追加されます。\n'
    '   募集者や一度リアクションした人はボタンを押せなくなります。\n'
    '\n'
    ':pushpin:募集中止ボタンについて\n'
    '   募集中止ボタンは押した時点で__募集を取り消す__ことができます。\n')
# help developer info
# TODO: バージョンアップ時変更
help.set_footer(
    text='made by Farrule\n'
    '@bot_chan verstion: 2.3.5β',
    icon_url='https://cdn.discordapp.com/'
    'attachments/865123798813900820/865258524971106314/Farrule_logo2.jfif')


# ? BOT起動時処理
@client.event
async def on_ready():
    print('-------------------------------------------------------------------------------\n')
    print('running now')
    print('@bot_chan')  # Bot Name
    print('Farrule#4771')  # User ID
    print(discord.__version__)  # discord.py バージョン
    print(sys.version)  # Python バージョン
    print()
    print('-------------------------------------------------------------------------------')
    # TODO: バージョンアップ時変更
    await client.change_presence(activity=discord.Game(name='@bot_chan v2.3.5β'))


# ? コマンド入力時処理
@client.event
async def on_message(mes):
    if mes.author.bot:
        return

    global flag, bot_name, MEMBER_DIS, limit, o_flag, MEMBER_LIST
    global bot_message, m_count, b_count, m, REACTION_LIST, args
    args = mes.content.split()

    # ! !at 処理
    if args[0] == '!at':
        if flag is True:
            if re.compile(r'\d+').search(args[2]):
                m = int(args[2])
                if m <= 9:
                    limit = args[2]
                    host = mes.author.name
                    MEMBER_LIST.append(host)
                    MEMBER_DIS = ',    '.join(MEMBER_LIST)
                    bot_message = await mes.channel.send(
                        f':loudspeaker: @here ***{args[1]}*** で'
                        f' ***{args[2]}*** /_{limit}_ 人募集中です。\n'
                        f':pushpin: 参加者:\n       {MEMBER_DIS}')
                    for x in range(m):
                        await bot_message.add_reaction(REACTION_LIST[x])
                    await bot_message.add_reaction(CANCEL)
                    bot_name = bot_message.author.name
                    flag = False
                else:
                    await mes.channel.send(
                        ':warning:  __９人以上__の募集はできません。\n')
                    return
            else:
                await mes.channel.send(
                    ':warning:  __人数の項目__が不適切です。\n')
                return
        else:
            await mes.channel.send(
                ':warning:  __募集中__の要項があります。\n')
            return

    # ! !help 処理
    if args[0] == '!help':
        await mes.channel.send(embed=help)

    # ! !atre 処理
    if args[0] == '!atre':
        await mes.channel.send(':exclamation: リセット処理を実行\n')
        flag = True
        o_flag = True
        b_count = 0
        m_count = 0
        MEMBER_LIST = []
        MEMBER_DIS = []


# ? リアクションボタン メンバーリスト追加処理
@client.event
async def on_reaction_add(reaction, user):
    global MEMBER_LIST, o_flag, m_count
    reaction

    if m_count >= m + 1:
        user = user.name
        if user in MEMBER_LIST:
            o_flag = False
            return
        else:
            o_flag = True
            MEMBER_LIST.append(user)
    else:
        m_count = m_count + 1


# ? 各リアクションボタン処理
@client.event
async def on_raw_reaction_add(reaction):
    global flag, REACTION_LIST, o_flag, MEMBER_LIST, m_count, b_count

    # 募集人数カウンタ
    def b_process_1():
        mem = int(args[2])
        mem = mem - 1
        args[2] = str(mem)

    # 要素リセット
    def b_process_2():
        global flag, o_flag, b_count, m_count, MEMBER_LIST, MEMBER_DIS
        flag = True
        o_flag = True
        b_count = 0
        m_count = 0
        MEMBER_LIST = []
        MEMBER_DIS = []

    # メンバーリスト整列
    def b_process_3():
        global MEMBER_LIST, bot_name, MEMBER_DIS
        if bot_name in MEMBER_LIST:
            MEMBER_LIST.remove(bot_name)
        MEMBER_DIS = ',    '.join(MEMBER_LIST)

    if b_count >= m + 1:
        # ! CANCELボタン処理
        if reaction.emoji.name == CANCEL:
            await bot_message.clear_reaction(CANCEL)
            for y in range(m):
                await bot_message.clear_reaction(REACTION_LIST[y])
            await bot_message.edit(content='募集が__中止__されました。\n')
            b_process_2()

        await asyncio.sleep(0.1)

        # ! 参加ボタン処理
        for i in REACTION_LIST:
            if reaction.emoji.name == i:
                if o_flag is False:
                    await bot_message.add_reaction(ERROR)
                    await asyncio.sleep(1)
                    await bot_message.clear_reaction(ERROR)
                    o_flag = True
                    return
                else:
                    b_process_1()
                    b_process_3()
                    await bot_message.clear_reaction(i)
                    await bot_message.edit(
                        content=f':loudspeaker: @here ***{args[1]}*** で'
                        f' ***{args[2]}*** /_{limit}_ 人募集中です。\n'
                        f':pushpin: 参加者:\n       {MEMBER_DIS}')
                    if args[2] == '0':
                        await bot_message.clear_reaction(CANCEL)
                        b_process_3()
                        await bot_message.edit(
                            content=f'***{args[1]}*** の募集は__終了__しました。\n'
                            f':pushpin: 参加者:\n       {MEMBER_DIS}')
                        b_process_2()
            else:
                return
    else:
        b_count = b_count + 1
        return


client.run(TOKEN)
