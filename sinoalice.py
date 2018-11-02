import discord
from discord.ext import commands
import pprint
import os
import pickle
import random

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携

class Sinoalice():
    "sinoaliceで役に立ちそうな関数を集めたよ！神魔報告関連は別にあるよ！ただし、役職に関してはアイコンの丸を灰色以外にしないと機能しません。"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='「?vc」で「コロシアムVC」の参加メンバーの(ニックネームではない)名前一覧が得られます。')
    async def vc(self):
        "「コロシアムVC」の参加メンバーの名前一覧を表示します。"
        channel = self.bot.get_channel("413951021891452932")
        if len([member.name for member in channel.voice_members]) == 0:
            await self.bot.say("今、" + channel.name + "には一人もいない……一人も……")
        else:
            member_list = pprint.pformat(
                [member.name for member in channel.voice_members])
            # replaceで改行して見やすく
            await self.bot.say(channel.name + "にいるのは\n" + member_list.replace(",", "\n") + "\nだよ！")

    @commands.command(description='「?vc_rand 2」で「コロシアムVC」の参加メンバーから二人を選びます。')
    async def vc_rand(self, num: int):
        "「コロシアムVC」の参加メンバーの中からランダムに指定された人数を選びます。"
        channel = self.bot.get_channel("413951021891452932")
        member_list = [member.display_name for member in channel.voice_members]
        if len(member_list) < num or num < 1:
            await self.bot.say("変だよ！\n今のVCには{}人しかいないのに、人数指定が{}人は変だよ！".format(len(member_list), num))
        else:
            await self.bot.say(random.sample(member_list, num) + "！\n君に決めた！")

    @commands.command(description='「コロシアムやばそう」というときのために。', pass_context=True)
    async def absent(self, ctx: commands.Context):
        "役職を「欠席遅刻予定」に変更します。みんなが把握して調整しやすく。"
        user = ctx.message.author
        role = discord.utils.get(user.server.roles, name="欠席遅刻予定")
        await self.bot.say(user.name + "はお休み、了解！")
        await self.bot.add_roles(user, role)
    '''    if not user in role.members:
            await self.bot.add_roles(user, role)
            await self.bot.say(user.name + "を" + role.name + "に変更しました")
        else:
            await self.bot.say("もうすでに" + role.name + "だよ！")
    '''
    @commands.command(description='「やっぱり出れるわ」というときのために。', pass_context=True)
    async def present(self, ctx: commands.Context):
        "あなたの役職「欠席遅刻予定」を解除します。"
        user = ctx.message.author
        role = discord.utils.get(user.server.roles, name="欠席遅刻予定")
        await self.bot.remove_roles(user, role)
        await self.bot.say(user.name + "はいける、了解！")
    '''
        if user in role.members:role_mentions
            await self.bot.remove_roles(user, role)
            await self.bot.say(user.name + "を" + role.name + "から解除しました")
    '''
    @commands.command(description='コロシアムが終了したら役職を戻しておきましょう。', pass_context=True)
    async def role_reset(self, ctx: commands.Context):
        "役職「欠席遅刻予定」をすべて解除します。"
        user = ctx.message.author
        role = discord.utils.get(user.server.roles, name="欠席遅刻予定")
        for member in user.server.members:
            await self.bot.remove_roles(member, role)
            #await self.bot.say(user.name + "を" + role.name + "から解除しました")
def setup(bot):
    bot.add_cog(Sinoalice(bot))
