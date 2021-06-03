---
title: "機械学習でコード補完をする TabNine を使おう"
date: 2020-09-07T21:04:49+09:00
categories: ["開発環境"]
tags: ["エディタ"]
---

## TabNine とは

{{< youtube TKLkXh_c-Gw >}}

[AI Smart Compose for Your Code | TabNine](https://www.tabnine.com/)

TabNine は機械学習を用いてコードを予測し補完するためのツールである。
言語サーバのコード補完にはない **2 トークン以上の補完** が目玉機能であり、定型的なコードスニペットの補完やパターンのあるコードの繰り返しに強い。

補完エンジンの内部では自己回帰言語モデル GPT-2 が使われており、この次世代モデルに当たる GPT-3 は「自然言語で指定したデザインのコンポーネントのソースコードを JSX で自動生成する」というデモで界隈を騒がせた。

{{< tweet 1282676454690451457 >}}

ちなみに自動プログラミングのカテゴリとして [git-complete](https://github.com/zk-phi/git-complete) という Emacs パッケージがある。
これは `git grep` を用いて作業中のプロジェクトから似たような箇所を見つけ補完するというパッケージだ。
こちらも非常に有用に見えたのだが、私が普段使っている company と相性が悪そうなので導入を断念した。

## 料金プラン

[Pricing | TabNine](https://www.tabnine.com/pricing/)

無料版は学習するプロジェクトのサイズが 400KB に制限されている。
つまり業務プロジェクトで無料版を使うのはほぼ不可能だろう。
有料プランでは Deep TabNine Cloud というクラウドのリソースを使った補完も利用することができる。

Professional プランは月額 \$15.00 (約 ¥1,600) となっており、かなり考えさせられる価格設定となっている。
**年額にすると IntelliJ IDEA のパーソナルライセンスの新規 1 年目のライセンス料を超える。**

## 設定

TabNine の補完を有効にしたエディタで `TabNine::config` と入力すると設定画面が Web ブラウザで開き、各種設定やライセンスのアップグレードを行うことができる。

## Semantic Completion

Semantic Completion は補完候補の検証に LSP 準拠の言語サーバを使う機能である。
TabNine が子プロセスとして起動した言語サーバの補完候補と比較することで、機械学習による補完候補を文法的やコンテキスト的に正しいものに絞り込む。

Semantic Completion を有効にするには `TabNine.toml` で言語サーバの実行コマンドを設定し、TabNine の補完を有効にしたエディタで `TabNine::sem` と入力する。

[Semantic Completion | TabNine](https://www.tabnine.com/semantic)

### Prefetch

2 トークン以上の補完候補に対して Semantic Completion を有効にするには、言語サーバを複数起動して補完候補を先読みしておく必要がある。
`TabNine.toml` で各言語ごとに `num_server_instances` で起動する言語サーバのプロセス数を設定できる。なんとも贅沢なマシンリソースの使い方だ。

## TabNine の問題点

- TabNine で Semantic Completion を使うと言語サーバ実行コマンドの設定をエディタと TabNine の 2 箇所でもつことになる
- 単一トークンの補完候補のメタデータ (型情報, ドキュメントなど) が TabNine 経由だと消える
- コード補完をしたときの挙動 (import 文の追加など) が TabNine 経由だとない。これは Java や TypeScript を書く場合は致命的である

## TabNine を言語サーバのプロキシにするという提案

私は「TabNine が言語サーバのプロキシとして動けばこれらの問題は全て解決できるのではないか」と考える。つまりこういうことである。

- TabNine の実行ファイル引数で言語サーバの実行コマンドを受け取る
- TabNine は引数で指定された実行コマンドで指定された数だけ言語サーバのプロセスを起動する
- コード補完以外の TabNine へのリクエストは全て子プロセスの言語サーバに委譲し、コード補完は TabNine 側で生成したものに置き換える

このようにすればエディタ側の TabNine の設定も

```sh
tabnine -- java -jar groovy-language-server-all.jar
```

のようにエディタで設定している言語サーバの実行コマンドの前に `tabnine --` を加えるだけでよいのでエディタごとにプラグインを開発する必要がない。
子プロセスとなる言語サーバの実行コマンドの設定が複数存在してしまう問題も解消する。
更にエディタ側で言語サーバを使う場合、立ち上げる言語サーバの合計プロセス数を 1 つ少なくできる。

早速 Issues で提案しようと思ったら既にあった。

[Have TabNine delegate requests for a lanaguage server · Issue #40 · codota/TabNine](https://github.com/codota/TabNine/issues/40)

author にもこの案の利点がよく理解されているように見える。今後のアップデートが楽しみだ!

## Doom Emacs で使う

Emacs で TabNine を使うためのパッケージとして [company-tabnine](https://github.com/TommyX12/company-tabnine) がある。
これは company の backend として動作する。

Doom Emacs では LSP 言語サーバで補完をするときの company backend を設定する変数 `+lsp-company-backends` があるのでこれを設定する。

```emacs-lisp
(package! company-tabnine)

(setq +lsp-company-backends '(company-tabnine))
```
