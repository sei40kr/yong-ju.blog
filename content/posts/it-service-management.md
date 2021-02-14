---
title: "IT サービス管理"
date: 2021-02-15T02:53:03+09:00
tags: ["勉強ノート", "マネジメント"]
---

## 前提知識

- [フォールトトレラントシステム]({{< ref "fault-torelant-system" >}})

## RASIS

RASIS はコンピュータシステムに関する代表的な指標の頭文字をとったものである。

信頼性 (Reliability)
: 安定して期待される役割を果たすことのできる能力。
代表的な評価指標に  **MTBF (= Mean Time Between Failure, 平均故障間隔)**  がある。

保守性 (Serviceability, maintainability)
: 要求された機能が保持される、または修復される能力。
代表的な評価指標に  **MTTR (= Mean Time To Repair, 平均修復時間)**  がある。

可用性 (Availability)
: システムが継続して稼働できる能力。
代表的な評価指標に**稼働率**があり、以下に示す式で求められる。
$$A=\frac{\text{MTBF}}{\text{MTBF}+\text{MTTR}}$$

完全性 (Integrity)
: データに欠損や不整合がないことを保証する能力。

機密性 (Security)
: データを許可されたユーザにのみ公開する特性。

## 事業継続計画

**事業継続計画 (BCP = Business Continuity Planning)** は、災害などの緊急事態が発生したときに、損害を最小限に抑えながら事業の継続や復旧を図るための計画である。

## ディザスタリカバリ

**ディザスタリカバリ (disaster recovery)** は災害 (人為的災害含む) による被害を最小限に抑えるための措置のことをいう。

災害により中断されたビジネスプロセスが復旧されるべき時間の目標を、**目標復旧時間 (RTO = Recovery Time Objective)** という。

重大なインシデントにより、IT サービスのトランザクションが失われることもある。
このような場合に失われる可能性のあるトランザクションの最大期間の目標を、**目標復旧時点 (RPO = Recovery Point Objective)** という。
RPO はオフサイトのバックアップ取得間隔に大きく依存する。

## SLA

**SLA (= Service Level Agreement, サービス水準合意)** はサービス提供者と顧客の間で結ばれる、サービスについての合意である。

SLA の内容には以下のようなものがある。

- サービスの品質
- **SLO (= Service Level Objective, サービスレベル目標)**
  - サービスの可用性
  - サービスの応答時間 (パフォーマンス)
  - サービスデスクの応答時間 (ex. 問い合わせの 85% は 2 分以内に応答する)
  - インシデントの対応時間 (ex. 深刻度 4 のチケットの 98% は 5 営業日以内に処理する)
- 責任範囲

## ITIL

**ITIL (= Information Technology Infrastructure Library, アイティル)** は IT サービスマネジメントにおけるベストプラクティスをまとめたものである。

### 3 つの P

ITIL には 3 つの P という概念があり、下記を指す。

- プロセス (Process)
- 人 (People)
- プロダクト (Product)

3 つの P は、充実したプロセスや人のスキル, 便利なツールがバランスよく配置されなければ、それらの恩恵を受けられないという考え方を示している。

### サービスサポート

サービスサポート (service support) には下記のプロセスがある。

#### インシデント管理

インシデント管理プロセスは、事業復旧を主目的とし、インシデントの発生から解決 (クローズ) までの一連の流れを管理するプロセスである。

インシデント管理プロセスには下記のゴールがある。

- 可能な限り迅速にサービスを復旧させる。
- 事業への悪影響を最小限に抑える。
- SLA に則ったサービスレベルを維持する。

#### 問題管理

問題管理プロセスは、インシデントや障害の原因を追求し、再発防止策を策定するプロセスである。

#### 構成管理

構成管理プロセスは、ソースコードやドキュメントなどの成果物に対する変更履歴を管理するプロセスである。

構成管理のベストプラクティスには下記のようなものがある。

- コードレビュー
- ビルド管理
- プロセス管理
- 環境管理
- 開発に関するチーム内コミニュケーションの促進
- バグトラッキング

#### 変更管理

変更管理プロセスは、サービス構成の変更の安全性と効率を高めるプロセスである。

#### リリース管理

リリース管理プロセスは、変更管理プロセスで承認された変更を、稼働している実サービスに反映するプロセスである。
リリース管理プロセスでは、変更管理との綿密な連携が求められる。
また、リリース計画についての顧客とのコミュニケーションも重要である。

### サービスデリバリ

サービスデリバリ (service delivery) には下記のプロセスがある。

#### サービスレベル管理

サービスレベル管理プロセスは、SLA を管理するプロセスである。

#### IT サービス財務管理

IT サービス財務管理プロセスは、IT サービスの提供の収益とコストを管理するプロセスである。

#### 可用性管理

可用性管理プロセスは、必要なシステムとマンパワーの可用性を管理するプロセスである。

#### IT サービス継続性管理

IT サービス継続性管理プロセスは、IT サービスの提供が停止した場合の 、顧客への影響を最小限に防ぐことを目的としたプロセスである。

#### キャパシティ管理

キャパシティ管理プロセスは、顧客が要求するサービスレベルに対し、将来的にシステムが必要とするリソースを管理するプロセスである。

### ツール

ITIL を支援するツールには以下のようなものがある。

- タスク管理ツール (ex. [Redmine](https://redmine.jp), [JIRA](https://www.atlassian.com/ja/software/jira), [Trello](https://trello.com/ja))
- チャットコラボレーションツール (ex. [Slack](https://slack.com/intl/ja-jp), [Microsoft Teams](https://www.microsoft.com/ja-jp/microsoft-teams/group-chat-software))
- バージョン管理ツール (ex. Git)
- API マネジメント (ex. OpenAPI)
- ログマネジメント (ex. Elasticsearch + Kibana, [Splunk](https://www.splunk.com/ja_jp))
- モニタリングツール (ex. Prometheus, Grafana, [DataDog](https://www.datadoghq.com/ja), [New Relic](https://newrelic.com/jp))
- オンコールツール (ex. [PagerDuty](https://ja.pagerduty.com))

<!-- TODO ITIL についての情報を追記 -->

## 参考文献

- Wikipedia, [RASIS](https://ja.wikipedia.org/wiki/RASIS)
- Wikipedia, [事業継続計画](https://ja.wikipedia.org/wiki/%E4%BA%8B%E6%A5%AD%E7%B6%99%E7%B6%9A%E8%A8%88%E7%94%BB)
- Wikipedia, [ディザスタリカバリ](https://ja.wikipedia.org/wiki/%E3%83%87%E3%82%A3%E3%82%B6%E3%82%B9%E3%82%BF%E3%83%AA%E3%82%AB%E3%83%90%E3%83%AA)
- Wikipedia, [サービス水準合意](https://ja.wikipedia.org/wiki/%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E6%B0%B4%E6%BA%96%E5%90%88%E6%84%8F)
- Wikipedia, [Service-level objective](https://en.wikipedia.org/wiki/Service-level_objective)
- Wikipedia, [Information Technology Infrastructure Library](https://ja.wikipedia.org/wiki/Information_Technology_Infrastructure_Library)
- Wikipedia, [サービスサポート](https://ja.wikipedia.org/wiki/%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88)
- Wikipedia, [ソフトウェア構成管理](https://ja.wikipedia.org/wiki/%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E6%A7%8B%E6%88%90%E7%AE%A1%E7%90%86)
- Wikipedia, [サービスデリバリ](https://ja.wikipedia.org/wiki/%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%83%87%E3%83%AA%E3%83%90%E3%83%AA)
