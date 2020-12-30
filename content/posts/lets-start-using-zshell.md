---
title: "究極の使い勝手を実現する UNIX シェル Z shell を使おう"
date: 2020-09-21T12:32:52+09:00
---

## 普段使っているシェルにこだわる理由

エンジニアにシェルのカスタマイズを勧めると「自分はあまりシェルコマンドが得意ではないから」と敬遠されがちである。だが、そのようなエンジニアこそシェルにこだわってほしい。インタラクティブシェルはシェル作業における基礎となるツールであり、我々のシェル作業をサポートしてくれるものである。**シェルコマンドが苦手だからこそシェルをカスタマイズするべきなのだ。**

## Z shell とは

[Z Shell - Wikipedia](https://ja.wikipedia.org/wiki/Z_Shell)

有名なシェルの 1 つであり zsh と呼ばれることが多い。この記事でも以下 zsh と呼ぶことにする。

macOS や Ubuntu を含むほとんどの OS のデフォルトシェルは bash である。
bash, zsh は共に POSIX に準拠しており、bash で動くコマンドやスクリプトの多くは zsh でも動くようになっている。

他に有名なシェルとして fish がある。

[fish shell](https://fishshell.com)

---

zsh の優れている点をいくつか紹介する。

- bash, fish と比べてプラグインの数が充実している
- bash と比べてコマンド補完やプロンプトのカスタマイズ性が充実している
- fish と異なり POSIX に準拠しているため普段のシェル作業に影響を与えない

## zsh をインストールする

macOS など、最初から zsh がインストールされている OS もある。

```bash
which zsh
```

で zsh の場所を確認することができる。

macOS ではプリインストールの zsh のバージョンが最新ではないかもしれない。その場合は Homebrew を使って最新版の zsh をインストールしてもよい。

```bash
brew install zsh
```

## zsh をログインシェルに設定する

ログインシェルは、Linux ユーザとしてログインした後にユーザセッションとして開始されるシェルプログラムである。

macOS では、初期設定のターミナルアプリで新しいセッションを開始すると自動的にログインシェルが実行されるようになっている。

まず、ログインシェルに設定するシェルの実行可能ファイルは `/etc/shells` に列挙されている必要がある。
`/etc/shells` を編集するには root 権限が必要なので、以下のようなコマンドで zsh の実行可能ファイルまでの絶対パスを `/etc/shells` のファイル末尾に追記する。

```bash
which zsh | sudo tee -a /etc/shells >/dev/null
```

次にログインしているユーザのログインシェルを変更する。

```bash
chsh -s "$(which zsh)"
```

ログインシェルの設定を完全に反映するために、このコマンドを実行した後に一度ログアウトすることが好ましい。

## zsh の設定ファイル

zsh の設定ファイルは複数存在する。
設定ファイルによって読み込まれる条件やタイミングも異なるので、目的に合致する設定ファイルを考える。

### ~/.zshenv

zsh が一番最初に読み込む設定ファイル。

環境変数の設定を記述することが多いが `~/.zshenv` に記述した環境変数は zsh プログラム自体にも影響を与える。通常 `~/.zshenv` では以下の環境変数を設定する。

| 環境変数  | 説明                         |
| :-------- | :--------------------------- |
| `LANG`    | デフォルトのロケールカテゴリ |
| `ZDOTDIR` | 後節で説明                   |

### ~/.zprofile

ログインシェルとして起動された ( `-l` オプションが引数に与えられた) 場合に読み込む設定ファイル。

Linux 環境ではログイン時に, macOS 環境ではターミナルアプリでセッションを開始する度に読み込まれる。
基本的に export する環境変数を記述する。 ( `PATH` など)

### ~/.zshrc

インタラクティブシェルとして起動された ( `-i` オプションが引数に与えられた) 場合に読み込む設定ファイル。

ほとんどのカスタマイズ設定は `~/.zshrc` に記述することになる。

## `ZDOTDIR` を設定してホームディレクトリをスッキリさせる

zsh は設定ファイルが 3 つも存在するのでホームディレクトリ直下がゴチャっとしてしまう。

```
~/
├ .zprofile
├ .zshenv
└ .zshrc
```

`ZDOTDIR` という環境変数を設定すると `~/.zprofile`, `~/.zshrc` をホームディレクトリ以外のディレクトリに配置できる。

```bash
export ZDOTDIR=~/.zsh
```

ただし下記の 2 点に注意する。

- `ZDOTDIR` は zsh に対する環境変数なので `zshenv` に設定を記述する( `~/.zprofile`, `~/.zshrc` を読み込む時点で定義済みでないと意味がない)
- 既に `ZDOTDIR` を export している zsh 上で zsh を実行した場合 `zshenv` は `${ZDOTDIR}/.zshenv` を参照してしまうので、念の為 symlink を定義しておく

  ```zsh
  # ZDOTDIR=~/.zsh
  ln -fs ~/.zshenv ~/.zsh/.zshenv
  ```

これでホームディレクトリ直下が少しスッキリする。

```
~/
├ .zsh/
│ ├ .zprofile
│ ├ .zshenv -> ~/.zshenv
│ └ .zshrc
└ .zshenv
```

## bash から設定の移行

インストール時に自動的に bash の設定を追加する開発ツールは多い。主に

- PATH を通す
- コマンド補完を定義する

といった内容の設定がインストーラによって追加されることが多い。

それらの設定が存在する場合、それらを zsh の設定ファイルに移行しなければ今まで使っていた開発ツールは正しく動作しない。
以下のファイルをチェックして、必要な設定は zsh に移行する。

- `/etc/bash_profile`
- `/etc/bashrc`
- `~/.bash_profile`
- `~/.bashrc`

bash と zsh はコマンド補完の定義の方法が異なる。
zsh で bash のコマンド補完定義を解釈したい場合は `bashcompinit` を使う。

```bash
autoload -Uz bashcompinit && bashcompinit
```

基本的に bash のコマンド補完と比べ zsh ネイティブなコマンド補完の方が機能的に優れていることが多い。
今まで使っていた bash のコマンド補完をそのまま移行する前に、後述する zsh-completions に zsh ネイティブなコマンド補完が存在していないか確認しよう。

## zsh プラグインマネージャ

### zinit

zsh のプラグインを管理するプラグインマネージャとして zinit をオススメする。

[zdharma/zinit: Ultra-flexible and fast Zsh plugin manager with clean fpath, reports, completion management, Turbo, annexes, services, packages.](https://github.com/zdharma/zinit)

zinit の優れている点をいくつか紹介する。

- プラグインマネージャ自体の大部分が遅延ロードに対応
- 豊富なオプション
- プラグインを zcompile でコンパイルし高速化 (参考: zshbuiltins(1))
- プラグインによる設定の変更を追跡できる

## zsh プラグイン

### Oh My Zsh

[ohmyzsh/ohmyzsh: A delightful community-driven (with 1700+ contributors) framework for managing your zsh configuration. Includes 200+ optional plugins (rails, git, OSX, hub, capistrano, brew, ant, php, python, etc), over 140 themes to spice up your morning, and an auto-update tool so that makes it easy to keep up with the latest updates from the community.](https://github.com/ohmyzsh/ohmyzsh/)

Oh My Zsh は zsh プラグインマネージャと zsh プラグインのセットである。

今回はプラグインマネージャとして zinit を紹介したが zinit で Oh My Zsh のプラグインを管理することもできる。

```zsh
# ohmyzsh/ohmyzsh/lib -> OMZL
zinit snippet OMZL::clipboard.zsh

# ohmyzsh/ohmyzsh/plugins -> OMZP
zinit snippet OMZP::zsh_reload/zsh_reload.plugin.zsh
```

### Prezto

[sorin-ionescu/prezto: The configuration framework for Zsh](https://github.com/sorin-ionescu/prezto)

Prezto も Oh My Zsh と同じく zsh プラグインマネージャとモジュールのセットである。
Oh My Zsh より後発であり、全てのモジュールが極力遅延ロードされるように設計されている。

zinit で Prezto のモジュールを管理することもできる。

```zsh
# sorin-ionescu/prezto -> PZT
zinit ice svn
zinit snippet PZT::modules/gnu-utility
```

## zsh のプラグイン&カスタマイズ

### コマンド履歴の保存

コマンド履歴をファイルに書き出すことで、異なるセッションでコマンド履歴を共有することができる。

```zsh
# ZDOTDIR=~/.zsh
HISTSIZE=10000
HISTFILE="${ZDOTDIR}/.zsh_history"
SAVEHIST=10000
```

| 環境変数   | 説明                                                                     |
| :--------- | :----------------------------------------------------------------------- |
| `HISTSIZE` | 内部コマンド履歴に保存するコマンド履歴の最大数                           |
| `HISTFILE` | インタラクティブシェルが終了したときにコマンド履歴を保存するためファイル |
| `SAVEHIST` | 履歴ファイルに保存するコマンド履歴の最大数                               |

参考: zshparam(1)

### コマンド履歴の検索

[zdharma/history-search-multi-word: Multi-word, syntax highlighted history searching for Zsh](https://github.com/zdharma/history-search-multi-word)

zsh は control-R でコマンド履歴を検索できるが、前方一致の検索しか存在せず使いづらい。
history-search-multi-word は複数ワードをサポートするコマンド履歴検索機能の再実装である。以前使ったコマンドが思い出せないときに、覚えている箇所からすぐ検索できるので大変重宝する。

```zsh
zinit ice wait'1' lucid
zinit light -b zdharma/history-search-multi-word
```

### シェルコマンドのシンタックスハイライト

[zdharma/fast-syntax-highlighting: (Short name F-Sy-H). Syntax-highlighting for Zshell – fine granularity, number of features, 40 work hours themes](https://github.com/zdharma/fast-syntax-highlighting)

入力したコマンドが見やすくハイライトされる。
前節で紹介した history-search-multi-word で検索したコマンド履歴もハイライトされるので大変見やすい。

```zsh
zinit ice wait atinit'zpcompinit; zpcdreplay' lucid
zinit light zdharma/fast-syntax-highlighting
```

### コマンド補完の改良

zsh ではコマンド補完の挙動を強力にカスタマイズできる。
利用可能な設定は zshcompsys(1) で参照できるが、私でも全てを把握しきれていないほど数が多いので Oh My Zsh の「コマンド補完の挙動をいい感じにしてくれるライブラリ」を読み込む。

[ohmyzsh/completion.zsh at master · ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh/blob/master/lib/completion.zsh)

```zsh
zinit snippet OMZL::completion.zsh
```

#### zsh-completions

コマンド補完定義の詰め合わせパック zsh-completions の導入もオススメする。
zsh-completions はコマンド補完の定義が遅延ロードされるように設計されているため、普段使わないコマンド補完の定義が含まれていても気にすることはない。

[zsh-users/zsh-completions: Additional completion definitions for Zsh.](https://github.com/zsh-users/zsh-completions)

```zsh
zinit ice pick'' blockf wait''
zinit light zsh-users/zsh-completions
```
