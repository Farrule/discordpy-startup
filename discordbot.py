"""
＿/＿/＿/＿/＿/＿/＿/＿/
＿/  ver 1.0.7.0   ＿/
_/＿/＿/＿/＿/＿/＿/＿/
"""


import discord  # discord.py
import re  # re
import sys   # sys.version
import os

client = discord.Client()
TOKEN = os.environ['DISCORD_BOT_TOKEN']
OK = '\N{Heavy Large Circle}'
NO = '\N{Cross Mark}'
Cancel = '\N{No Entry Sign}'
flag = True
#TODO: embed
help = discord.Embed(
                    title=
                    "基本コマンド記述方法"

                    ,description=
                    '「!at タイトル 人数 自由文(任意)」\n\n'
                    'リアクションボタンは\n'
                    f'   {OK}ボタンは「参加」\n'
                    f'   {NO}ボタンは「訂正」\n'
                    f'   {Cancel}ボタンは「中止」\n'
                    'として扱ってください\n'
                    '２つ以上の募集はできません'

                    ,color =
                    discord.Colour.red())


#? BOT起動時処理
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
    await client.change_presence(activity=discord.Game(name='@bot_chan v1.0.7.0'))


#? コマンド入力時処理
@client.event
async def on_message(message):
    if message.author.bot:
        return

    global args
    global limit
    global bot_message
    global flag
    args = message.content.split()


    # TODO: !at 処理
    if args[0] == '!at':
        #! 排他処理
        if flag == True:
            if len(args) == 4:
                #! 自由文あり処理
                if re.compile(r'\d+').search(args[2]):
                    limit = args[2]
                    bot_message = await message.channel.send(
                        f'@here {args[1]}で{args[2]}人募集中です\n'
                        f'{args[3]}'
                    )
                    await bot_message.add_reaction(OK)
                    await bot_message.add_reaction(NO)
                    await bot_message.add_reaction(Cancel)
                flag = False

            elif len(args) == 3:
                #! 自由文なし処理
                if re.compile(r'\d+').search(args[2]):
                    limit = args[2]
                    bot_message = await message.channel.send(
                        f'@here {args[1]}で{args[2]}人募集中です'
                    )
                    await bot_message.add_reaction(OK)
                    await bot_message.add_reaction(NO)
                    await bot_message.add_reaction(Cancel)
                    flag = False

            else:
                return

        else:
            await message.channel.send('募集中の要項があります')
            return


    # TODO: !ah 処理
    if args[0] == '!ah':
        await message.channel.send(embed = help)


    #TODO: !re 処理
    if args[0] == '!atre':
        await message.channel.send('リセット処理を実行')
        re.X = False
        re.A = False
        flag = True


#? リアクション処理
@client.event
async def on_raw_reaction_add(reaction):
    global flag


    #! Cancelボタン処理
    if reaction.emoji.name == Cancel:
        if re.X == True:
            await bot_message.edit(content='募集が中止されました')
            await bot_message.clear_reaction(OK)
            await bot_message.clear_reaction(NO)
            await bot_message.clear_reaction(Cancel)
            re.X = False
            re.A = False
            flag = True
        else:
            re.X = True


    #!OKボタン処理
    if reaction.emoji.name == OK:
        if re.A == True:
            mem = int(args[2])
            mem = mem - 1
            args[2] = str(mem)
            await bot_message.edit(content=f'@here {args[1]}で{args[2]}人募集中です')
            if args[2] == '0':
                await bot_message.edit(content=f'{args[1]}の募集は終了しました')
                await bot_message.clear_reaction(OK)
                await bot_message.clear_reaction(NO)
                await bot_message.clear_reaction(Cancel)
                re.A = False
                re.X = False
                flag = True
        else:
            re.A = True


    #! NOボタンの処理
    if reaction.emoji.name == NO:
        if args[2] == limit:
            return
        else:
            mem = int(args[2])
            mem = mem + 1
            args[2] = str(mem)
            await bot_message.edit(content=f'@here {args[1]}で{args[2]}人募集中です')


client.run(TOKEN)
