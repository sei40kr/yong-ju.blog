---
title: "Emacsを使おう"
date: 2020-09-03T01:00:56+09:00
categories: ["開発環境"]
tags: ["開発環境", "エディタ", "Emacs"]
---

Vim vs Emacs論争においては永い時を経て、大半のユーザーがVim側に傾きつつある。
Vimの独自キーバインドの根幹となる「カウント + テキストオブジェクト + オペレータ」のアイデアの素晴らしさや、Vimスクリプトの既存資産の充実度を私は評価している。
それでもなお私がEmacsを人に奨める理由を、よくあるEmacsへの誤解を解きつつこの記事で解説していく。

## Emacsに対する誤解

### 誤解: Vimのキーバインドが使えない

Emacsにおいても、[Evil](https://melpa.org/#/evil)を使うことで**EmacsでVimのキーバインドが使える。**

EvilがVimキーバインドをサポートする範囲はテキスト編集のみに留まらない。
[evil-collection](https://melpa.org/#/evil-collection) はファイラやMagitなど、あらゆるツールバッファにおけるVimキーバインドをサポートする。

{{< hint info >}}
Evilは完全にVimのキーバインドを再現している訳ではなく、一部のキーバインドが微妙に異なる。
使う頻度が高いキーにおける差分を列挙する。

| モード   | キー    | Vimの動作                                                               | Evilの動作                   |
|-------|-------|-----------------------------------------------------------------------|---------------------------|
| 挿入 | `C-h` | Backspace                                                             | ヘルプの表示                    |
| 選択 | `S`    | 選択範囲を囲む ( [surround.vim](https://github.com/tpope/vim-surround) 使用時 ) | セレクトモード (「選択範囲を囲む」は `s` ) |

これらの差分もカスタマイズでVimの動作に揃えることができる。
{{< /hint >}}

### 誤解: Vim のコマンドが使えない

いくつかのVimコマンドはEvilにも実装されている。
Vimと同じように、通常モードで `:` を押すと、VimのExコマンドを入力するコマンドラインが表示される。

置換 ( `:s` ) はもちろん、`:sort` や `:read` も完備されており、少なくとも手入力でインタラクティブに実行する分には不足ないと思われる。
また、置換のオプション ( `g` など) のデフォルトをEvilの設定でカスタマイズすることも可能だ。

### 誤解: Vimの既存資産に相当するものがない

EmacsではVim Scriptが動作しないので、「Vimの既存資産をそのまま動かせない」は正しい。
しかし、メジャーなVimプラグインには既に完成度の高い代替プラグインがEmacsに存在している。

| Vim                            | Emacs                   |
|:-------------------------------|:------------------------|
| incsearch.vim                  | evil-mode               |
| vim-expand-region              | expand-region           |
| vim-surround                   | evil-surround           |
| vim-commentary, NERD Commenter | evil-nerd-commenter     |
| vim-multiple-cursors           | evil-mc, evil-multiedit |
| clever-f                       | evil-snipe              |
| easymotion                     | avy                     |
| vim-quickrun                   | quickrun.el             |
| Unite, Denite                  | helm, ivy               |
| vimfiler, Defx                 | Neotree, Treemacs       |

また、以上のプラグインは全て公式にVimキーバインドをサポートしているか、evil-collection (前述) に専用設定が存在しているかのどちらかである。

既にEvilコミュニティは熟していることがお分かり頂けるだろう。

### 誤解: Emacsは遅い

#### Emacsにもプラグインの遅延ロード機構はある

Emacsも大半のVimプラグインマネージャと同じような遅延ロード機構を備えているため、プラグインのロードはそれなりに速い。

#### そもそもEmacsを終了する機会があまりない

そもそもEmacsは [Projectile](https://melpa.org/#/projectile) と [persp-mode.el](https://melpa.org/#/persp-mode) でプロジェクトごとにワークスペースを管理できるため、**終了 (と再起動) する機会があまりない。**
そのため、起動時間の遅さはネックにならない。

また、`emacsclient` を使うと「指定したファイルを現在起動しているEmacsプロセスで開く」こともできる。
よって、シェル作業のエディタとしてEmacsを使う場合も、都度Emacsプロセスを立ち上げる必要がない。

また、[Oh My Zshの emacs プラグイン](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/emacs)では、「起動中のEmacsプロセスが存在すればそれを使用し、存在しなければ新規にプロセスを立ち上げる」ということを行うラッパーを提供している。
これにより、特に意識することなく `emacsclient` の恩恵を受けることができる。

ちなみに、Emacsはヘッドレスモードでも起動できるため、Emacsデーモンをsystemdのユーザーサービスとしてログイン時に起動しておくこともできる。

{{< details title="emacs.service の例" >}}
```ini
[Unit]
Description=Emacs text editor
Documentation=info:emacs man:emacs(1) https://gnu.org/software/emacs/

[Service]
Type=notify
ExecStart=/usr/bin/emacs --fg-daemon
Restart=on-failure

[Install]
WantedBy=default.target
```
{{< /details >}}

#### Emacs 27で Portable Dumper が登場

Emacs 27以降には **Portable Dumper** という機能が追加されている。
Emacs Lispファイルのロード時に評価される箇所を予め評価しておき、起動時にPortable Dumperによってその評価結果をメモリ上に展開することで、**起動時に読み込むEmacs Lispファイルのロード時間を大幅に短縮する。**

参考: [portable dumper: アーキテクチャに依存しない Emacs の起動時間短縮手法](https://gist.github.com/t-sin/911d192dac926bf06c2a750083855fc8)

#### Emacs 28で Native Compilation が登場

Emacs 28移行には **Native Compilation** という機能が追加されている。
Emacs Lispをネイティブバイナリにコンパイルすることで、**Emacs Lispの実行パフォーマンスを大幅に向上させる。**

## Emacs を使うべき理由

ここまでEmacsのネガティヴな噂に対して、その誤解を解いてきた。
ここからは、Emacsならでは機能というポジティブな面に注目していく。

### グラフィカルな UI

Emacsには公式のGUIインターフェイスが付属する。

EmacsのGUIはターミナルで起動したEmacsをウィンドウで囲ったなんちゃってGUIではない。
ファイラから画像ファイルを開いて表示できるし、Markdown中のLaTeXフラグメントのプレビューもできる。

### Org

EmacsにはOrgと呼ばれるMarkdownのようなマークアップ言語が存在する。

OrgはMarkdownより遥かに多くの機能をサポートする:

- TODO & スケジュール管理機能
- 時間管理機能
- 表計算機能
- コードの埋め込み
- コード実行結果の埋め込み
- HTML や LaTeX, PDF へのエクスポート

参考: [Org mode for Emacs: あなたの生活をプレーンテキストで](https://www.orgmode.org/ja)

### TRAMP

Emacsには **TRAMP** という、**リモートのファイルシステムをまるでローカルであるかのように扱う**機能がファイルシステムレベルで実装されている。
TRAMPはシェルコマンドを介してリモートのファイルシステムにアクセスするため、シェルにアクセスできる環境であれば、**Dockerコンテナ内だろうとVagrantインスタンスの中だろうと、まるでローカルのようにアクセスできる。**
(注: Dockerコンテナ内へのアクセスは [docker-tramp](https://melpa.org/#/docker-tramp), Vagrantインスタンス内へのアクセスは [vagrant-tramp](https://melpa.org/#/vagrant-tramp) が必要)

また、アクセスにroot権限が必要なファイルもTRAMPでアクセスできるため、「`sudo` でエディタを開くとバニラ状態のエディタを使わされる」という問題も起きない。

### Magit

Emacsのプラグインの一つに **Magit** と呼ばれる超強力なGitクライアントがある。
Magitは、**Gitのあらゆる操作を分かりやすいインターフェイスと強力な補完でサポートしてくれる。**
もちろん、全てVimキーバインドで操作が可能だ。

MagitだけでもEmacsを使う価値は十分にあると言える。

参考: [A Git Porcelain inside Emacs](https://magit.vc)

## まとめ

Emacsの魅力が少し分かって頂けただろうか。

せっかく興味をもって頂いても「また一から新しいエディタをカスタマイズするのは億劫だ」と思うかもしれない。
別記事で、**既にカスタマイズされたEmacsディストリビューションの利用**について書いたので是非読んでほしい。

続編: [高品質EmacsディストリビューションDoom Emacsを使おう]({{< ref "doom-emacs" >}})
