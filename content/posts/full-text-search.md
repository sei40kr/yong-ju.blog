---
title: "全文検索システム"
date: 2021-01-17T02:58:09+09:00
tags: ["データベース", "全文検索"]
---

## 全文検索の分類

### 逐次検索 (順次操作検索, grep 型検索)

複数のデータを順次検索していくことで、検索対象となる文字列を探し出す。

事前にインデックスを作成せず、文書を順次走査していくため、検索対象データの増加に伴って検索速度が低下する。

ある文字列の中から別の文字列を高速に検索するアルゴリズムには以下のようなものがある。

- **BM (Boyer-Moore) 法**
- **KMP (Knuth-Morris-Pratt) 法**

### インデックス型検索

あらかじめ検索対象となる文書を走査しておき、高速な検索ができるようインデックスを作成しておくことで、検索時のパフォーマンスを向上させる。

## 転置インデックス

インデックス型検索のインデックスには**転置インデックス**が使われる。

DAAT (Document At A Time)
: DAAT 型の転置インデックスでは、各索引文字列に対してその索引文字列を含む文書のリストを記憶するインデックスを作成する。

TAAT (Term At A Time)
: TAAT 型の転置インデックスでは、各文書に対して文書に含まれる索引文字列のリストを記憶するインデックスを作成する。

## 検索評価指標

### 再現率 (Recall)

検索結果にどれだけ正解文書が含まれているか → **網羅性**の指標

$$再現率=\frac{検索結果に含まれる正解文書の数}{正解文書の数}$$

### 適合率 (Precision)

どれだけ検索に適合した文書を含んでいるか → **正確性**の指標

$$適合率=\frac{検索結果に含まれる正解文書の数}{検索結果の文書の数}$$

### F 値 (F-measure)

再現率と適合率の調和平均

$$\text{F 値}=\frac{2}{\frac{1}{再現率}+\frac{1}{適合率}}$$

## 検索トークンの抽出

文書や検索クエリから検索トークンを抽出する (トークナイズ) 方法は以下の 2 つがある。

### N-gram

- 一定の長さ ($N$) の文字列単位で分解する。
- $N$ より小さい長さの文字列を検索できない。
- $N=1$ の場合を Unigram (ユニグラム), $N=2$ の場合を Bigram (バイグラム), $N=3$ の場合を Trigram (トライグラム) と呼ぶ。
- **再現性に優れるが、精度に劣る。** (ex. 京都 → 東**京都**)

### 形態素解析

- 意味をもつ最小単位 (形態素) の列に分解する。
- 日本語の場合は、単語をスペースで区切る (わかち書き) の習慣がないため、解析用の辞書が必須となる。
- **精度に優れるが、再現率に劣る。**
- 日本語の代表的な形態素解析エンジンとして、以下の 3 つがある。
  - [MeCab](https://taku910.github.io/mecab)
  - [Kuromoji](https://www.atilika.com/ja/kuromoji)
  - [Sudachi](https://github.com/WorksApplications/Sudachi)

<!-- TODO 検索シノニムについて書く -->
<!-- TODO 正規化について書く -->

## ランキング指標

### TF-IDF

文書中に現れる単語の重要度を評価する手法の 1 つである。

$$\text{tf-idf}=\frac{文書中の単語の出現回数}{文書中の全ての単語の出現回数の和} \cdot\log\frac{総文書数}{単語を含む文書数}$$

式後半の部分は一般語フィルタとして働き、多くの文書に出現する単語の重要度は下がり、特定の文書にしか出現しない単語の重要度を上げる役割をもつ。

<!-- TODO Okapi BM25 について書く -->
<!-- TODO nDCG について書く -->

## 有名な全文検索エンジン

[Apache Lucene](https://lucene.apache.org)
: Java 製の OSS 検索**ライブラリ**。

[Elasticsearch](https://www.elastic.co/jp/elasticsearch)
: Lucene ベースの OSS 全文検索システム。Elastic 社が中心となり開発されている。

[Apache Solr](https://lucene.apache.org/solr)
: Lucene ベースの OSS 全文検索システム。

[Algolia](https://www.algolia.com)
: BaaS の全文検索システム。API 経由で利用できる。


## 参考文献

- Wikipedia, [全文検索](https://ja.wikipedia.org/wiki/%E5%85%A8%E6%96%87%E6%A4%9C%E7%B4%A2)
- Wikipedia, [文字列検索](https://ja.wikipedia.org/wiki/%E6%96%87%E5%AD%97%E5%88%97%E6%8E%A2%E7%B4%A2)
- Wikipedia, [tf-idf](https://ja.wikipedia.org/wiki/Tf-idf)
- Wikipedia, [Okapi BM25](https://ja.wikipedia.org/wiki/Okapi_BM25)
- rilmayer, 図書館情報学オタクと学ぶ 検索エンジニア入門, 2020
- 守谷 純之介, [検索結果の品質向上 Elasticsearch 入門](https://speakerdeck.com/rtechkouhou/jian-suo-jie-guo-falsepin-zhi-xiang-shang-elasticsearchru-men), 2019
