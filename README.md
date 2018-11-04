# はじめに
このdirectoryはTom-O-HEROがdiscord_botを作成・実験する場です。

# 各ソースについて
- shinma.py | 神魔速報や挨拶などを行う。主役。
- note.py,tool.py,sinoalice.py,system.py | cog用のfile
- Procile, requirements.txt, runtime.txt | heroku用のテキスト
- test.py | 実験用。
- hello.py | 挨拶を行う。最初に作ったbot。今では放置。


# update
- 細かい修正は随時。

# Nov,3
- 神魔登録を含めて少しずつ更新！よりスマートに！notes関連での関数も大分増えた！game関連も少しずつ増えていくかな？
- new関数を更新。新しい関数のhelpを表示するように。command内での入力を受付可能に！やったぜ！自害プログラムも完備だ！
# Nov,2
- botが暴走……。tokenの取り扱いをlocalにして外部からは手が届かないように……(すごく今さら……)。ごめんなさい……。
- early returnをいまさら導入。無駄な深さが軽減。その他バグ修正など。
- cogを導入！開発側としては大分大きいけど、使い手としては関数に分類が付いたくらいかな？callrandをとりあえず追加！メモをランダムに開いちゃおう！王様ゲーム的なのも作れそうかも？
# Nov,1
- 長かったからcall_labels=>labelsに変更したよ！役職関連の関数をこれで完備だ！これでお休み一目瞭然！tmp_uoとtmp_dlは内部関数に。
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

# memo
　discordでの豆知識。`_a_`のように囲むことで文字を修飾できる。また、GitHubの```によるcode block表記も可能。
- _,*:italic
- **:bold
- ***:bold and italic
- __:underline
- ___:italic and underline