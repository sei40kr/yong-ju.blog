---
title: "純関数型 OS である NixOS を使おう"
date: 2020-12-24T02:31:33+09:00
---

# NixOS とは

**NixOS** は Linux のディストリビューションの 1 つである。

[NixOS - NixOS Linux](https://nixos.org)

# NixOS の特徴

- パッケージマネージャ Nix を使ってパッケージを管理する
- Nix Expression Language (以下 Nix 言語) で書かれた構成ファイルを記述する
- 構成ファイルをビルドすると環境 (environment) が生成される
- 環境に切り替える (switch) することでその環境が利用可能になる
- 過去にビルドされた環境はスナップショットとして保存されており、環境のスナップショットに切り替えることで、環境をロールバックすることができる

純関数型言語のように OS の環境をコードベースで宣言的に記述することによって、自分の環境を GitHub などに push してバージョン管理することができる。

これだけでは説明が不十分だと思うので、NixOS を構成するコンポーネントの内部処理を追いながら NixOS のアーキテクチャを明らかにしていく。

# パッケージマネージャ Nix でのパッケージ管理

パッケージマネージャ Nix は以下の 3 つの特徴がある。

- **Reproducible** - パッケージが動作する環境の再現性。 Nix は同一パッケージの異なるバージョンを共存させることができる。パッケージがある環境で正常に動作すれば、他の環境でも正常に動作することが保証される。
- **Declarative** - 宣言的であること。
- **Reliable** - あるパッケージをインストールあるいはアップグレードすることによって他のパッケージが正常に動作しなくなることがない。

Nix はビルドしたパッケージを `/nix/store` (以下 Nix store) 以下にコピーする。
Nix を使ってパッケージをビルド & Nix store にコピーするときの大まかな内部処理を下記に示す。

1. ローカルに clone したチャンネル (channel) からパッケージを探す
1. チャンネルから Nix 言語でパッケージをビルド & コピーする方法を記したファイル, derivation を読み込む
1. derivation で指定されたソースが Nix store になければ clone する
1. derivation で指定されたビルドに必要な依存パッケージ (native build input) のうち Nix store にないものをビルド & コピーする
1. derivation で指定されたランタイムで必要な依存パッケージ (build input) のうち Nix store にないものをビルド & コピーする
1. derivation で指定された依存パッケージと一部のユーティリティツール (e.g. `coreutils` ) にのみ PATH を通した bash セッションを開始 (Docker コンテナを想像すると分かりやすい)
1. bash セッションにて derivation で指定されたビルドコマンドを実行
1. bash セッションにて derivation で指定されたインストールコマンド (実態はコピー) を実行 (ランタイムに必要なファイルのみを Nix store にコピーする)

## 補足

- パッケージマネージャ Nix 自体は実は macOS でも利用可能である
- clone やビルド, インストールの前後に他のコマンドが実行される場合がある。
  例えば fixup フェーズのコマンドはテキストベースの実行可能ファイル (e.g. シェルスクリプト, Python スクリプト) に記述された shebang を絶対パスに変換する。
- Nix store 直下のパッケージディレクトリは必ず `<SHA256 ハッシュサム>-<パッケージ名>[-<パッケージバージョン>]` と命名されており、パッケージとバージョンからディレクトリ名が一意に定まる。
  この仕組みにより、同一パッケージの異なるバージョンを複数共存させたり、インストールされていないソースやパッケージを高速に検出することが可能となる。
- Nix store にコピーされたパッケージには PATH が通っていない。環境のビルド & 切り替え (後述) を行うことでコマンドとして利用可能になる。

# Nix 言語で記述した構成ファイルをビルドし環境を生成する

Nix 言語で記述した構成ファイルをビルドして環境を生成するときの大まかな内部処理を下記に示す。

1. 構成ファイルをビルドする
2. 構成ファイルで宣言した環境で参照している設定ファイルが Nix store になければコピーする
3. 構成ファイルで宣言した環境で列挙しているパッケージが Nix store になければビルド & コピーする

## 補足

- 要するに NixOS における環境 (environment) の実体は、設定ファイルとパッケージの列挙に過ぎない。
- 構成ファイルや設定ファイルを変更しても、ビルドした時点の環境 (設定ファイル含む) は Nix store にコピーされているため、環境は不変である。

# 構成ファイルからビルドした環境に切り替える

では生成された環境に切り替えるにはどうするか。実は驚くほどシンプルである。

ビルドした環境に切り替えるときの大まかな内部処理を下記に示す。

1. ビルドした環境で参照している設定ファイルの symlink を環境で指定された場所に作成する
2. ビルドした環境で列挙しているパッケージの実行可能ファイルの symlink を Nix profile 内の PATH が通ったディレクトリに作成する

## 補足

- symlink を作成するのは実は実行可能ファイルに限らない。他にも Manpage や systemd サービスのファイルなどの symlink がデフォルトで作成される。具体的には `environment.pathsToLink` で指定したディレクトリに含まれるファイルの symlink が Nix profile 内に作成される。

# Flakes

Nix 言語で宣言的に自分の環境を記述し dotfiles などで管理するのに便利な機能 Flakes を紹介したかったが、自分の理解が追いついていないので一旦 WIP とする。

[Flakes - NixOS Wiki](https://nixos.wiki/wiki/Flakes)

# 参考リンク

- [NixOS - Guides - Install Nix](https://nixos.org/guides/install-nix.html) - NixOS のインストールガイド
- [NixOS - Nix 2.3.10 manual](https://nixos.org/manual/nix/stable/#ch-expression-language) ― Nix Expression Language の言語仕様
- [NixOS Wiki](https://nixos.wiki) ― NixOS ユーザによってメンテナンスされている Wiki
- [NixOS/nixpkgs](https://github.com/NixOS/nixpkgs) ― Nixpkgs のレポジトリ
- [hlissner/dotfiles](https://github.com/hlissner/dotfiles) ― [高品質 Emacs ディストリビューション Doom Emacs を使おう]({{< ref "lets-start-using-doom-emacs" >}}) で紹介した Doom Emacs の author, Henrik Lissner さんの dotfiles. 環境をモジュール (module) という単位を分割し、ホストマシン毎に必要なモジュールを有効化して環境を宣言している。
