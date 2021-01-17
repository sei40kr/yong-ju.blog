---
title: "全文検索システム"
date: 2021-01-17T02:58:09+09:00
tags: ["データベース", "全文検索"]
---

## 全文検索の分類

### 逐次検索 (順次操作検索, grep 型検索)

複数のデータを順次検索していくことで、検索対象となる文字列を探し出す。

事前にインデックスを作成せず、文書を順次走査していくため、**検索対象データの増加に伴って検索速度が低下**する。

ある文字列の中から別の文字列を高速に検索するアルゴリズムには以下のようなものがある。

- **BM (Boyer-Moore) 法**
- **KMP (Knuth-Morris-Pratt) 法**

### インデックス型検索

あらかじめ検索対象となる文書を走査しておき、高速な検索ができるようインデックス (後述の転置インデックス参照) を作成しておくことで、検索時のパフォーマンスを向上させる。

## 転置インデックス

インデックス型検索のインデックスには**転置インデックス**が使われる。
転置インデックスの構造には以下の 2 通りがある。

DAAT (Document At A Time)
: 各索引文字列に対してその索引文字列を含む文書のリストをもつ

TAAT (Term At A Time)
: 各文書に対してその文書に含まれる索引文字列のリストをもつ

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

## 単語の抽出

文書や検索クエリを単語単位で分解する (トークナイズ) 方法は以下の 2 つがある。

### N-gram

- 一定の長さ ($N$) の文字列単位で分解する。
- $N=1$ の N-gram を uni-gram (ユニグラム)、$N=2$ の N-gram を bi-gram (バイグラム)、$N=3$ の N-gram を tri-gram (トライグラム) と呼ぶ。
- **$N$ より小さい長さの文字列を検索できない。**
- **再現性に優れるが、精度に劣る。** (ex. 京都 → 東**京都**)

### 形態素解析

- 意味をもつ最小単位 (形態素) の列に分解する。
- 日本語の場合は、単語をスペースで区切る (わかち書き) の習慣がないため、**解析用の辞書が必須**となる。
- **精度に優れるが、再現率に劣る。**

日本語の代表的な形態素解析エンジンとして、以下の 3 つがある。

- [MeCab](https://taku910.github.io/mecab)
- [Kuromoji](https://www.atilika.com/ja/kuromoji)
- [Sudachi](https://github.com/WorksApplications/Sudachi)

## 単語の表記ゆれの吸収

### Stemming (ステミング, Lemmatisation)

形態素解析で抽出した単語の語形を辞書系にする (ex. 会った → 会う, met -> meet)

### 検索シノニム (synonym)

同義の単語を予め辞書登録しておく (ex. 地下ドル → 地下アイドル)

## ランキング指標

### TF-IDF

文書中に現れる単語の重要度を評価する手法の 1 つである。

$$\text{tf-idf}=\frac{文書中の単語の出現回数}{文書中の全ての単語の出現回数の和} \cdot\log\frac{総文書数}{単語を含む文書数}$$

式後半の部分 (**逆文書頻度, IDF = Inverse Document Frequency**) によって多くの文書に出現する単語の重要度は下がり、特定の文書にしか出現しない単語の重要度を上げる役割をもつ。
つまり **IDF は一般語フィルタ**として機能する。

<!-- TODO Okapi BM25 について書く -->
<!-- TODO nDCG について書く -->

## 有名な全文検索エンジン

[Apache Lucene](https://lucene.apache.org)
: Java 製の OSS 検索**ライブラリ**。

[Apache Solr](https://lucene.apache.org/solr)
: Lucene ベースの OSS 全文検索システム。

[Elasticsearch](https://www.elastic.co/jp/elasticsearch)
: Lucene ベースの OSS 全文検索システム。Elastic 社が中心となり開発されている。

[Algolia](https://www.algolia.com)
: BaaS の全文検索システム。API 経由で利用できる。


## 参考文献

- Wikipedia, [全文検索](https://ja.wikipedia.org/wiki/%E5%85%A8%E6%96%87%E6%A4%9C%E7%B4%A2)
- Wikipedia, [文字列検索](https://ja.wikipedia.org/wiki/%E6%96%87%E5%AD%97%E5%88%97%E6%8E%A2%E7%B4%A2)
- Wikipedia, [tf-idf](https://ja.wikipedia.org/wiki/Tf-idf)
- Wikipedia, [Okapi BM25](https://ja.wikipedia.org/wiki/Okapi_BM25)
- rilmayer, 図書館情報学オタクと学ぶ 検索エンジニア入門, 2020
- 守谷 純之介, [検索結果の品質向上 Elasticsearch 入門](https://speakerdeck.com/rtechkouhou/jian-suo-jie-guo-falsepin-zhi-xiang-shang-elasticsearchru-men), 2019
- 高岡 一馬, [Java でつくる本格形態素解析器](https://www.slideshare.net/WorksApplications/java-82794239), 2017
