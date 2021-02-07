---
title: "統計"
date: 2021-02-07T22:06:02+09:00
tags: ["勉強ノート", "数学", "統計学"]
---

## データの種類

### 質的変数

種類 (ex. 性別, 血液型) を区別するような変数。中でも性別のように 2 種類の値しかとらない質的変数を**2 値変数**と呼ぶ。

質的変数は尺度水準によって以下のように細かく分類できる。

名義尺度
: 単に分類するための変数。 (ex. 生徒番号, 電話番号, 性別)

順序尺度
: 順序関係や大小関係に意味のある変数。 (ex. 成績の順位, アンケートの満足度)

### 量的変数

量 (ex. 身長, テストの点数) を表現する変数。

量的変数は尺度水準によって以下のように細かく分類できる。

間隔尺度
: 大小関係に加え、差に意味がある変数。 (ex. 西暦, 温度)

比例尺度
: 大小関係, 差, 比すべてに意味がある変数。

## データの指標

### 平均

平均 (mean) は、すべてのデータを合計してデータ数で割った値。

$$\overline{x}=\frac{1}{n}\sum_{i=1}^n$$

### 中央値

中央値 (median) は、データを降順に並べたときに中央に位置する値。データ数が偶数のときは中央に位置する 2 つの値の平均値となる。

### 最頻値

最頻値 (mode) は、データの中で最も多く出現する値。

### 偏差

偏差 (deviation) は、各データと平均値の差。

### 分散

分散 (variance) は、偏差の 2 乗を合計したもので、データのばらつきを表す指標。

$$S^2=\frac{1}{n}\sum_{i=1}^n(x_i-\overline{x})^2$$

### 標準偏差

標準偏差 (standard deviation) は、分散のルートをとった、データと同じ単位をもつデータのばらつきを表す指標。

$$S=\sqrt{S^2}=\sqrt{\frac{1}{n}\sum_{i=1}^n(x_i-\overline{x})^2}$$

### 四分位範囲

データの下位 25%, 50%, 75% に位置する値を第 1 四分位数, 第 2 四分位数, 第 3 四分位数といい、それぞれ $Q_1,Q_2,Q_3$ で表す。
(第 2 四分位数 $Q_2$ は中央値に一致する)

このとき $\text{IQR}=Q_3-Q_1$ を四分位範囲 (interquartile range) という。


<!-- TODO データの整理, 表やグラフについて書く -->

### 共分散

共分散 (covariance) は 2 組の対応するデータの偏差積の平均値。

$$S_{xy}=\frac{1}{n}\sum_{i=1}^n(x_i-\overline{x})(y_i-\overline{y})$$

### 相関係数

相関係数 (correlation coefficient) は 2 つの確率変数の間にある関係の強弱を測る指標で、-1 から 1 の値をとる。

$$r_{xy}=\frac{S_{xy}}{S_xS_y}$$

1. $r_{xy}>0$ のとき、データは**正の相関**をもつ
1. $r_{xy}=0$ のとき、データは**無相関**
1. $r_{xy}<0$ のとき、データは**負の相関**をもつ

## 推測統計

### 母集団と標本

推測統計では観測対象全体の統計的性質を、その観測対象の一部分のみを使って推測する。

母集団 (population)
: 推測したい観測対象全体

母数
: 母集団の平均, 分散, 相関係数の総称

標本 (sample)
: 推測に使う観測対象の一部分

標本統計量
: 標本から計算される平均, 分散, 相関係数

標本抽出 (sampling)
: 母集団から標本を取り出すこと

無作為抽出 (random sampling)
: ランダムに標本抽出を行うこと

サンプルサイズ
: 取り出す標本の数

### 確率

確率変数 (random variable)
: とりうる値とその確率が決まっているもの

試行 (trial)
: 確率変数の結果を観測すること

事象 (event)
: 試行の結果起こりうること

根本事象 (elementary event)
: これ以上分解することのできない事象

## 確率変数

### 期待値

確率変数 $X$ を無限回試行して得られた実現値の平均を**期待値** (expected value) といい、離散型確率変数 $X$ の期待値は $\mu, E(X)$ で表す。

期待値について、常に以下の式が成り立つ。

$$E(aX+b)=aE(X)+b$$

このような性質を**線形性**という。

### 分散

確率変数の分散も、データの分散と同様にばらつきを表す指標であり、離散型確率変数 $X$ の分散は $\sigma^2,V(X)$ で表す。

分散について、常に以下の式が成り立つ。

$$V(aX+b)=a^2V(X)$$

## 離散型確率変数

確率変数 $X$ が $x$ という値をとる確率を、**確率質量関数** (PMF = Probability Mass Function) $f(x)$ で表す。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x)&=P(X=x)\\\\E(X)&=\sum_kx_kf(x_k)\\\\V(X)&=\sum_k(x_k-\mu)^2f(x_k)\end{aligned}$$
<!-- prettier-ignore-end -->

