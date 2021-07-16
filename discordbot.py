"""
＿/＿/＿/＿/＿/＿/＿/＿/
＿/   ver 2.0. α   ＿/
_/＿/＿/＿/＿/＿/＿/＿/
"""


import discord
import re
import sys
import os


client = discord.Client()
TOKEN = os.environ['DISCORD_BOT_TOKEN']
flag = True
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
help.set_footer(
    text='made by Farrule\n'
    '@bot_chan verstion: 2.0. α',
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
    await client.change_presence(activity=discord.Game(name='@bot_chan v2.0. α'))


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
    args = mes.content.split()

    # TODO: ?at 処理
    if args[0] == '?at':
        if flag == True:
            m = int(args[2])
            if m <= 9:
                if len(args) == 4:

                    #! 自由文あり処理
                    if re.compile(r'\d+').search(args[2]):
                        bot_message = await mes.channel.send(
                            f'@here {args[1]}で{args[2]}人募集中です\n'
                            f'{args[3]}')
                        for x in range(m):
                            await bot_message.add_reaction(REACTION_LIST[x])
                        await bot_message.add_reaction(CANCEL)
                        flag = False
                    else:
                        await mes.channel.send('人数の項目が不適切です')

                elif len(args) == 3:

                    #! 自由文なし処理
                    if re.compile(r'\d+').search(args[2]):
                        bot_message = await mes.channel.send(
                            f'@here {args[1]}で{args[2]}人募集中です')
                        for x in range(m):
                            await bot_message.add_reaction(REACTION_LIST[x])
                        await bot_message.add_reaction(CANCEL)
                        flag = False
                    else:
                        await mes.channel.send('人数の項目が不適切です')

                else:
                    return
            else:
                await mes.channel.send('９人以上の募集はできません')
                return
        else:
            await mes.channel.send('募集中の要項があります')
            return

    # TODO: ?help 処理
    if args[0] == '?help':
        await mes.channel.send(embed=help)

    # TODO: ?atre 処理
    if args[0] == '?atre':
        await mes.channel.send('リセット処理を実行')
        flag = True


# ? 各リアクションボタン処理
@client.event
async def on_raw_reaction_add(reaction):
    global flag
    global b_count
    global m_count
    global MEMBER_LIST

    def b_process_1():
        mem = int(args[2])
        mem = mem - 1
        args[2] = str(mem)

    def b_process_2():
        global flag
        global b_count
        global m_count
        global MEMBER_LIST
        flag = True
        b_count = 0
        m_count = 0
        MEMBER_LIST = []

    def b_process_3():
        global MEMBER_LIST
        MEMBER_LIST = ',    '.join(MEMBER_LIST)

    if b_count >= m + 1:
        #! CANCELボタン処理
        if reaction.emoji.name == CANCEL:
            await bot_message.clear_reaction(CANCEL)
            for y in range(m):
                await bot_message.clear_reaction(REACTION_LIST[y])
            await bot_message.edit(content='募集が中止されました。')
            b_process_2()

        #! 参加ボタン処理
        if reaction.emoji.name == ONE:
            b_process_1()
            await bot_message.clear_reaction(ONE)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                MEMBER_LIST = '\n'.join(MEMBER_LIST)
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == TWO:
            b_process_1()
            await bot_message.clear_reaction(TWO)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == THREE:
            b_process_1()
            await bot_message.clear_reaction(THREE)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == FOUR:
            b_process_1()
            await bot_message.clear_reaction(FOUR)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == FIVE:
            b_process_1()
            await bot_message.clear_reaction(FIVE)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == SIX:
            b_process_1()
            await bot_message.clear_reaction(SIX)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == SEVEN:
            b_process_1()
            await bot_message.clear_reaction(SEVEN)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == EIGHT:
            b_process_1()
            await bot_message.clear_reaction(EIGHT)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

        if reaction.emoji.name == NINE:
            b_process_1()
            await bot_message.clear_reaction(NINE)
            await bot_message.edit(
                content=f'@here {args[1]}で{args[2]}人募集中です。')
            if args[2] == '0':
                await bot_message.clear_reaction(CANCEL)
                b_process_3()
                await bot_message.edit(
                    content=f'{args[1]}の募集は終了しました。\n'
                    f'参加者:\n{MEMBER_LIST}')
                b_process_2()

    else:
        b_count = b_count + 1


# ? リアクションボタン メンバーリスト追加処理
@client.event
async def on_reaction_add(reaction, user):
    global MEMBER_LIST
    global m_count
    reaction

    if m_count >= m + 1:
        user = user.name
        MEMBER_LIST.append(user)
    else:
        m_count = m_count + 1


client.run(TOKEN)
