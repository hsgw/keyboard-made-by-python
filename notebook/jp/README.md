![top](../imgs/keyboard_made_by_python.jpg)

# Pythonだけでキーボードを作る

こんにちは。hsgwです。   
毎年、アドベントカレンダーの記事では役に立つtipsを投稿することにしています。

今年はPythonだけでキーボードを設計する方法を紹介します。

# TL;DR
- ファームウェアだけでなく、回路図(ネットリスト)や基板、ケースを全てPythonで設計する   
- 設計の流れを主に紹介する (細かいコードについてはドキュメントとソースを読んで下さい)
- 設計したコードをjupyter notebook(google colaboratory)で実行できる形で解説する   
- 主に使用するライブラリは以下の通り

|            |ライブラリ|
|------------|-----|
|回路図       |[skidl](https://github.com/devbisme/skidl)|
|基板         |[pcbflow](https://github.com/michaelgale/pcbflow) ([folkしたリポジトリ](https://github.com/hsgw/pcbflow/tree/fix_kicad))|
|ケース       |[cadquery](https://github.com/CadQuery/cadquery)|
|ファームウェア|[KMK Firmware](https://github.com/KMKfw/kmk_firmware), [circuitpython](https://circuitpython.org/)|

# なぜPythonでキーボードを作るのか
[Python](https://www.python.org/)はプログラミング言語のひとつです。実用的なプログラムを簡単に読みやすく書くことを重視して作られています。

もちろんそれだけでなく、ありとあらゆるライブラリによって拡張され、複雑な計算や画像認識、機械学習といったコンピュータらしい振る舞いだけでなく、ゲームでも音楽でも絵でもなんでも作れます。
AIと名がつくものには大抵使われていますし、最近巷を騒がしている画像生成AIもPythonで動いています。

例外にもれず、回路図を書くためのライブラリや基板を配線するライブラリ、3Dモデルを作るライブラリもありますし、実際にマイコンを動かすのもPythonで書かれたライブラリです。

Pythonに限らず`コードを書くこと`で`何かを設計する`利点は、設計が文字ベースの情報であることです。
特殊な事柄(回路図記号など)を意識せずにテキストエディタだけで理解・設計が可能です。
他の誰かと共同編集するときもgitの強力なバージョン管理や差分抽出が使えるのでスムーズです。

そして、その設計のためのコードはプログラムなので複雑な計算や同じ値や部分の繰り返しをコンピュータにまかせましょう。間違いが少なくなって変更も容易です。

# コードと解説
以下のリンクをクリックするとgoogle colaboratoryで実行できるコードと解説を開きます。

ケース編は環境の都合で[binder](https://mybinder.org)を使用します。これも同じような実行環境です。

- [google colaboratoryとは]()
- [基板を設計する](https://colab.research.google.com/github/hsgw/keyboard-made-by-python/blob/main/notebook/jp/pcb.ipynb)
- [ケースを設計する](https://mybinder.org/v2/gh/hsgw/keyboard-made-by-python/HEAD?labpath=notebook%2Fjp%2Fcase.ipynb) ※ [binder](https://mybinder.org)で開きます。表示するのに時間がかかるかもしれません
- [ファームウェアを書く]() 

# 最後に
今年はLainのGBの発送をしたぐらいでドタバタした一年でした。半導体・部品不足も円安も収まりそうなので、来年はのんびりキーボード出来ればいいなと思っています。    
良いお年を！

// この記事はcasasagi+3Dプリントケースで書きました