確率の性質より、離散型確率変数は以下の 2 つの式を満たす。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x_k)&\ge0\\\\\sum_kf(x_k)&=1\end{aligned}$$
<!-- prettier-ignore-end -->

## 離散型確率分布

### ベルヌーイ分布

ベルヌーイ分布 (Bernoulli distribution) は最も基本的な確率分布で、とりうる値が $\{0,1\}$ しかない確率分布である。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x)&=\begin{cases}p^x(1-p)^{1-x}&(x\in\{0,1\})\\\\0&(\text{otherwise})\end{cases}\\\\E(X)&=p\\\\V(X)&=p(1-p)\end{aligned}$$
<!-- prettier-ignore-end -->

### 二項分布

二項分布 (binomial distribution) は成功確率が $p$ のベルヌーイ試行を $n$ 回行った時の成功回数が従う確率分布であり、その分布を $B(n,p)$ で表す。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x)&=\begin{cases}_nC_xp^x(1-p)^{x-k}&(x\in\{0,1,\dots,n\})\\\\0&(\text{otherwise})\end{cases}\\\\E(X)&=np\\\\V(X)&=np(1-p)\end{aligned}$$
<!-- prettier-ignore-end -->

$B(n,p)$ に従う確率変数 $X$ と $B(m,p)$ に従う確率変数 $Y$ が互いに独立であるとき、確率変数の和 $X+Y$ は $B(n+m,p)$ に従う。 (**再生性**)

### 幾何分布

幾何分布 (geometric distribution) はベルヌーイ試行を繰り返して、初めて成功するまでの試行回数が従う確率分布である。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x)&=\begin{cases}p(1-p)^{x-1}&(x\in\{1,2,3,\dots\})\\\\0&(\text{otherwise})\end{cases}\\\\E(X)&=\frac{1}{p}\\\\P(X)&=\frac{1-p}{p^2}\end{aligned}$$
<!-- prettier-ignore-end -->

### ポアソン分布

ポアソン分布はランダムな事象が単位時間あたりに発生する件数が従う確率分布である。

ポアソン分布は、二項分布 $B(n,p)$ において $n$ が大きく $p$ が小さい場合の近似となる。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x)&=\begin{cases}\frac{\lambda^x}{x!}\cdot e^{-\lambda}&(x\in\{0,1,2,\dots\})\\\\0&(\text{otherwise})\end{cases}\\\\E(X)&=\lambda\\\\V(X)&=\lambda\end{aligned}$$
<!-- prettier-ignore-end -->

## 連続型確率変数

### 確率密度関数

連続型確率変数は**確率密度関数** (PDF = Probability Density Function) $f(x)$ で表す。

確率変数 $X$ が $x_0\le X \le x_1$ の区間に入る確率 $P(x_0\le X \le x_1)$ を、確率密度関数 $f(x)$ を用いて次のように表す。

<!-- prettier-ignore-start -->
$$\begin{aligned}P(x_0\le X\le x_1)&=\int_{x_0}^{x_1}f(x)dx\\\\\mu=E(X)&=\int_{-\infty}^\infty xf(x)dx\\\\\sigma^2=V(X)&=\int_{-\infty}^\infty(x-\mu)^2f(x)dx\end{aligned}$$
<!-- prettier-ignore-end -->

### 確率の性質

確率の性質より、連続型確率変数は以下の 2 つの式を満たす。

<!-- prettier-ignore-start -->
$$\begin{aligned}f(x)&\ge0\\\\\int_{-\infty}^\infty f(x)dx&=1\end{aligned}$$
<!-- prettier-ignore-end -->

### 類型分布関数

確率変数 $X$ が $k$ 以下になる時の確率は**類型分布関数** (CDF = Cumulative Distribution Function) $F(k)$ で表す。

$$F(x)=P(X\le x)=\int_{-\infty}^{x}f(x)dx$$

## 連続型確率分布

### 正規分布

正規分布 (normal distribution, ガウス分布, Gaussian distribution) は、自然界の多くの事象を表現できる確率分布である。
期待値が $\mu$, 分散が $\sigma^2$ であるような正規分布を $N(\mu,\sigma^2)$ で表す。

$$f(x)=\frac{1}{\sqrt{2\pi}\sigma}\exp\{-\frac{(x-\mu)^2}{2\sigma^2}\}$$

正規分布に従う確率変数を標準化した確率変数が従う $N(0,1)$ を**標準正規分布**という。

## 参考文献

- 谷合 廣紀, Python で理解する統計解析の基礎, 2018
- Wikipedia, [共分散](https://ja.wikipedia.org/wiki/%E5%85%B1%E5%88%86%E6%95%A3)
- Wikipedia, [相関係数](https://ja.wikipedia.org/wiki/%E7%9B%B8%E9%96%A2%E4%BF%82%E6%95%B0)
- Wikipedia, [二項分布](https://ja.wikipedia.org/wiki/%E4%BA%8C%E9%A0%85%E5%88%86%E5%B8%83)
