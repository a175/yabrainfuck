# yabrainfuck
Yet another brainfuck implementation

## 説明
`BrainFuckVM`はBrainFuckの中間コードを動かす仮想マシンのクラス,
`BrainFuckCompilier`はテキストで書かれたコードを中間コードにコンパルするコンパイラです.
例えば, いわゆるHelloWordプログラム
`++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.`
を走らせるには以下のように行います:
```
import brainfuck
bfvm= brainfuck.BrainFuckVM()
bfc = brainfuck.BrainFuckCompilier(bfvm)
codetorun = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
codelist = bfc.get_codelist_from_text(codetorun)
bfvm.set_codelist(codelist)
bfvm.run()
```
デフォルトのコンパイラ`BrainFuckCompilier`は,
現状構文の解釈はしません.
また,
文字コードが16進数で0xUVWXYZであるとき,
`5Z+4Y+3X+2W+V`を8で割った余りを求め,
それにより中間コードを作ります.
したがって, この値が等しい文字に置き換えても, 同じ中間コードを出力します.
なお, これは, 今の所ホワイトスペースや改行コードも例外ではありません.

例えば, Hello World
```
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```
は, ルーン文字を使って
```
ᚣᚷᚿᛗᛟ᛫ᚫᚿᛇᛚ᛫ᚣᚷᛃᛓᛦᚣᚷᛆᛋᛟ᛫ᚦᚷᛋᛗᛦᚣᚰᛄᛐᛤ᛭ᚩᚺᛋᛚ᛫ᚦᚹᛆᛒᛟᛯᚬᚽᛌᛙᛩᚦᚺᛊᛚᛥᚥᚱᚾᛗᛟ᛫ᚫᚿᛋᛗᛪᚪᚷᛃᛗᛢᛮᚮᚾᛌᛙᛪᚬᚶᛋᛗᛣᚢᚱᛅᛍᛥ᛭ᚭᚾᛍᛙᛥᚥᚹᛅᛑᛥᚢᚮᛆᛋᛞᛮᚫᚷᛊ
```
ともかけます.
例えば梵字を使って以下のように書くこともできます.
```
𑖅𑖑𑖥𑖭𑖍𑖥𑖭𑖍𑖝𑖀𑖍𑖙𑖭𑖍𑖝𑖨𑖅𑖙𑖨𑖅𑖙𑖥𑖈𑖑𑖥𑖅𑖔𑖥𑖮𑖎𑖦𑖮𑖏𑖟𑖨𑖍𑖜𑖭𑖈𑖛𑖨𑖈𑖙𑖩𑖆𑖗𑖦𑖇𑖗𑖠𑖀𑖐𑖜𑖇𑖏𑖛𑖬𑖍𑖙𑖭𑖍𑖙𑖥𑖅𑖘𑖤𑖅𑖙𑖥𑖄𑖔𑖠𑖄𑖎𑖧𑖬𑖎𑖤𑖭𑖍𑖙𑖬𑖏𑖛𑖧𑖇𑖛𑖧𑖄𑖓𑖧𑖇𑖓𑖧𑖇𑖏𑖧𑖄𑖔𑖜𑖭𑖌𑖜𑖭𑖍𑖘
```
また, 書体の異なるAを使った以下のものでも同じコードを吐きます.
```
𝓐𝓐𝓐𝓐𝓐𝓐𝓐𝓐𝐀𝖠𝓐𝓐𝓐𝓐𝐀𝖠𝓐𝓐𝖠𝓐𝓐𝓐𝖠𝓐𝓐𝓐𝖠𝓐𝜜𝜜𝜜𝜜A𝙰𝖠𝓐𝖠𝓐𝖠A𝖠𝖠𝓐𝐀𝜜𝙰𝜜A𝙰𝖠𝖠𝔄𝖠AAA𝔄𝓐𝓐𝓐𝓐𝓐𝓐𝓐𝔄𝔄𝓐𝓐𝓐𝔄𝖠𝖠𝔄𝜜A𝔄𝜜𝔄𝓐𝓐𝓐𝔄AAAAAA𝔄AAAAAAAA𝔄𝖠𝖠𝓐𝔄𝖠𝓐𝓐𝔄
```

これらは, `BrainFuckCompilier` のもつ, 
中間コードをプログラムに変換する`get_equivalent_code_text`を使えば,
以下のような感じで得られます.
```
import brainfuck
bfvm = brainfuck.BrainFuckVM()
bfc = brainfuck.BrainFuckCompilier(bfvm)
codetorun = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
codelist = bfc.get_codelist_from_text(codetorun)
candidates = [ chr(i) for i in range(0x16A0,0x16F0+1)]
translatedcode = bfc.get_equivalent_code_text(codelist,candidates,15)
print(translatedcode)
```
`candidates`は使用する文字のリストです.
この例では, ルーン文字をリストとして与えています.
`15`という部分を`0`にすると,
いつも`candidates`の先頭から使用する文字の候補を検索します.
それだと同じ文字が並ぶことが多いので,
1命令ごとに検索する場所を変えたいときには,
値を設定します.


