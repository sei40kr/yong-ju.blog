---
title: "ビッグデータ"
date: 2021-01-17T18:49:59+09:00
tags: ["勉強ノート", "ビッグデータ", "データベース", "分散システム"]
---

## 前提知識

- [データベースシステム]({{< ref "database-system" >}})
- [分散システム]({{< ref "distributed-system" >}})

## データの種類

### 非構造化データ (unstructured data)

スキーマをもたないデータ。

### 構造化データ (structured data)

スキーマが明確に定義されたデータ。以下のようなものがある。

ファクトテーブル (fact table)
: プロセスの指標やメトリクス, 事実を保存するテーブル

ディメンションテーブル (dimension table)
: ファクトテーブルに付随するマスターを保存するテーブル

サマリーテーブル (summary table)
: ファクトテーブルをある程度まとめて集約したものを保存するテーブル

## データの保存場所

DWH (データウェアハウス)
: 意思決定のため、目的別に編成され、削除や更新をしないデータの集合

データレイク
: 構造化/非構造化データやバイナリ等のファイルを含めたデータを一元的に格納したもの

データマート
: 必要なデータのみを DWH から抽出し、必要とする分析データを予め集計したもの

---

典型的な使い方として、システムから抽出した**生データ (raw data)** を 1 日の終わりにまとめて DWH に書き込み、それを夜間のうちに集計してデータマートにロードしたり、レポートを作成したりする。
このような抽出 (extract), 変換・加工 (transform), ロード (load) からなる操作を**ETL** (= Extract/Transform/Load) という。

## データを利用する目的

### BI (= Business Intelligence, ビジネスインテリジェンス)

データを収集, 蓄積, 分析, 報告し、経営上などの意思決定に役立てること。

BI で使われる一般的な機能を以下に示す。

データマイニング
: 詳しくは後述。

プロセスマイニング
: 発生した事象 (以下イベント) のログに基づいてビジネスプロセスを分析する。

複合イベント処理 (CEP = Complex Event Processing)
: イベントに関するデータのストリームを分析し、何らかの結論を得る。

ビジネス業績管理 (BPM = Business Performance Management)
: 重要業績評価指標 (KPI = Key Point Indicator, 以下 KPI) をモニタリングし、企業の業績を最適化する。

ベンチマーキング
: サービスやプロセスを優れた他社のパフォーマンスと比較し、分析する。

### データマイニング (data mining)

統計学, パターン認識, 機械学習などのデータ解析の技法をビッグデータに適用し、知識を取り出す。

## データ収集

### バルク (bulk) 型

データをまとめて取り出す。

### ストリーミング (streaming) 型

次々と生成されるデータを絶え間なく送り続ける。

ストリーミング型が適しているデータ処理には以下のようなものがある。

- システムモニタリング
- ログ管理
- 複合イベント管理

## データ分析

確証的データ探索 (confirmatory data analysis)
: 仮説を立ててそれを検証する

探索的データ探索 (exploratory data analysis)
: データを見ながらその意味を読み取ろうとする

## 参考文献

- Wikipedia, [Fact table](https://en.wikipedia.org/wiki/Fact_table)
- Wikipedia, [Dimension (data warehouse)](https://en.wikipedia.org/wiki/Dimension_(data_warehouse))
- Wikipedia, [データレイク](https://ja.wikipedia.org/wiki/%E3%83%87%E3%83%BC%E3%82%BF%E3%83%AC%E3%82%A4%E3%82%AF)
- Wikipedia, [データウェアハウス](https://ja.wikipedia.org/wiki/%E3%83%87%E3%83%BC%E3%82%BF%E3%82%A6%E3%82%A7%E3%82%A2%E3%83%8F%E3%82%A6%E3%82%B9)
- Wikipedia, [データマート](https://ja.wikipedia.org/wiki/%E3%83%87%E3%83%BC%E3%82%BF%E3%83%9E%E3%83%BC%E3%83%88)
- Wikipedia, [Extract/Transform/Load](https://ja.wikipedia.org/wiki/Extract/Transform/Load)
- 西田 圭介, ビッグデータを支える技術, 2017
