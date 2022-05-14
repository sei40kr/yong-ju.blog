---
title: "確率統計"
date: 2021-02-07T22:06:02+09:00
categories: ["数学", "機械学習"]
tags: ["勉強ノート", "大学数学"]
---

## データの種類

### 質的変数

質的変数は種類 (性別, 血液型など) を区別するような変数である。
中でも性別のように2種類の値しかとらない質的変数を**2値変数**と呼ぶ。

質的変数は尺度水準によって以下のように分類できる。

名義尺度
: 単に分類するための変数。 (生徒番号, 電話番号, 性別など)

順序尺度
: 順序関係や大小関係に意味のある変数。 (成績の順位, アンケートの満足度など)

### 量的変数

量的変数は量 (身長, テストの点数など) を表現する変数である。

量的変数は尺度水準によって以下のように分類できる。

間隔尺度
: 大小関係, 差に意味がある変数。 (西暦など)

比例尺度
: 間隔尺度の性質 (大小関係, 差) に加え、比にも意味がある変数。

{{< hint info >}}
摂氏 (℃), 華氏 (°F) 表記の温度は間隔尺度であるが、比例尺度ではない。
一方でケルビン (K) 表記の温度は比例尺度である。
{{< /hint >}}

## データの指標

### 平均値

**平均値 (mean)** は、すべてのデータを合計してデータ数で割った値である。

{{< katex display >}}
\overline{x}=\frac{1}{n}\sum_{i=1}^n{x_i}
{{< /katex >}}

{{< hint info >}}
「平均値」を意味する英単語には mean の他に average がある。

統計学では、mean は「平均値」を表すのに対し、average は「代表値」を表す。
代表値とは、平均値を含む中央値 (後述), 最頻値 (後述) など、分布の中心的位置を表す数値の総称である。
{{< /hint >}}

### 分散

分散 (variance) は、偏差の2乗を合計したもので、データのばらつきを表す指標。

{{< katex display >}}
S^2=\frac{1}{n}\sum_{i=1}^n(x_i-\overline{x})^2
{{< /katex >}}

### 中央値

中央値 (メジアン, median) は、データを降順に並べたときに中央に位置する値である。
データ数が偶数のときは中央に位置する2つの値の平均値となる。

### 最頻値

最頻値 (モード, mode) は、データの中で最も多く出現する値である。

### 偏差

偏差 (deviation) は、各データと平均値の差である。

### 標準偏差

標準偏差 (standard deviation) は、分散のルートをとった、データと同じ単位をもつデータのばらつきを表す指標。

{{< katex display >}}
S=\sqrt{S^2}=\sqrt{\frac{1}{n}\sum_{i=1}^n(x_i-\overline{x})^2}
{{< /katex >}}

### 四分位範囲

データの下位 25%, 50%, 75% に位置する値を第 1 四分位数, 第 2 四分位数, 第 3 四分位数といい、それぞれ {{< katex >}}Q_1,Q_2,Q_3{{< /katex >}} で表す。
(第 2 四分位数 {{< katex >}}Q_2{{< /katex >}} は中央値に一致する)

このとき {{< katex >}}\text{IQR}=Q_3-Q_1{{< /katex >}} を四分位範囲 (interquartile range) という。

### 共分散

共分散 (covariance) は 2 組の対応するデータの偏差積の平均値。

{{< katex display >}}
S_{xy}=\frac{1}{n}\sum_{i=1}^n(x_i-\overline{x})(y_i-\overline{y})
{{< /katex >}}

### 相関係数

相関係数 (correlation coefficient) は 2 つの確率変数の間にある関係の強弱を測る指標で、-1 から 1 の値をとる。

{{< katex display >}}
r_{xy}=\frac{S_{xy}}{S_xS_y}
{{< /katex >}}

1. {{< katex >}}r_{xy}>0\iff\text{データは正の相関をもつ}{{< /katex >}}
1. {{< katex >}}r_{xy}=0{{< /katex >}} のとき、データは**無相関**
1. {{< katex >}}r_{xy}<0{{< /katex >}} のとき、データは**負の相関**をもつ

