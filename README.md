# はじめに
このdirectoryはTom-O-HEROがdiscord_botを作成・実験する場です。

# 各ソースについて
:shinma.py| 神魔速報や挨拶などを行う。主役。
:note.py,tool.py,sinoalice.py,system.py|cog用のfile
:Procile, requirements.txt, runtime.txt| heroku用のテキスト
:test.py| 実験用。
:hello.py| 挨拶を行う。最初に作ったbot。今では放置。


# update
- 細かい修正は随時。

## Oct,31
- ファイルベースをjsonからpickleに！今までのスピードが帰ってきたぜ！！
- tmp_upとtmp_dlのときのみS3とやり取りするんだよ！効率的！新しい関数はないけど、毎回出してるとややこしいもんね！
- 役割を忘れすぎているから神魔botに無理やり神魔を思い出させたよ！限定的にpickle復活！
- s3連携完了だああああ！これでbotを更新してもdataが消えることはなくなったああ！fixし放題だね！
- その代わり、ちょっと反応遅くなっちゃったけど許してほしいな……)call_labelsも実装したよ！
- ctx実装。役職機能実装(server側の変更も必要)。absentを使って役職をAbsentに。role_reset_allで戻せるから安心して！
- S3とHerokuの連携を図りたい……。
## Oct,30
- pickle実装できたけれど、結局server起動ごとに変数は消えてしまう……。でもserverで共有できるメモ機能のnotesとcallsを実装したよ。
## Oct,29
- ch_listの一時削除。noteやcallを追加。pickle実験したいなー
## Oct 28,2018
- bot.commandも実装。rollなどを行えるように。VCチャンネルのメンバーリストも取得可能に。(現状ではsource内にチャンネルidを記載する形で指定)
- ch_listやvc_randを追加。各commandのdescriptionを充実。セリフを感情豊かに
## Oct 27,2018
- 作成。神魔登録機能や簡単な挨拶機能を備える。
- 呼応反応を充実。