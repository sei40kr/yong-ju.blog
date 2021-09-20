---
title: "数値計算"
date: 2021-01-20T02:36:44+09:00
categories: ["数値計算"]
tags: ["勉強ノート"]
---

## 整数の表現

コンピュータ内部では電気信号の有無を0と1に割り当て2進法で数値を表現する。

### 符号付整数型

符号付整数型 (signed integer type) は最上位ビット (most significant bit, MSB) を符号ビットに割り当て、**0ならば値が0か正、1ならば値が負**であることを表す。
他のビットは**仮数部**と呼ばれ、正の数であれば数値を、負の数であれば数値の絶対値を**2の補数** (後述) で表すのが一般的である。

### 2の補数

**2の補数 (2's complement)** は負の値を表現する方法の1つであり、元の値のすべてのビットを反転したものに1を加算した数値である。

前述の符号ビットと組み合わせると、**負の数を含む加算 (と減算) を同じ加算器で扱うことができる。**

### 精度

整数型は一般的に16ビット (`short`), 32ビット (`int`), 64ビット (`long`, `long long`) のいずれかで表される。

{{< hint info >}}
整数型のビット数は実装に依存することもある。
例えば、C/C++の `long` やRust の `usize` のビット数は実装 (プラットフォーム) 依存である。
{{< /hint >}}

整数型のビット数を {{< katex >}}b{{< /katex >}} とすると、表現可能な数値 {{< katex >}}x{{< /katex >}} の範囲は {{< katex >}}0\le x\le2^b-1{{< /katex >}} となる。
ただし、符号付整数型ではMSBが符号ビットになるため、表現可能な数値 {{< katex >}}x{{< /katex >}} の範囲は {{< katex >}}-2^{b-1}\le x\le2^{b-1}-1{{< /katex >}} となる。

### 整数の計算エラー

オーバーフロー
: 演算結果が格納域の記録できる範囲を超えてしまうと、最上位桁より上への繰り上がり (キャリー) が失われたり、本来演算結果を格納する場所とは違うビット (符号ビットなど) に格納される場合がある。
この現象を **(算術)オーバーフロー (overflow)** という。

<!-- TODO アンダーフローについて書く -->

## 浮動小数点数の表現

浮動小数点数型では以下に示す情報で数値を表現する。

- 符号
- 仮数 (significand)
- 基数 (base)
- 指数 (exponent)

数値の絶対値は以下の式で表される。

{{< katex display >}}
\begin{aligned}
&=s\times b^{e}\\
s&:仮数\\
b&:基数\\
e&:指数
\end{aligned}
{{< /katex >}}

#### IEEE 754

IEEE標準のひとつであるIEEE 754 (IEEE Standard for Floating-Point Arithmetic) で定められている浮動小数点数の方式を以下に示す。

| 方式                        | 符号ビット | 指数部の長さ (bits) | 仮数部の長さ (bits) | 指数部のゲタ |
| :-----------------          | :--------- | ------------------: | ------------------: | -----------: |
| 半精度浮動小数点数          | 1 ビット   | 5                   | 10                  | 15           |
| 単精度浮動小数点数 (float)  | 1 ビット   | 8                   | 23                  | 127          |
| 倍精度浮動小数点数 (double) | 1 ビット   | 11                  | 52                  | 1023         |

### 小数点数の計算エラー

丸め誤差 (rounding error)
: 数値のどこかの桁で切り上げ/捨てなど端数処理を行った場合に生じる誤差。

打ち切り誤差 (truncation error)
: 反復計算において、必要とされる回数より少ない回数で反復を止める (打ち切り) によって生じる誤差。

情報落ち (loss of trailing digits)
: 精度が限られている条件下で、絶対値の大きい数と絶対値の小さい数を加減算したときに、絶対値の小さい数が無視されてしまう現象。

桁落ち (cancellation)
: 値がほぼ等しく、丸め誤差をもつ数値同士の減算したときに、有効数字が減る現象。

{{< hint info >}}
数値計算の誤差によって引き起こされた事故として

- 湾岸戦争でのスカッドミサイルの迎撃の失敗
- アリアン5ロケットの発射の失敗

などが挙げられる。
{{< /hint >}}

### Rumpの例題

{{< katex display >}}
f(a,b)=333.75b^6+a^2(11a^2b^2-b^6-121b^4-2)+5.5b^8+\frac{a}{2b}
{{< /katex >}}

ここで、{{< katex >}}a=77617.0,b=33096.0{{< /katex >}} のときの {{< katex >}}f(a,b){{< /katex >}} を計算する。

- 単精度浮動小数点数で計算すると {{< katex >}}f(a,b)\approx1.172603\dots{{< /katex >}} が得られる。
- 倍精度浮動小数点数で計算すると {{< katex >}}f(a,b)\approx1.1726039400531\dots{{< /katex >}} が得られる。
- 真の値は {{< katex >}}f(a,b)=-0.82739605\dots{{< /katex >}} である。

Rumpの例題はこのように

> ある演算精度での計算結果とそれより高い演算精度での計算結果を比較したときに、双方の値が近ければ、その値はある程度は正しい。

という直感に対する反例である。

### 精度保証付き数値計算

精度保証付き数値計算とは、数学的で厳密な誤差の評価を伴う数値計算のことをいう。

### 任意精度演算

任意精度演算とは、数値の精度に限りがない演算システム (またはデータ構造) のことをいう。

有名な任意精度演算をサポートするデータ構造として、Javaの `BigInteger` (整数), `BigDecimal` (小数点数) などがある。

- [BigInteger (Java SE8)](https://docs.oracle.com/javase/jp/8/docs/api/java/math/BigInteger.html)
- [BigDecimal (Java SE8)](https://docs.oracle.com/javase/jp/8/docs/api/java/math/BigDecimal.html)

## 参考文献

- Wikipedia, [コンピュータの数値表現](https://ja.wikipedia.org/wiki/%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%82%BF%E3%81%AE%E6%95%B0%E5%80%A4%E8%A1%A8%E7%8F%BE)
- Wikipedia, [整数型](https://ja.wikipedia.org/wiki/%E6%95%B4%E6%95%B0%E5%9E%8B)
- Wikipedia, [2の補数](https://ja.wikipedia.org/wiki/2%E3%81%AE%E8%A3%9C%E6%95%B0)
- Wikipedia, [算術オーバーフロー](https://ja.wikipedia.org/wiki/%E7%AE%97%E8%A1%93%E3%82%AA%E3%83%BC%E3%83%90%E3%83%BC%E3%83%95%E3%83%AD%E3%83%BC)
- Wikipedia, [浮動小数点数](https://ja.wikipedia.org/wiki/%E6%B5%AE%E5%8B%95%E5%B0%8F%E6%95%B0%E7%82%B9%E6%95%B0)
- Wikipedia, [数値解析](https://ja.wikipedia.org/wiki/%E6%95%B0%E5%80%A4%E8%A7%A3%E6%9E%90)
- Wikipedia, [誤差](https://ja.wikipedia.org/wiki/%E8%AA%A4%E5%B7%AE)
