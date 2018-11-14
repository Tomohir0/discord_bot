import discord
from discord.ext import commands
import pprint
import random
import os
import qrcode
import pickle

#import boto3
#bucket_name = "tomo-discord"
#s3 = boto3.resource('s3')
## s3連携


class Exp():
    "いろいろ説明するための関数を集めたよ！"

    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True, description='sourceは https://github.com/Tomohir0/discord_bot/blob/master/shinma.py を確認してください。')
    async def new(self,ctx: commands.Context):
        """最近の更新情報をお知らせします。"""
        if ctx.invoked_subcommand is None:
            m_new = ("Nov,14:神魔報告に音声読み上げモードを追加！「神魔tts」と入力してみて！PCにしか対応していなくて、VCの有無にかかわらずPCでdiscord開いている全員に読み上げ音声が届いてしまうけども！")
            m_old=("Nov,6:ただいま！"
                    "\nNov,5:note関連で追加要素多すぎるからまた改めて！"
                    "\nNov,4:QRcode実装！botっぽい！"
                    "\nNov,3:神魔登録を含めて少しずつ更新！よりスマートに！notes関連での関数も大分増えた！game関連も少しずつ増えていくかな？"
                    "\nNov,3:new関数を更新。新しい関数のhelpを表示するように。command内での入力を受付可能に！やったぜ！自害プログラムも完備だ！"
                    "\nNov,2:botが暴走……。tokenの取り扱いをlocalにして外部からは手が届かないように……(すごく今さら……)。ごめんなさい……。"
                    "\nNov,2:early returnをいまさら導入。無駄な深さが軽減。その他バグ修正など。"
                    "\nNov,2:cogを導入！開発側としては大分大きいけど、使い手としては関数に分類が付いたくらいかな？callrandをとりあえず追加！メモをランダムに開いちゃおう！王様ゲーム的なのも作れそうかも？"
                    "\nNov,1:長かったからcall_labels=>labelsに変更したよ！役職関連の関数をこれで完備だ！これでお休み一目瞭然！tmp_uoとtmp_dlは内部関数に。")
            await self.bot.say(m_new)
            await self.bot.say("\n\n過去の更新情報については https://github.com/Tomohir0/discord_bot/blob/master/README.md ")

    @new.command(pass_context=True, sub="func")
    async def new_func(self,ctx):
        new_funcs = ["callr", "dels", "sudo_dels", "sel_c", "notes"]
        for func in new_funcs:
            ctx.message.content = "?help " + func
            await self.bot.process_commands(ctx.message)

    @commands.command(pass_context=True)
    async def exp_emerg(self,ctx: commands.Context):
        "emergency(緊急事態)にそなえての説明。"
        m = ("先日の暴走を受けて。自害プログラムとして「?bot_kick」「?bot_logout」を実装しました。"
             "このbotが乗っ取られたと判断された場合には即座に「?bot_kick」を入力してください。全serverでこのbotのmessageを削除し、直ちにkick、logoutを行います。"
             "\nまた、乗っ取りの際に用いられる「@ everyone」が2つ以上含まれたmessageがbot自身から発された場合、bot自らの判断のもと「?bot_kick」を起動します。")
        await self.bot.say(m)
    
    @commands.command(pass_context=True)
    async def exp_note(self, ctx, number:int):
        "note関連のお知らせをまとめました。指定した番号の説明を表示します。"
        ms=[] # messageのlistを用意
        ms.append("基本的には今まで通り「?notes <label名> <内容>」でmemoを保存して「?calls <label名>」でそのmemoを読み出すことができます。"
            "\n「?labels」でserverに存在するmemoのlabel一覧を見ることができます。新たに追加された機能としては削除関数「?dels」があります。"
            "\n「?dels <label名>」でそのmemoを削除することが**できるかもしれません**。また、今回よりsudo版も一部関数に実装されましたが、bot_ownerを除き利用はできないのでご了承ください。")
        ms.append("「?notes」でmemoを保存する際、すでにそのlabel名が使用されていた場合には「上書き/付け足し/前に付け足し/label変更/キャンセル」を選択できるようになりました。"
            "\nそれに付随して、label名が重複した場合に尋ねることなくはじめから「上書き/付け足し/前に付け足し」のいずれをするか定められている互換関数「?notew/?notea/?notef」を用意しました。"
            "\nmemoを書き換え続けたいなら「?notew」を、memoを延々と長くしたいなら「?notea」または「?notef」をご利用ください。")
        ms.append("label名を覚えきれていない場合の補助として、label一覧を見てからlabelを選択できるselcet ver.も用意しました。"
            "\n「?sel_c」で入力したlabelによって「?calls」を、「?sel_d」なら「?dels」を起動できます。")

        await self.bot.say(ms[number])


def setup(bot):
    bot.add_cog(Exp(bot))
