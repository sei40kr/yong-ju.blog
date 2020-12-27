---
title: "Linux を普段使いのデスクトップ環境にしよう"
date: 2020-09-07T21:34:10+09:00
---

# Linux を使うことのメリット

- **普段使っているウィンドウマネージャやステータスバー, アプリケーションランチャなどの挙動を自分好みにカスタマイズできる**
- 多くのプログラムの設定がテキストファイルで管理されており、それらをリモートのバージョン管理システムに push することにより、自分のカスタマイズをクラウド上に保存できる。

# どの Linux ディストリビューションを使えばよいか

Linux 上でデスクトップ環境を自分で構築していくのであれば、以下の観点で選ぶのがよい。

1. 可能な限りミニマムな構成のもの。自分で環境を構築していく上でプリインストールされたサービスと競合することを避けたい。また、必要な機能を自分で 1 からインストールすることによってどの機能が何に依存しているのかも分かりやすい。
2. OS 標準のパッケージマネージャが暗黙的に設定をしないこと。必要な機能を自分で 1 から設定することによって仕組みを理解できる。

この 2 つの条件を満たすディストリビューションが以下の 2 つである。

## Arch Linux

- ミニマムな構成
- [ArchWiki](https://wiki.archlinux.jp) に日本語ドキュメントが充実している
- GUI インストーラがないのでインストールが少し難しい。インストールディスクから既にセットアップされた Arch Linux を立ち上げ、その環境でシステムディスクに OS を構成するパッケージ ( `base` ) をインストールしていく。

[インストールガイド - ArchWiki](https://wiki.archlinux.jp/index.php/%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%82%AC%E3%82%A4%E3%83%89)

## NixOS

- ミニマムな構成
- Nix と呼ばれる言語で宣言的に OS の設定やインストールするパッケージの列挙を定義する。 **バージョン管理できる設定の範囲が広がり、バージョン管理した設定ファイルから環境を復元するのも簡単。**
- 公式ドキュメントは充実しているが、知りたい情報を探すのが少し難しい。
- NixOS の魅力や使い方については別の記事で解説する。

# ArchWiki

ArchWiki は Arch Linux の wiki だが OS の留まらずあらゆるプログラムの日本語ヘルプも提供している。特に便利な設定のスニペットや他のパッケージとの協調設定に関する情報が多い。Linux を使っていく上で困ったときは、まず公式マニュアルや Man ページを見て、それでも解決しない場合は ArchWiki を見るといい。

[ArchWiki](https://wiki.archlinux.jp/index.php/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8)

# デスクトップ環境

Linux のデスクトップ環境は以下の要素で構成される。

## ディスプレイマネージャ

ユーザセッションを開始し、指定したスタートアッププログラムを起動するためのプログラム。(e.g. GDM, LightDM) 要するにログイン画面を表示してログイン処理を行うプログラムである。必須ではない。

ユーザセッション開始前に呼び出されるこのプログラムだけは必ず system-wide にインストールする必要がある。

ディスプレイマネージャを使わない場合はセッション開始後にシェルが表示されるので、スタートアッププログラムを起動する場合はインタラクティブシェルの設定 ( `.bashrc` , `.zshrc` ) に記述する。

```bash
# グラフィカルセッションの中でなければ X サーバを起動する
if [[ -z "$DISPLAY" && "$XDG_VTNR" == 1 ]]; then
  exec startx
fi
```

[ディスプレイマネージャ - ArchWiki](https://wiki.archlinux.jp/index.php/%E3%83%87%E3%82%A3%E3%82%B9%E3%83%97%E3%83%AC%E3%82%A4%E3%83%9E%E3%83%8D%E3%83%BC%E3%82%B8%E3%83%A3)

## X サーバ

グラフィカルセッションを開始するためのプログラム。(e.g. startx, xinit) デスクトップ環境を含むグラフィカルなプログラムを開始するためにはディスプレイマネージャの上で起動する必要がある。

## ウィンドウマネージャ

ウィンドウを管理するためのプログラム。(e.g. Xmonad, i3) ウィンドウシステムの操作感はウィンドウマネージャで決まる。

私のオススメは [Xmonad](https://xmonad.org) である。Xmonad は、Haskell というあまり馴染みのない言語ではあるが、 **設定ではなくウィンドウマネージャの実行プログラムそのものを記述する** という点で他のウィンドウマネージャと異なり、カスタマイズの自由度も高い。Xmonad やその他のプログラムを組み合わせて利便性の高いデスクトップ環境を作成する方法は別記事で解説する。

- [ウィンドウマネージャ - ArchWiki](https://wiki.archlinux.jp/index.php/%E3%82%A6%E3%82%A3%E3%83%B3%E3%83%89%E3%82%A6%E3%83%9E%E3%83%8D%E3%83%BC%E3%82%B8%E3%83%A3)
- [xmonad - ArchWiki](https://wiki.archlinux.jp/index.php/Xmonad)

## コンポジットマネージャ

ウィンドウを透過したりドロップシャドウを加えるためのプログラム。(e.g. Picom) Xorg のウィンドウマネージャなどウィンドウの合成機能が含まれていないウィンドウマネージャを使う場合に向いている。必須ではない。

特定のディスプレイマネージャに依存しないスタンドアロンなコンポジットマネージャといえば、今の所 [Picom](https://github.com/yshui/picom) 一択だろう。Xcompmgr からフォークし多くのバグ修正を加えたものが compton であり、更に compton からフォークしたものが Picom である。

[Picom - ArchWiki](https://wiki.archlinux.jp/index.php/Picom)

---

ディスプレイマネージャではグラフィカルセッション開始と同時に起動するプログラムを指定する。このプログラムが終了したときセッションが終了されグラフィカルセッションからログアウトされる。 `xinit`, `startx` での初期設定は `xterm` というターミナルプログラムである。つまり初期設定ではグラフィカルセッション開始時に存在する `xterm` のウィンドウを終了するとセッションからログアウトされてしまう。通常はここにウィンドウマネージャのプログラムを設定する。ウィンドウマネージャは異常終了を除くとユーザが終了要求した場合のみ終了するので、ユーザはウィンドウマネージャを終了することによってグラフィカルセッションからログアウトできる。

GNOME スイートはかなり密結合でディスプレイマネージャからウィンドウマネージャ, コンポジットマネージャ, 一部の GNOME ソフトウェアまでが密結合である。特に GNOME3 ではその性質が非常に強くなっている。また GNOME 独自のバックエンドシステムサービスも存在するのでこの辺りも別記事で解説する。

# ググれる環境をつくる

Linux をインストールした後に最初にやるべきことは「ググれる環境をつくる」ことである。グラフィカルなプログラムを実行するためのディスプレイマネージャ xinit と Chromium をインストールする。

```bash
sudo pacman -S xorg-xinit chromium
```

alt-shift-Return で新しい xterm プロセスを開いて、とりあえずシェルから Chromium を起動する。

```bash
chromium
```

# Linux を使うことのデメリット

Linux を使っていて唯一不便に思うのはグラフィカルなアプリケーションが少ないことだ。

この問題はネイティブアプリケーションのように使える Web アプリ, [PWA](https://en.wikipedia.org/wiki/Progressive_web_application) の登場により徐々に解消されていくだろう。しかし今の段階では、例えばメールクライアント 1 つ挙げても、どのアプリケーションも使いやすさで Windows や macOS の標準メールクライアントに劣る。電子書籍リーダにしても同様で、私が普段使っている Kindle は Linux 版がないので **「試して理解 Linux のしくみ」という書籍が Linux で読めない。** (DRM の都合上 Kindle Cloud Reader では読めない書籍が多い)

# まとめ

デスクトップ環境は仕事でもプライベートでも使うので、設定をクラウド上に保存しつつ、自分に用途に合わせて現状の不満点を少しずつ改善することができれば、普段の生活を快適にすることができる。つまりデスクトップ環境構築はライフハックだ。

この記事は Linux を普段使いするメリットと Linux 上でカスタマイズ可能なデスクトップ環境を構築するために必要な要素について解説した。実際に自分好みのデスクトップ環境を構築していく手順を設定ファイルのソースコードを交えて別記事に書こうと思う。