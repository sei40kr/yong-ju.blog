---
title: "Doom Emacs を使おう"
date: 2020-09-03T22:16:20+09:00
---

この記事は [Emacs を使おう]({{< ref "lets-start-using-emacs" >}}) の続編である。前回の記事では Vimmer も Emacs を使うべき理由を説明しているので是非見て頂きたい。

# Emacs のディストリビューション

「Emacs を 1 からカスタマイズをするのが面倒くさい」という人のために Emacs にはコミュニティによってメンテナンスされているディストリビューションがいくつか存在する。

|                                                      | Star 数 | コミット数 |
| :--------------------------------------------------- | ------: | ---------: |
| [Spacemacs](https://www.spacemacs.org)               |   20.5k |      11047 |
| [Prelude](https://prelude.emacsredux.com/en/latest)  |    4.4k |       1370 |
| [Doom Emacs](https://github.com/hlissner/doom-emacs) |    7.7k |      14304 |

これらは外部パッケージの列挙を含む膨大な Emacs の設定ファイルだ。無論そこに自分の設定を加えて更にカスタマイズすることもできる。

# Doom Emacs

自分は Emacs のディストリビューションとして Doom Emacs をオススメする。Doom Emacs の魅力をいくつかご紹介しよう。

[hlissner/doom-emacs: An Emacs framework for the stubborn martian hacker](https://github.com/hlissner/doom-emacs)

- author である Henrik Lissner の高頻度なコミットとリファクタリングの徹底により、小さいコミュニティであるにも関わらず機能と品質で Spacemacs を圧倒している
- Spacemacs の素晴らしいコンセプトを受け継いでいる
  - **Mnemonic → キーバインドが覚えやすいこと**
  - **Discoverable → キーバインドが発見可能であること。** ほとんどのキーバインドは Space から始まり、困ったときは Space を押すとガイドが表示される。コマンドからキーバインドを逆引きすることも可能だ。
  - **Consistent → キーバインドが一貫していること**
  - **Crowd-configured → コミュニティ開発であること**
- Doom Emacs のカスタマイズは `~/.doom.d` 内に記述してバージョン管理できる
- Spacemacs と比べ起動速度が速い
- Spacemacs と異なり、外部パッケージのバージョンをコミットレベルで固定しているので、アップデートで Doom Emacs 側の設定や他のパッケージとの協調動作が壊れることがない
- Native Compilation に対応しており Emacs Lisp を予めバイトコードにコンパイルすることにより、起動速度だけではなく実行速度まで高速化できる

# Doom Emacs のモジュールシステム

Doom Emacs のインストール方法は公式のマニュアルとインストーラが充実しているので割愛する。

[doom-emacs/getting_started.org at develop · hlissner/doom-emacs](https://github.com/hlissner/doom-emacs/blob/develop/docs/getting_started.org)

Doom Emacs の設定の基本となるのがモジュールとフラグだ。 `~/.doom.d/init.el` に有効化するモジュールとそのモジュール固有のフラグを設定していく。

```emacs-lisp
(doom! :lang
       (python
        +lsp
        +poetry))
```

これは Python 開発に必要なパッケージと言語サーバのサポート ( `+lsp` ), Poetry サポート ( `+poetry` ) に必要なパッケージを使うことを宣言している。Vim からのお引越しであれば

```emacs-lisp
(doom! :editor
       (evil +everywhere))
```

も有効化しておこう。 `+everywhere` はファイラなどのツールバッファなどでも evil-mode をサポートするためのフラグだ。

この設定を保存した後に

```sh
~/.emacs.d/bin/doom sync
```

を実行するとまだインストールされていないパッケージがインストールされる。

利用可能なモジュールはここに列挙されている。

[doom-emacs/modules.org at develop · hlissner/doom-emacs](https://github.com/hlissner/doom-emacs/blob/develop/docs/modules.org)

既に非常に多くの開発言語がサポートされている。これら全てのモジュールに深い知識で携わっている Henrik Lissner さんの凄さも伺える。

# まとめ

Emacs というとそれだけでかつての Vim 仲間に拒絶される。エディタ沼は踏み込むとヤバいというのが周囲のエンジニアの認識であり、自分が「ランチ会でエディタについて語りまーす」と発言すると**ランチ会が中止になる。**「既存のパッケージでは満足できなくなりパッケージの自作で無限に時間が溶ける」より前の段階は沼ではないので安心してほしい。

辛いことはたくさんあったが Doom Emacs は本当にいいエディタなので使ってほしいし支えてほしい。
