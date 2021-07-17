"""
＿/＿/＿/＿/＿/＿/＿/＿/
＿/   ver 2.2.0α   ＿/
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
ERROR = '\N{NO ENTRY}'

# リアクションリスト
REACTION_LIST = [
    ONE, TWO, THREE, FOUR, FIVE,
    SIX, SEVEN, EIGHT, NINE]

# メンバーリスト
MEMBER_LIST = []

# help_Embed
help = discord.Embed(
    title=':loudspeaker: 募集用bot 「@bot_chan」の使い方',
    description='募集したい内容を、人数を設定して募集をかけることが出きるbotです。\n'
    '各コマンドの使い方は以下を御参照ください。\n',
    color=discord.Color.red())
# help ?at使い方
help.add_field(
    name=':loudspeaker: ?at コマンドの使い方\n',
    value='募集の際に使うこのbotの基本となるコマンドです。\n'
    '\n'
    '記述方法は\n'
    '?at 「募集要項」 「人数」「自由記述文(必要に応じて)」\n'
    'となります。\n'
    '\n'
    '※各要素に必ず半角スペースを１つ設けてください。\n'
    '※鍵かっこをつける必要はありません。\n'
    '※合計９人まで募集をかけられます。\n'
    '\n'
    '例: ?at APEX 2\n',
    inline=False)
# help リアクションについて
help.add_field(
    name=':loudspeaker: リアクションについて\n',
    value='このbotではリアクションを用いて\n'
    '参加ボタンを(例 :red_circle:)\n'
    '募集中止ボタンを(:cl:)として扱っています。\n'
    '\n'
    '人数に応じてボタンが追加され、それぞれ１人ずつ押すようにしてください。\n'
    '\n'
    'それぞれの参加ボタンが押された時点で募集を終了します。\n'
    '\n'
    '募集中止ボタンは押した時点で募集を取り消すことができます。\n')
# help developer info
#TODO: バージョンアップ時変更
help.set_footer(
    text='made by Farrule\n'
    '@bot_chan verstion: 2.2.0α',
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
    #TODO: バージョンアップ時変更
    await client.change_presence(activity=discord.Game(name='@bot_chan v2.2.0α'))


# ? コマンド入力時処理
@client.event
async def on_message(mes):
    if mes.author.bot:
        return

    global flag
    global bot_message
    global args
    global REACTION_LIST
    global m
    global b_count
    global m_count
    global MEMBER_LIST
    global o_flag
    args = mes.content.split()

    #! ?at 処理
    if args[0] == '?at':
        if flag == True:
            m = int(args[2])
            if m <= 9:
                if len(args) == 4:

                    #! 自由文あり処理
                    if re.compile(r'\d+').search(args[2]):
                        bot_message = await mes.channel.send(
                            f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n'
                            f'{args[3]}')
                        for x in range(m):
                            await bot_message.add_reaction(REACTION_LIST[x])
                        await bot_message.add_reaction(CANCEL)
                        flag = False
                    else:
                        await mes.channel.send('__人数の項目__が不適切です。\n')

                elif len(args) == 3:

                    #! 自由文なし処理
                    if re.compile(r'\d+').search(args[2]):
                        bot_message = await mes.channel.send(
                            f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                        for x in range(m):
                            await bot_message.add_reaction(REACTION_LIST[x])
                        await bot_message.add_reaction(CANCEL)
                        flag = False
                    else:
                        await mes.channel.send('__人数の項目__が不適切です。\n')

                else:
                    return
            else:
                await mes.channel.send('__９人以上__の募集はできません。\n')
                return
        else:
            await mes.channel.send('__募集中__の要項があります。\n')
            return

    #! ?help 処理
    if args[0] == '?help':
        await mes.channel.send(embed=help)

    #! ?atre 処理
    if args[0] == '?atre':
        await mes.channel.send('リセット処理を実行\n')
        flag = True
        o_flag = True
        b_count = 0
        m_count = 0
        MEMBER_LIST = []


# ? リアクションボタン メンバーリスト追加処理
@client.event
async def on_reaction_add(reaction, user):
    global MEMBER_LIST
    global m_count
    global o_flag
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
    global flag
    global b_count
    global m_count
    global MEMBER_LIST
    global o_flag

    # 募集人数カウンタ
    def b_process_1():
        mem = int(args[2])
        mem = mem - 1
        args[2] = str(mem)

    # 要素リセット
    def b_process_2():
        global flag
        global b_count
        global m_count
        global MEMBER_LIST
        global o_flag
        flag = True
        o_flag = True
        b_count = 0
        m_count = 0
        MEMBER_LIST = []

    # メンバーリスト整列
    def b_process_3():
        global MEMBER_LIST
        MEMBER_LIST = ',    '.join(MEMBER_LIST)

    if b_count >= m + 1:
        #! CANCELボタン処理
        if reaction.emoji.name == CANCEL:
            await bot_message.clear_reaction(CANCEL)
            for y in range(m):
                await bot_message.clear_reaction(REACTION_LIST[y])
            await bot_message.edit(content='募集が__中止__されました。\n')
            b_process_2()

        await asyncio.sleep(0.1)

        #! 参加ボタン処理
        if reaction.emoji.name == ONE:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(ONE)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == TWO:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(TWO)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == THREE:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(THREE)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == FOUR:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(FOUR)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == FIVE:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(FIVE)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'{args[1]} の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == SIX:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(SIX)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == SEVEN:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(SEVEN)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == EIGHT:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(EIGHT)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

        if reaction.emoji.name == NINE:
            if o_flag == False:
                await bot_message.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_message.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                b_process_1()
                await bot_message.clear_reaction(NINE)
                await bot_message.edit(
                    content=f':loudspeaker: @here ***{args[1]}*** で ***{args[2]}*** 人募集中です。\n')
                if args[2] == '0':
                    await bot_message.clear_reaction(CANCEL)
                    b_process_3()
                    await bot_message.edit(
                        content=f'***{args[1]}*** の募集は__終了__しました。\n'
                        f':pushpin: 参加者:\n       {MEMBER_LIST}')
                    b_process_2()

    else:
        b_count = b_count + 1


client.run(TOKEN)