## データの整理

### 標準化

データから平均を引き、標準偏差で割る操作を標準化 (standardization) という。標準化されたデータを Z スコア (z-score) といい、平均が 0, 標準偏差が 1 となる。

{{< katex display >}}
z_i=\frac{x_i-\overline{x}}{S}
{{< /katex >}}

<!-- TODO データの整理, 表やグラフについて書く -->

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
: ランダムに標本抽出する

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
: これ以上分解できない事象

## 確率変数

### 期待値

確率変数 {{< katex >}}X{{< /katex >}} を無限回試行して得られた実現値の平均を**期待値 (expected value)** といい、以下 {{< katex >}}E(X){{< /katex >}} で表す。

また、期待値について以下の式が成り立つ。

{{< katex display >}}
E[aX+b]=aE[X]+b
{{< /katex >}}

{{< hint info >}}
このような性質を**線形性 (linearity)**という。
{{< /hint >}}

### 分散

確率変数 {{< katex >}}X{{< /katex >}} における分散もデータの分散と同様にばらつきを表す指標であり、以下 {{< katex >}}V[X]{{< /katex >}} で表す。

分散について、常に以下の式が成り立つ。

{{< katex display >}}
\begin{aligned}
V[X]&=E[(E[X]-X)^2]\\
&=E[X^2]-E[X]^2\\
V[aX+b]&=a^2V[X]\\
\end{aligned}
{{< /katex >}}

{{< details title="V[X]=E[X^2]-E[X]^2 の証明" >}}
{{< katex display >}}
\begin{aligned}
V[X]&=E[(X-E[X])^2]\\
&=E[X^2-2E[X]X-E[X]^2]\\
&=E[X^2]-2E[X]^2+E[X]^2\\
&=E[X^2]-E[X]^2
\end{aligned}
{{< /katex >}}
{{< /details >}}

## 離散型確率変数

飛び飛びの値をとる (離散的である) 確率変数を **離散型確率変数 (discrete random variable)** という。

離散型確率分布において、{{< katex >}}X=x{{< /katex >}} となる確率 {{< katex >}}P[X=x]{{< /katex >}} を返す関数を、**確率質量関数 (Probability Mass Function, PMF)** といい、以下 {{< katex >}}f(x){{< /katex >}} で表す。

{{< katex >}}X{{< /katex >}} が離散型確率変数であるとき、以下が成り立つ。

{{< katex display >}}
\begin{aligned}
E[X]&=\sum_kx_kf(x_k)\\
V[X]&=\sum_k(x_k-\mu)^2f(x_k)
\end{aligned}
{{< /katex >}}

また、確率の性質より以下が自明に成り立つ。

{{< katex display >}}
0\le f(x_i)\le1\\
\sum_kf(x_k)=1
{{< /katex >}}

## 連続型確率変数

連続した値をとる確率変数を **連続的確率変数 (continuous random variable)** という。

連続型確率変数 {{< katex >}}X{{< /katex >}} が {{< katex >}}x_0\le X\le x_1{{< /katex >}} を満たす確率 {{< katex >}}P[x_0\le x\le x_1]{{< /katex >}} が

{{< katex display >}}
P[x_0\le x\le x_1]=\int_{x_0}^{x_1}f(x)dx
{{< /katex >}}

を満たすよう定義した {{< katex >}}f(x){{< /katex >}} を**確率密度関数 (Probability Density Function, PDF)** という。

{{< katex >}}X{{< /katex >}} が連続型確率変数であるとき、以下が成り立つ。

{{< katex display >}}
\begin{aligned}
E[X]&=\int_{-\infty}^\infty xf(x)dx\\
V[X]&=\int_{-\infty}^\infty(x-E[X])^2f(x)dx
\end{aligned}
{{< /katex >}}

また、確率の性質より以下が自明に成り立つ。

{{< katex display >}}
0\le f(x)\le1\\
\int_{-\infty}^\infty f(x)dx=1
{{< /katex >}}

## ベルヌーイ分布

