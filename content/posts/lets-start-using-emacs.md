---
title: "Emacs を使おう"
date: 2020-09-03T01:00:56+09:00
categories: ["開発環境"]
tags: ["エディタ", "Emacs"]
---

## Vimmer が Emacs を嫌う理由とそれに対する弁明

### Emacs キーバインドで小指が損傷

evil-mode を使うことで Emacs で Vim のキーバインドが使える。

それでも evil-mode のことをよく思わない Vimmer も多い。

[我が evil-mode を嫌いな理由 〜evil-mode の闇〜](https://www.slideshare.net/Shougo/evilmode-evilmode)

テキスト編集は Vim キーバインドだが、あらゆるところで Emacs キーバインドが残っている。基本的に evil-mode は Emacs のキーバインドを上書きするので Vim で定義されていないキーは Emacs のキーバインドがそのまま残っている。

[emacs-evil/evil-collection](https://github.com/emacs-evil/evil-collection)

恐らく標準設定で困るのは以下の 2 つだろう。

1. 挿入モードでは `C-h` は Backspace ではなくヘルプ
2. surround のマッピングが `S` ではなく `s`

いずれもカスタマイズで解決可能だ。

### Vim のコマンドが使えない

ほとんどの Vim コマンドは evil-mode に実装されており Vim と全く同じ方法で呼び出すことができる。

`:sort` や `:read` も完備されており一定以上のレベルの Vimmer でも事足りるのではないだろうか。また設定することで「 `:s` の `g` オプションをデフォルトで有効にする」など細かい挙動の変更も可能だ。

### Vim の資産が使えない

Emacs では Vim Script が動かないのでこれは正しい。しかし大抵の場合、既に完成度の高い代替パッケージが存在している。以下で紹介するパッケージは全て公式に evil-mode に対応しているか evil-collection に evil-mode で使うための設定が存在する。

- incsearch.vim → evil-mode に標準搭載
- vim-expand-region → expand-region
- vim-surround → evil-surround
- vim-commentary, NERD Commenter → evil-nerd-commenter
- vim-multiple-cursors → evil-mc, evil-multiedit
- clever-f → evil-snipe
- easymotion → avy
- vim-quickrun → quickrun.el
- Unite, Denite → helm, ivy
- vimfiler, Defx → Neotree, Treemacs

既に Emacs + evil-mode 使いのコミュニティは熟していることがお分かり頂けるだろう。

### Emacs は Vim と比べ起動が遅い

これも 2020 年現在 stable である Emacs 26 においては正しい。

しかし Emacs は Projectile というパッケージでプロジェクトを管理でき persp-mode.el でワークスペースを管理できるため、そもそも Emacs を終了する機会が滅多にない。

emacsclient を使えば「シェルのコマンドラインから指定したファイルを現在起動している Emacs で開く」といったことも可能だ。emacsclient の使い方は Man ページと Oh My Zsh の Emacs プラグインが参考になる。

[ohmyzsh/emacs.plugin.zsh at master · ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/emacs/emacs.plugin.zsh)

尚、Emacs はヘッドレスモードでも起動でき、OS へのログインと同時にバックグラウンドで Emacs のデーモンを起動しておくことも可能だ。

更に Emacs 27 以降には Portable Dumper といった起動時間を短縮する機能が追加されている。パッケージの Emacs Lisp ファイルはほとんどが遅延ロードされ、遅延ロード不可能な部分は Portable Dumper によって解釈済みのものをメモリ上に展開するので起動が早くなる。

[portable dumper: アーキテクチャに依存しない Emacs の起動時間短縮手法](http://lc.linux.or.jp/lc2002/papers/nagano0920h.pdf)

## Emacs を使うべき理由

もちろん Emacs に乗り換えるメリットもたくさんある。

### グラフィカルな UI

Neovim をグラフィカルな UI で扱うための gonvim というプログラムが存在する。

一方 Emacs は GUI モードでの起動を公式にサポートしている。これはターミナルモードの Emacs をウィンドウで囲ったようななんちゃって GUI モードではない。画像ファイルを開いて表示することもできるし、スペルミスを含む英単語を波線で強調することもできる。Jupyter Notebook と seaborn を使ったデータの可視化も Emacs だけで完結することができる。

### Org

Emacs には Org と呼ばれる Markdown のようなマークアップ言語が存在する。

[Org mode for Emacs: あなたの生活をプレーンテキストで](https://www.orgmode.org/ja)

- TODO & スケジュール管理機能
- 時間管理機能
- 表計算機能
- コードの埋め込み
- コード実行結果の埋め込み
- HTML や LaTeX, PDF へのエクスポート

などの機能があり、マークアップ言語として大変高機能だが、デメリットもあり

- Markdown と比べて普及していない
- Org の編集機能を有するエディタが Emacs しか存在しない

と考えると個人利用に留めるのが現実的だろう。(全員 Emacser というチームでなければ)

### TRAMP

Emacs には TRAMP と呼ばれるリモートのファイル操作を SSH 経由で行う機能がファイルシステムレベルに組み込まれている。これによりリモートのファイルをローカルにあるファイルのように編集することが可能だ。

また、編集に root 権限が必要なファイルも TRAMP 経由でアクセスできるので「root でシステムファイルを編集しようとするとユーザコンフィグで設定した機能が全て使えない」という問題も発生しない。

### Magit

Emacs のパッケージの 1 つに Magit と呼ばれる超高機能な Git クライアントがある。もちろん全機能が Vim のキーバインドで利用可能だ。Magit を介した Git の操作だけでも Emacs を使う価値は十分にある。

[A Git Porcelain inside Emacs](https://magit.vc)

## まとめ

Emacs の魅力が少し分かって頂けただろうか。せっかく興味をもって頂いても「また 1 からエディタをカスタマイズするのは面倒だ」と思われるかもしれない。そこで別の記事で「既にカスタマイズされた超高機能 Emacs ディストリビューション Doom Emacs」について書こうと思う。

続編: [高品質EmacsディストリビューションDoom Emacsを使おう]({{< ref "doom-emacs" >}})
