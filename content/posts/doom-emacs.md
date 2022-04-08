---
title: "高品質EmacsディストリビューションDoom Emacsを使おう"
date: 2020-09-03T22:16:20+09:00
categories: ["開発環境"]
tags: ["開発環境", "エディタ", "Emacs", "Doom Emacs"]
---

この記事は [Emacsを使おう]({{< ref "lets-start-using-emacs" >}}) の続編である。
前回の記事ではVimmerにもEmacsをオススメする理由を説明しているので是非一読して頂きたい。

## Emacsのディストリビューション

「Emacsを1からカスタマイズをするのが面倒くさい」という人のためにEmacsにはコミュニティによってメンテナンスされているディストリビューションがいくつか存在する。

|                                                      | Star 数 | コミット数 |
|:-----------------------------------------------------|--------:|-----------:|
| [Spacemacs](https://www.spacemacs.org)               |   20.5k |      11047 |
| [Prelude](https://prelude.emacsredux.com/en/latest)  |    4.4k |       1370 |
| [Doom Emacs](https://github.com/hlissner/doom-emacs) |    7.7k |      14304 |

これらの実体はプラグインの列挙を含む膨大なEmacsの設定ファイル ( `.emacs.d` ) だ。
もちろん、そこに自分の設定を加えて更にカスタマイズすることもできる。

## Doom Emacs

この記事ではEmacsのディストリビューションとしてDoom Emacsをオススメする。
Doom Emacsの魅力をいくつかご紹介しよう。

![Doom Emacs](/img/doom-emacs.png)

[hlissner/doom-emacs: An Emacs framework for the stubborn martian hacker](https://github.com/hlissner/doom-emacs)

- authorであるHenrik Lissnerの高頻度なコミットとリファクタリングの徹底により、小さいコミュニティであるにも関わらず機能と品質でSpacemacsをする
- Spacemacsの素晴らしいコンセプトを受け継いでいる
  - **Mnemonic, 覚えやすいキーバインド**
  - **Discoverable, 発見可能なキーバインド。**
    ほとんどのキーバインドは `SPC` から始まり、困ったときは `SPC` を押すとガイドが表示される。
    コマンドからキーバインドを逆引きすることも可能。 ( `SPC :` )
  - **Consistent, 一貫したキーバインド**
  - **Crowd-configured, コミュニティ開発**
- Doom Emacs独自の素晴らしい設計思想のもと設計されている
  - **Gotta go fast, スタートアップ時間とランタイムパフォーマンスの両方を最適化。**
    Spacemacsと比べスタートアップ時間が短い。
  - **Nix/Guix is a great idea!, 宣言的で再現性のあるパッケージ管理。**
    全てのプラグインはコミットハッシュで固定されており、プラグインの最新revisionのアップデートがDoom Emacsの設定や他のプラグインとの強調動作を壊すことがない。
    また、Emacs 28のnative compilationにも対応する。
- Doom Emacsのカスタマイズは `~/.doom.d` 内に記述してバージョン管理できる

## Doom Emacsのインストール

Doom Emacsのインストール方法は、公式のマニュアルとインストーラが充実しているため割愛する。

[doom-emacs/getting_started.org at develop · hlissner/doom-emacs](https://github.com/hlissner/doom-emacs/blob/develop/docs/getting_started.org)

## Doom Emacsのモジュールシステム

Doom Emacsの設定の基本となるのがモジュールとフラグだ。
`~/.doom.d/init.el` に、有効化するモジュールとモジュール固有のフラグを設定していく。

```emacs-lisp
(doom! :lang
       (python
        +lsp
        +poetry))
```

これはPythonのサポートに加え、言語サーバのサポート ( `+lsp` ) 及び Poetry サポート ( `+poetry` ) を有効にすることを宣言している。

Vimからのお引越しであれば、Doom EmacsでVimのキーバインドが使えるよう `:editor evil` モジュールを有効化しよう。

```emacs-lisp
(doom! :editor
       (evil +everywhere))
```

`+everywhere` フラグは、ファイラなどのツールバッファでもVimのキーバインドが使用できるようにするためのものだ。

この設定を保存した後に

```sh
~/.emacs.d/bin/doom sync
```

を実行すると、まだインストールされていないパッケージがインストールされる。

利用可能な全てのモジュールは [docs/modules.org](https://github.com/hlissner/doom-emacs/blob/develop/docs/modules.org) に列挙されている。

Doom Emacsは既に非常に多くのプログラミング言語や開発ツールがサポートしている。
これら全てのモジュールに深い知識で携わっているHenrik Lissnerさんの凄さが伺える。