確率 {{< katex >}}p{{< /katex >}} で {{< katex >}}1{{< /katex >}}、それ以外の場合 (確率 {{< katex >}}1-p{{< /katex >}}) に {{< katex >}}0{{< /katex >}} をとる、最も基本的な離散型確率分布を **ベルヌーイ分布 (Bernoulli distribution)** といい、以下 {{< katex >}}\text{Bern}(p){{< /katex >}} で表す。

{{< katex >}}\text{Bern}(p){{< /katex >}} の密度関数は次のようになる。

{{< katex display >}}
f(x)=\begin{cases}p^x(1-p)^{1-x}&(x\in\{0,1\})\\
0&(\text{otherwise})
\end{cases}
{{< /katex >}}

{{< katex >}}X\sim\text{Bern}(p){{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
E[X]&=p\\
V[X]&=p(1-p)
\end{aligned}
{{< /katex >}}

{{< details title="V[X] の導出" >}}
{{< katex display >}}
\begin{aligned}
V[X]&=E[(X-E[X])^2]\\
&=E[X^2]-E[X]^2\\
&=p-p^2\\
&=p(1-p)
\end{aligned}
{{< /katex >}}
{{< /details >}}

## 二項分布

成功確率が {{< katex >}}p{{< /katex >}} であるベルヌーイ試行を {{< katex >}}n{{< /katex >}} 回行った時の成功回数が従う離散型確率分布を **二項分布 (binomial distribution)** といい、以下 {{< katex >}}\text{Bin}(n,p){{< /katex >}} で表す。

{{< katex >}}\text{Bin}(n,p){{< /katex >}} の密度関数は次のようになる。

{{< katex display >}}
f(x)=\begin{cases}
_nC_xp^x(1-p)^{x-k}&(x\in\{0,1,\dots,n\})\\
0&(\text{otherwise})
\end{cases}
{{< /katex >}}

{{< katex >}}X\sim\text{Bin}(n,p){{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
E[X]&=np\\
V[X]&=np(1-p)
\end{aligned}
{{< /katex >}}

確率変数 {{< katex >}}X\sim\text{Bin}(n,p){{< /katex >}} と {{< katex >}}Y\sim\text{Bin}(m,p){{< /katex >}} が互いに独立であるとき、確率変数の和 {{< katex >}}X+Y{{< /katex >}} は {{< katex >}}\text{Bin}(n+m,p){{< /katex >}} に従う。 (**再生性**)

<!-- TODO V[X] の導出 -->

## 幾何分布

成功確率が {{< katex >}}p{{< /katex >}} であるベルヌーイ試行を繰り返し、初めて成功するまでの試行回数が従う離散型確率分布を
**幾何分布 (geometric distribution)** といい、以下 {{< katex >}}\text{Ge}(p){{< /katex >}} で表す。

{{< katex >}}\text{Ge}(p){{< /katex >}} の密度関数は次のようになる。

{{< katex display >}}
f(x)=\begin{cases}
p(1-p)^{x-1}&(x\in\{1,2,3,\dots\})\\
0&(\text{otherwise})
\end{cases}
{{< /katex >}}

{{< katex >}}X\sim\text{Ge}(p){{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
E[X]&=\frac{1}{p}\\
P[X]&=\frac{1-p}{p^2}
\end{aligned}
{{< /katex >}}

が成り立つ。

## ポアソン分布

単位時間当たり平均 {{< katex >}}\lambda{{< /katex >}} 回発生する事象が単位時間に起こる件数が従う離散型確率分布を **ポアソン分布 (Poisson distribution)** といい、以下 {{< katex >}}\text{Poi}(\lambda){{< /katex >}} で表す。

{{< katex >}}\text{Poi}(\lambda){{< /katex >}} の密度関数は次のようになる。

{{< katex display >}}
f(x)=\begin{cases}
\dfrac{\lambda^x}{x!}\cdot e^{-\lambda}&(x\in\{0,1,2,\dots\})\\
0&(\text{otherwise})
\end{cases}
{{< /katex >}}

{{< katex >}}X\sim\text{Poi}(\lambda){{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
E[X]&=\lambda\\
V[X]&=\lambda
\end{aligned}
{{< /katex >}}

が成り立つ。

ポアソン分布は、二項分布 {{< katex >}}\text{Bin}(n,p){{< /katex >}} において {{< katex >}}n{{< /katex >}} が大きく {{< katex >}}p{{< /katex >}} が小さい場合の近似となる。

{{< details title="二項分布からポアソン分布の導出 (ポアソンの極限定理)" >}}
{{< katex display >}}
\begin{aligned}
\text{Poi}(\lambda)&=\lim_{\lambda=np,n\rightarrow=\infty}{}_nC_kp^k(1-p)^{n-k}\\
&=\lim_{n\rightarrow\infty}\frac{n!}{(n-k)!k!}(\frac{\lambda}{n})^k(1-\frac{\lambda}{n})^{n-k}\\
&=\lim_{n\rightarrow\infty}\frac{n(n-1)(n-2)\cdots(n-k+1)}{k!}(\frac{\lambda}{n})^k(1-\lambda)^{n-k}\\
&=\lim_{n\rightarrow\infty}(\frac{n}{n})(\frac{n-1}{n})(\frac{n-2}{n})\cdots(\frac{n-k+1}{n})(\frac{\lambda^k}{k!})(1-\frac{\lambda}{n})^n(1-\frac{\lambda}{n})^{-k}\\
&=1\cdot1\cdot1\cdots1(\frac{\lambda^k}{k!})e^{-\lambda}\cdot1\\
&=\frac{\lambda^ke^{-\lambda}}{k!}
\end{aligned}
{{< /katex >}}
{{< /details >}}

<!-- TODO E[X], V[X] の導出 -->

## 指数分布

単位時間当たり平均 {{< katex >}}\lambda{{< /katex >}} 回発生する事象の発生間隔が従う連続型確率分布を**指数分布 (exponential distribution)** といい、以下 {{< katex >}}\text{Ex}(\lambda){{< /katex >}} で表す。

{{< katex >}}\text{Ex}(\lambda){{< /katex >}} の密度関数は次のようになる。

{{< katex display >}}
f(x)=\begin{cases}
\lambda e^{-\lambda x}&(x\ge0)\\
0&(\text{otherwise})
\end{cases}
{{< /katex >}}

<!-- TODO 指数分布の導出 -->

{{< katex >}}X\sim Ex(\lambda){{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
E[X]&=\dfrac1\lambda\\
V[X]&=\dfrac1{\lambda^2}
\end{aligned}
{{< /katex >}}

が成り立つ。

---

{{< hint info >}}
単位時間当たり平均 {{< katex >}}\lambda{{< /katex >}} 回発生する事象の

- **単位時間に起こる件数**は {{< katex >}}\text{Poi}(\lambda){{< /katex >}} (ポアソン分布) に従う。
- **発生間隔**は {{< katex >}}\text{Ex}(\lambda){{< /katex >}} (指数分布) に従う。
{{< /hint >}}

## 正規分布

自然界の多くの事象が従う、期待値が {{< katex >}}\mu{{< /katex >}}、分散が {{< katex >}}\sigma^2{{< /katex >}} となる **左右対称・釣り鐘型** の連続型確率分布を **正規分布 (normal distribution)** あるいは **ガウス分布 (Gaussian distribution)** といい、以下 {{< katex >}}\text{N}(\mu,\sigma^2){{< /katex >}} で表す。

{{< katex display >}}
f(x)=\frac{1}{\sqrt{2\pi}\sigma}\exp\left\{-\frac{(x-\mu)^2}{2\sigma^2}\right\}
{{< /katex >}}

{{< katex >}}X\sim\text{N}(\mu,\sigma^2){{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
E[X]&=\mu\\
V[X]&=\sigma^2
\end{aligned}
{{< /katex >}}

また、{{< katex >}}X\sim \text{N}(\mu,\sigma^2){{< /katex >}} のとき

{{< katex display >}}
aX+b\sim\text{N}(a\mu+b,a^2\sigma^2)
{{< /katex >}}

が成り立つ。

よって、確率変数 {{< katex >}}X{{< /katex >}} を標準化した確率変数 {{< katex >}}Z=\dfrac{X-\mu}\sigma{{< /katex >}} は {{< katex >}}\text{N}(0,1){{< /katex >}} に従う。
このように {{< katex >}}\mu=0,\sigma^2=1{{< /katex >}} であるような正規分布 {{< katex >}}\text{N}(0,1){{< /katex >}} を特に {{< katex >}}\text{N}(0,1){{< /katex >}} を **標準正規分布** という。

## カイ二乗分布

確率変数 {{< katex >}}Z_1,Z_2,\dots,Z_n{{< /katex >}} が互いに独立で {{< katex >}}\text{N}(0,1){{< /katex >}} に従うとする。
このとき、それらの二乗和 {{< katex >}}\sum_{i=0}^nZ_i^2{{< /katex >}} が従う連続型確率分布を**自由度 {{< katex >}}n{{< /katex >}} のカイ二乗分布 (chi-square distribution)** といい、以下 {{< katex >}}\chi^2(n){{< /katex >}} で表す。

## t分布

確率変数 {{< katex >}}Z,Y{{< /katex >}} が互いに独立で、{{< katex >}}Z\sim\text{N}(0,1),Y\sim\chi^2(n){{< /katex >}} とする。
このとき、{{< katex >}}t=\dfrac{Z}{\sqrt{Y/n}}{{< /katex >}} が従う連続型確率分布を**自由度 {{< katex >}}n{{< /katex >}} のt分布 (t distribution)** といい、以下 {{< katex >}}t(n){{< /katex >}} で表す。

## マルコフの不等式

{{< katex >}}X{{< /katex >}} を非負の値を取る確率変数とする。
このとき、任意の {{< katex >}}c>0{{< /katex >}} に対して

{{< katex display >}}
P[X\ge c]\le\frac{E[X]}c
{{< /katex >}}

が成り立つ。

{{< details title="証明" >}}
{{< katex display >}}
\begin{aligned}
E[X]&=\int_0^\infty xf_X(x)dx\\
&=\int_0^c xf_X(x)dx+\int_c^\infty xf_X(x)dx
\end{aligned}
{{< /katex >}}

{{< katex >}}\int_0^cxf_X(x)dx\ge0{{< /katex >}} より

{{< katex display >}}
E[X]\le\int_c^\infty xf_X(x)dx
{{< /katex >}}

{{< katex >}}x\ge c{{< /katex >}} より

{{< katex display >}}
\begin{aligned}
E[X]&\ge c\int_c^\infty f_X(x)dx\\
&\ge cP[x\ge c]\\
\therefore P[x\ge c]&\le\frac{E[X]}c
\end{aligned}
{{< /katex >}}
{{< /details >}}

## チェビシェフの不等式

{{< katex >}}E[Y]=\mu,V[Y]=\sigma^2{{< /katex >}} とする。
このとき、任意の {{< katex >}}a>0{{< /katex >}} に対して

{{< katex display >}}
P[|x-\mu|\ge a\sigma]\le\frac1{a^2}
{{< /katex >}}

が成り立つ。

{{< details title="証明" >}}
マルコフの不等式において {{< katex >}}X=(Y-\mu)^2,c=a^2\sigma^2{{< /katex >}} とすると

{{< katex display >}}
\begin{aligned}
P[(Y-\mu)^2\ge a^2\sigma^2]&\le\frac{E[(Y-\mu)^2]}{a^2\sigma^2}\\
P[|Y-\mu|\ge a\sigma]&\le\frac1{a^2}
\end{aligned}
{{< /katex >}}
{{< /details >}}

## 参考文献

- 谷合 廣紀, Python で理解する統計解析の基礎, 2018
- Wikipedia, [共分散](https://ja.wikipedia.org/wiki/%E5%85%B1%E5%88%86%E6%95%A3)
- Wikipedia, [相関係数](https://ja.wikipedia.org/wiki/%E7%9B%B8%E9%96%A2%E4%BF%82%E6%95%B0)
- Wikipedia, [二項分布](https://ja.wikipedia.org/wiki/%E4%BA%8C%E9%A0%85%E5%88%86%E5%B8%83)
