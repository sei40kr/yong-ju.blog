---
title: "ORM は百害あって一利なしは本当か"
date: 2020-12-22T23:45:17+09:00
tags: ["プログラミング", "バックエンド"]
---

[O/R マッピングは百害あって一利なし！ - Qiita](https://qiita.com/gomiryo/items/6d448c500749f91242d2)

この記事が投稿されたのは今から 2 年ほど前のことだが、当時の私はこの記事の内容についてかなり共感していた。
本当に ORM は百害あって一利なしか、標準的な ORM フレームワークの役割から考察してみる。

## これまでの ORM の役割

- クエリリザルトからエンティティ or DTO にマッピングする役割
- 独自の DML を提供し、永続化するデータベースの差異を吸収する Repository に近い役割 (最近は独自 DML を持たない ORM も多い)
- レコードの識別子をキーとするオブジェクトキャッシュとしての役割

## ORM が百害あって一利なしと言われてしまった理由

- ORM フレームワーク独自の DML というよりマイナーな知識を増やしている
- ORM フレームワーク独自の DML で実装できることは生 SQL と比べ必然的に減る
- 計算資源が安価になったので、エンティティ or DTO のオブジェクトキャッシュはもはや不要になった

## これまでの問題

### 共通の問題

- クエリリザルトをエンティティ or DTO にマッピングする部分が type-safe ではない
- クエリやコマンドのテスタビリティ
  1. DML の構文チェック
  1. クエリやコマンドの振る舞いのテスト
  1. DBUnit はどちらもテストできるが、動作がとても遅い

### ORM or DB ライブラリを使わないと発生する問題

- マッピング処理の冗長さ
- エラー処理の冗長さ

### ORM を使わないと発生する問題

- **なし**

### ORM を使うことで発生する問題

- ORM フレームワークが提供する独自 DML の学習コスト
- エンティティに ORM が要求する no-args constructor を実装すると、モデルの制約に沿わないオブジェクトが作られる可能性がある

## これからの ORM

Exposed の例から抜粋:

```kotlin
object Users : Table() {
    val id = varchar("id", 10) // Column<String>
    val name = varchar("name", length = 50) // Column<String>
    val cityId = (integer("city_id") references Cities.id).nullable() // Column<Int?>

    override val primaryKey = PrimaryKey(id, name = "PK_User_ID") // name is optional here
}

object Cities : Table() {
    val id = integer("id").autoIncrement() // Column<Int>
    val name = varchar("name", 50) // Column<String>

    override val primaryKey = PrimaryKey(id, name = "PK_Cities_ID")
}

fun main() {
    (Users innerJoin Cities).slice(Users.name, Cities.name)
        .select {
            (Users.id.eq("andrey") or Users.name.eq("Sergey")) and
                Users.id.eq("sergey") and Users.cityId.eq(Cities.id)
        }.forEach {
            println("${it[Users.name]} lives in ${it[Cities.name]}")
        }
}
```

- テーブルスキーマをコードで表記し、使ってる DB に合わせて DDL を自動生成
- クエリをコードで表記し、使っている DB に合わせて DML を自動生成
- **構文的に問題がある DDL/DML はコンパイルエラーになるため、そもそもビルドできない**
- Kotlin などの altJava の柔軟な型システムを使った **クエリリザルト → エンティティ or DTO への型チェック**
- エンティティ or DTO で簡単にテストデータを用意でき、高速なテストを実現

抜粋した Exposed の利用例は Kotlin の演算子オーバーライドとメソッドの中置記法を利用して、かなり DSL らしく記述されている。

## まとめ

柔軟な型システムをもつ言語の登場により、ORM フレームワークに大きくパラダイムシフトが起こりつつある、ということを Kotlin の ORM, [Exposed](https://github.com/JetBrains/Exposed) を見て思うなどした。
