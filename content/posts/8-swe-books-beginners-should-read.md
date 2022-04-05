---
title: "初学者にオススメするソフトウェアエンジニアリングの技術書 8選"
date: 2022-03-31T00:52:41+09:00
categories: ["キャリア", "技術書"]
tags: ["キャリア", "読書", "技術書"]
---

## ITエンジニアのための業務知識がわかる本

**会社法**から**企業会計原則**などのあらゆる業務の基幹となる法律知識から始まり、**マーケティング**, **生産管理**, **在庫管理 (SCM)**, **販売管理**などの業務知識を、実際のシステム設計や画面を交えて解説している。
専門用語も多数解説しているため、ドメインエキスパートと同じ言語で会話する上でも役に立つ。

- [ITエンジニアのための【業務知識】がわかる本 第5版](https://www.amazon.co.jp/dp/4798157384)

{{< hint info >}}
BtoB領域の開発に従事していると分かるが、このような業務知識や業務システムのノウハウは大変貴重である。
BtoBソフトウェアベンダーが探りを入れるために競合他社のBtoBソフトウェアサービスを申し込むことも多々ある。
(大抵は出禁になる)
{{< /hint >}}

## キタミ式イラストIT塾 応用情報技術者

なにかと馬鹿にされがちな応用情報技術者 (AP) 資格だが、ソフトウェアエンジニアとしてやっていく上での必要な知識を薄く広く学ぶには非常によい試験である。
その試験内容は**コンピュータアーキテクチャの基礎**から**データベース**, **ネットワーク**, **プロジェクト管理**や**経営学**など、非常に幅広い。

- [キタミ式イラストIT塾 応用情報技術者 令和04年](https://www.amazon.co.jp/dp/429712453X)

キタミ式イラストIT塾は分かりやすい一方、試験内容のカバレッジが若干狭いため、他の参考書と併読することがオススメ。

「徹底攻略」シリーズは、物理本を買うと電子版 (PDF) も貰える。
「電子書籍で持ち運び、物理本で見直す」という勉強方法ができるため、資格試験の受験を考えている人に特にオススメ。

- [徹底攻略 応用情報技術者教科書 令和4年度](https://www.amazon.co.jp/dp/4295012912)

キタミ式イラストIT塾では深く触れられていない、**演算器**, **レジスタ**, **キャッシュの仕組み**, **スーパースカラ**や**パイプライン**などの低レイヤー最適化技術を学ぶのに以下の本もオススメ。

- [プロセッサを支える技術 －－果てしなくスピードを追求する世界 (WEB+DB PRESS plus)](https://www.amazon.co.jp/dp/4774145211)

## 実践ドメイン駆動設計

ドメイン駆動設計を実装を交えながら丁寧に解説している。
開発者とドメインエキスパートが対話をするための共通言語 (**ユビキタス言語**) の定義から始まり、基本的なアーキテクチャや**ES**, **CQRS**などの実装パターンに触れつつ、**マイクロサービス**, **永続層のスケーリング**, **データ一貫性**など幅広いソフトウェアエンジニアリングの問題に触れている。

- [実践ドメイン駆動設計 (Object Oriented SELECTION)](https://www.amazon.co.jp/dp/479813161X)

本著で登場する「**境界づけられたコンテキスト**」の実装例として、以下のGitHubレポジトリのソースコードを参照することもオススメ。
ただし、実装例のJavaのバージョンがかなり古い。

- [VaughnVernon/IDDD_Samples](https://github.com/VaughnVernon/IDDD_Samples)

本著の内容は非常に網羅的である反面、初学者 (特にバックエンド未経験者) には重いかもしれない。
よりライトに読めるDDD本の選択肢として [@little_hand_s](https://twitter.com/little_hand_s) さんの著書も紹介しておく。

- [ドメイン駆動設計 モデリング/実装ガイド](https://little-hands.booth.pm/items/1835632)
- [ドメイン駆動設計 サンプルコード&FAQ](https://little-hands.booth.pm/items/3363104)

## Zalando RESTful APIとイベントスキーマのガイドライン

Zalando社におけるRESTful APIの設計ガイドライン。
**リソース指向アーキテクチャ (resource-oriented architecture, ROA)** でRESTful APIを設計するためのガイドラインがまとまっている。
無料で読める。

- [Zalando RESTful API と イベントスキーマのガイドライン](https://restful-api-guidelines-ja.netlify.app)

## Cassandra The Definitive Guide

とある企業の基盤チームに配属されていた頃のバイブル。
分散システムの基本から始まり、Cassandraのアーキテクチャについて詳しく解説していく。

Cassandraはレプリケーション・ファクターやQuorumなどの設定により、データ一貫性のレベルを変更でき、BrewerのCAP定理におけるCPとAPの間でその特性をコントロールできる。
つまり、**Cassandraのアーキテクチャを学ぶことは、分散データベースそのものを学ぶことに近い。**
日本語版はないが、分散システムを学びたい方へオススメである。

- [Cassandra - the Definitive Guide: Distributed Data at Web Scale](https://www.amazon.co.jp/dp/1492097144)

加えて、分散システムを学ぶ上で役に立つ記事やブログを紹介しておく。

- [分散型システム徹底入門 – Part 1.](https://postd.cc/a-thorough-introduction-to-distributed-systems-3/)
- [分散型システム徹底入門 – Part 2.](https://postd.cc/a-thorough-introduction-to-distributed-systems-2/)
- [分散型システム徹底入門 Part 3.](https://postd.cc/a-thorough-introduction-to-distributed-systems/)
- [NoSQLデータベース：調査と決定のガイダンス（その1）](https://postd.cc/nosql-databases-a-survey-and-decision-guidance-1/)
- [NoSQLデータベース：調査と決定のガイダンス（その2）](https://postd.cc/nosql-databases-a-survey-and-decision-guidance-2/)
- [大規模な決済システムを構築する際に学んだ分散型アーキテクチャの考え方 – 前編](https://postd.cc/distributed-architecture-concepts-i-have-learned-while-building-payments-systems/)
- [大規模な決済システムを構築する際に学んだ分散型アーキテクチャの考え方 – 後編](https://postd.cc/distributed-architecture-concepts-i-have-learned-while-building-payments-systems-2/)
- [Software Transactional Memo](https://kumagi.hatenablog.com/)

## The Twelve-Factor App

保守性に優れるソフトウェアサービスを設計するための方法論がまとまっている。
無料で読める。

- [The Twelve-Factor App](https://12factor.net/ja/)

## AWS認定アソシエイト3資格対策

AWS中級資格の試験対策本で、AWSサービスの基本的な使い方がまとまっている。
IAMなどの**ゼロトラスト**的な考え方、VPCなどの**仮想ネットワーク**, セキュリティグループやACLなどの**多層防御**など、AWSサービスの概要から学ぶべきクラウド設計のノウハウは多くある。

- [AWS認定アソシエイト3資格対策~ソリューションアーキテクト、デベロッパー、SysOpsアドミニストレーター~](https://www.amazon.co.jp/dp/4865941991)

特にAWS Well-Architected フレームワークの5本の柱には、クラウド設計の重要な考え方がまとめられているので是非一読してほしい。

- [フレームワークの 5 本の柱 - AWS Well-Architected フレームワーク](https://wa.aws.amazon.com/wellarchitected/2020-07-02T19-33-23/wat.pillars.wa-pillars.ja.html)

## Pythonで理解する統計解析の基礎

統計解析の基礎をPythonで動かしながら学ぶことができる。
あらゆる箇所で数学的な証明を欠いているのは難点だが、Google先生と併用しながら読み進めることができた。

- [Pythonで理解する統計解析の基礎 (PYTHON×MATH SERIES)](https://www.amazon.co.jp/dp/4297100495)

教育系YouTuberの[ヨビノリ先生](https://yobinori.jp/index.html)の解説動画も是非見てほしい。
前述の著書に欠けている数学的証明や各統計量の気持ちなどを丁寧に解説している。

- [確率統計学｜予備校のノリで学ぶ「大学の数学・物理」](https://yobinori.jp/video/probability-statistics.html)