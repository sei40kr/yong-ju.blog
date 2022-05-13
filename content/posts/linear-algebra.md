---
title: "線形代数"
date: 2021-04-08T03:07:05+09:00
categories: ["数学"]
tags: ["線形代数", "行列", "大学数学", "数学", "勉強ノート"]
---

## 一次独立

いずれも {{< katex >}}\bold{0}{{< /katex >}} でないベクトル {{< katex >}}\bold{a_1,a_2,\dots,a_n}{{< /katex >}} について {{< katex >}}c_1\bold{a_1}+c_2\bold{a_2}+\cdots+c_n\bold{a_n}=\bold{0}{{< /katex >}} が成り立つのが {{< katex >}}c_1=c_2=\cdots=c_n=0{{< /katex >}} だけの場合、{{< katex >}}\bold{a_1,a_2,\dots,a_n}{{< /katex >}} を**一次独立 (linearly independent)** という。
また、一次独立でないものを**一次従属 (linearly dependent)** という。

### 定理

あるベクトル {{< katex >}}\bold{b}{{< /katex >}} が一次独立なベクトル {{< katex >}}\bold{a_1,a_2,\dots,a_n}{{< /katex >}} の線型結合で表されるとき、その表し方は1通りである。

{{< details title="証明" >}}
別の数の組 {{< katex >}}\{c_1,\dots,c_n\}{{< /katex >}} と {{< katex >}}\{c_1',\dots,c_n'\}{{< /katex >}} を用いて

{{< katex display >}}
\begin{aligned}
\bold{b}&=c_1\bold{a_1}+\cdots+c_n\bold{a_n}\\
\bold{b}&=c_1'\bold{a_1}+\cdots+c_n'\bold{a_n}
\end{aligned}
{{< /katex >}}

と2通りの表し方ができると仮定する。

このとき

{{< katex display >}}
(c_1-c_1')\bold{a_1}+\cdots+(c_n-c_n')\bold{a_n}=\bold{0}
{{< /katex >}}

となる。ここで {{< katex >}}\bold{a_1,\dots,a_n}{{< /katex >}} は一次独立であるので

{{< katex display >}}
c_1-c_1'=\cdots=c_n-c_n'=0\\
\therefore c_1=c_1',\dots,c_n=c_n'
{{< /katex >}}

となり、これは矛盾する。
{{< /details >}}

## 階数

任意の行列 {{< katex >}}A{{< /katex >}} は行基本変形を繰り返すことによって階段行列にすることができる。

<!-- TODO 行基本変形について -->

行列 {{< katex >}}A{{< /katex >}} の階段行列の中の少なくとも1つは {{< katex >}}0{{< /katex >}} でない成分をもつ行の個数を行列 {{< katex >}}A{{< /katex >}} の**階数 (rank)** といい、以下 {{< katex >}}\text{rank}(A){{< /katex >}} で表す。

{{< katex >}}n{{< /katex >}} 元連立方程式の係数行列を {{< katex >}}A{{< /katex >}}、定数項ベクトルを {{< katex >}}\bold{b}{{< /katex >}}、係数行列と定数項ベクトルを連結した拡大係数行列を {{< katex >}}Ab{{< /katex >}} とおくと、以下の関係が成り立つ。

{{< katex display >}}
\begin{aligned}
\text{rank}(A)&=\text{rank}(A\bold{b})\land\begin{cases}
\text{rank}(A)=n&\iff\text{解は1つ}\\
\text{rank}(A)\lt n&\iff\text{解は不定であり、}n-\text{rank}(A)\,\text{個の任意定数で表せる}
\end{cases}\\
\text{rank}(A)&\ne\text{rank}(A\bold{b})\iff\text{解なし (不能)}
\end{aligned}
{{< /katex >}}

{{< hint info >}}
特に {{< katex >}}\bold{b}=\bold{0}{{< /katex >}} のとき、必ず {{< katex >}}\text{rank}(A)=\text{rank}(A\bold{b}){{< /katex >}} であるため、連立方程式は必ず解をもつ。
{{< /hint >}}

## 行列式

**行列式 (determinant)** とは正方行列に対して定義される量であり、以下行列 {{< katex >}}A{{< /katex >}} の行列式を {{< katex >}}|A|{{< /katex >}} で表す。

### 性質

- **転置不変性**

  {{< katex display >}}
  |A|=|A^t|
  {{< /katex >}}

- **交代性**

  行 or 列を入れ替えると、行列式の値は {{< katex >}}-1{{< /katex >}} 倍になる。

- **多重線形性**

  ある行 or 列の定数倍を他の行 or 列に加えても行列式の値は変化しない。

### 求め方: サラスの方法

サラスの方法は、2次あるいは3次正方行列において、左下から右下へ向かう方向に {{< katex >}}+{{< /katex >}}, 右上から左下に向う方向に {{< katex >}}-{{< /katex >}} の符号を付けて積をとり、それらの和をとることで行列式を求める。

**例**

2次正方行列 {{< katex >}}A=\left(\begin{matrix}
a_{11}&a_{12}\\
a_{21}&a_{22}
\end{matrix}\right){{< /katex >}} の行列式は

{{< katex display >}}
|A|=a_{11}a_{22}-a_{12}a_{21}
{{< /katex >}}

で計算できる。

3次正方行列 {{< katex >}}A=\left(\begin{matrix}
a_{11}&a_{12}&a_{13}\\
a_{21}&a_{22}&a_{23}\\
a_{31}&a_{32}&a_{33}
\end{matrix}\right){{< /katex >}} の行列式は

{{< katex display >}}
|A|=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}-a_{31}a_{22}a_{13}-a_{32}a_{23}a_{11}-a_{33}a_{21}a_{12}
{{< /katex >}}

で計算できる。

ただし、**4次以上の正方行列に対してサラスの方法は使えない。**

### 求め方: 余因子展開

行列 {{< katex >}}A{{< /katex >}} から {{< katex >}}i{{< /katex >}} 行 {{< katex >}}j{{< /katex >}} 列を取り除いた小行列式を {{< katex >}}M_{i,j}{{< /katex >}} と表すとき

{{< katex display >}}
\tilde{a}_{i,j}=(-1)^{i+j}|M_{i,j}|
{{< /katex >}}

を {{< katex >}}A{{< /katex >}} の**{{< katex >}}(i,j){{< /katex >}} 余因子 (cofactor)** といい、{{< katex >}}\tilde{a}_{i,j}{{< /katex >}} で表す。

行列 {{< katex >}}A{{< /katex >}} を {{< katex >}}n{{< /katex >}}次正方行列とすると、{{< katex >}}A{{< /katex >}} の行列式は次のように与えられる。

**第 {{< katex >}}i{{< /katex >}} 列に沿った余因子展開**

{{< katex display >}}
\begin{aligned}
|A|&=a_{i,1}(-1)^{i+1}|M_{i,1}|+a_{i,2}(-1)^{i+2}|M_{i,2}|+\cdots+a_{i,n}(-1)^{i+n}|M_{i,n}|\\
&=\sum_{j'=1}^n{a_{i,j'}(-1)^{i+j'}|M_{i,j'}|}\\
&=\sum_{j'=1}^n{a_{i,j'}\tilde{a}_{i,j'}}
\end{aligned}
{{< /katex >}}

**第 {{< katex >}}j{{< /katex >}} 行に沿った余因子展開**

{{< katex display >}}
\begin{aligned}
|A|&=a_{1,j}(-1)^{1+j}|M_{1,j}|+a_{2,j}(-1)^{2,j}|M_{2,j}|+\cdots+a_{n,j}(-1)^{n+j}|M_{n,j}|\\
&=\sum_{i'=1}^n{a_{i',j}(-1)^{i'+j}|M_{i'+j}|}\\
&=\sum_{i'=1}^n{a_{i',j}\tilde{a}_{i',j}}
\end{aligned}
{{< /katex >}}

### 例題

- {{< katex >}}\begin{vmatrix}1&0&2\\-1&-1&1\\2&1&2\end{vmatrix}{{< /katex >}} を第1行に沿って余因子展開せよ
- {{< katex >}}\begin{vmatrix}1&4&7\\2&5&8\\3&6&9\end{vmatrix}{{< /katex >}} を第1列に沿って余因子展開せよ
- {{< katex >}}\begin{vmatrix}-2&1&0&2\\1&0&-1&2\\-4&2&3&1\\2&0&1&-1\end{vmatrix}{{< /katex >}} を第2列に沿って余因子展開せよ

## 逆行列

正方行列 {{< katex >}}A{{< /katex >}} に対して {{< katex >}}AX=XA=E{{< /katex >}} となる正方行列 {{< katex >}}X{{< /katex >}} が存在するとき、行列 {{< katex >}}A{{< /katex >}} は「**正則である (regular)**」という。
このとき、{{< katex >}}X{{< /katex >}} を {{< katex >}}A{{< /katex >}} の**逆行列 (inverse matrix)** といい、以下 {{< katex >}}A^{-1}{{< /katex >}} で表す。

{{< katex >}}n{{< /katex >}}次正方行列 {{< katex >}}A{{< /katex >}} が正則であるとき、その逆行列 {{< katex >}}A^{-1}{{< /katex >}} は

{{< katex display >}}
A^{-1}=\frac1{|A|}\tilde{A}
{{< /katex >}}

と表せる。

ここで、{{< katex >}}\tilde{A}{{< /katex >}} を {{< katex >}}A{{< /katex >}} の**余因子行列 (cofactor matrix)**といい、以下のように定義される。

{{< katex display >}}
\tilde{A}=\left(\begin{array}{ccccc}
\tilde{a}_{11}&\tilde{a}_{12}&\cdots&\tilde{a}_{1n}\\
\tilde{a}_{21}&\tilde{a}_{22}&\cdots&\tilde{a}_{2n}\\
\vdots&\vdots&\ddots&\vdots\\
\tilde{a}_{n1}&\tilde{a}_{n2}&\cdots&\tilde{a}_{nn}\\
\end{array}\right)^t=\left(\begin{array}{ccccc}
\tilde{a}_{11}&\tilde{a}_{21}&\cdots&\tilde{a}_{n1}\\
\tilde{a}_{12}&\tilde{a}_{22}&\cdots&\tilde{a}_{n2}\\
\vdots&\vdots&\ddots&\vdots\\
\tilde{a}_{1n}&\tilde{a}_{2n}&\cdots&\tilde{a}_{nn}\\
\end{array}\right)
{{< /katex >}}

<!-- TODO 掃き出し法について書く -->

### 性質

{{< katex display >}}
n\text{次正方行列が正則}\iff\text{rank}(A)=n\iff|A|\ne0
{{< /katex >}}

### 例題

- {{< katex >}}A=\left(\begin{matrix}a&b\\c&d\end{matrix}\right){{< /katex >}} の逆行列を求めよ

## 固有ベクトルと固有値

ある {{< katex >}}n{{< /katex >}}次正方行列 {{< katex >}}A{{< /katex >}} に対し {{< katex >}}A\bold{x}=\lambda\bold{x}{{< /katex >}} を満たす {{< katex >}}n{{< /katex >}} 次元列ベクトル {{< katex >}}\bold{x}\;(\bold{x}\ne\bold{0}){{< /katex >}} が存在するとする。
このとき、{{< katex >}}\lambda{{< /katex >}} を {{< katex >}}A{{< /katex >}} の**固有値 (eigenvalue)** といい、{{< katex >}}\bold{x}{{< /katex >}} を {{< katex >}}\lambda{{< /katex >}} に対する**固有ベクトル (eigenvector)** という。

また、{{< katex >}}A{{< /katex >}} の相異なる固有ベクトル {{< katex >}}\lambda_1,\lambda_2,\dots,\lambda_k{{< /katex >}} は**一次独立**である。

{{< hint info >}}
**固有値と固有ベクトルの意味の考察**

{{< katex display >}}
A\bold{x}=\lambda\bold{x}
{{< /katex >}}

ベクトル {{< katex >}}\bold{x}{{< /katex >}} を行列 {{< katex >}}A{{< /katex >}} によって変換したときに、変換後のベクトル {{< katex >}}A\bold{x}{{< /katex >}} が変換前のベクトルのスカラー倍になる (変換前後でベクトルの向きが変わらない) とき、変換前のベクトルが固有ベクトル {{< katex >}}\bold{x}{{< /katex >}} でそのときの倍率が固有値 {{< katex >}}\lambda{{< /katex >}} となる。
{{< /hint >}}

{{< details title="A の相異なる固有値 λ_1, λ_2, ..., λ_k に対する固有ベクトル x_1, x_2, ..., x_k が一次独立であることの証明" >}}
{{< katex >}}k=1{{< /katex >}} のとき、成立は明らか。

{{< katex >}}k=m{{< /katex >}} のとき、成立を仮定する。

{{< katex >}}k=m+1{{< /katex >}} とき

{{< katex display >}}
c_1\bold{x_1}+c_2\bold{x_2}+\cdots+c_m\bold{x_m}+c_{m+1}\bold{x_{m+1}}=\bold{0}\tag{1}
{{< /katex >}}

について考える。

(1) の両辺に左から {{< katex >}}A{{< /katex >}} をかけると、{{< katex >}}A\bold{x}_i=\lambda_i\bold{x}_i{{< /katex >}} より

{{< katex display >}}
c_1\lambda_1\bold{x_1}+c_2\lambda_2\bold{x_2}+\cdots+c_m\lambda_m \bold{x_m}+c_{m+1}\lambda_{m+1}\bold{x_{m+1}}=\bold{0}\tag{2}
{{< /katex >}}

(1) の両辺に左から {{< katex >}}\lambda_{m+1}{{< /katex >}} をかけると

{{< katex display >}}
c_1\lambda_{m+1}\bold{x_1}+c_2\lambda_{m+1}\bold{x_2}+\cdots+c_m\lambda_{m+1} \bold{x_m}+c_{m+1}\lambda_{m+1}\bold{x_{m+1}}=\bold{0}\tag{3}
{{< /katex >}}

ここで {{< katex >}}\text{(2)}-\text{(3)}{{< /katex >}} を考えると

{{< katex display >}}
c_1(\lambda_1-\lambda_{m+1})\bold{x_1}+c_2(\lambda_2-\lambda_{m+1})\bold{x_2}+\cdots+c_m(\lambda_m-\lambda_{m+1})\bold{x_m}=\bold{0}
{{< /katex >}}

仮定より {{< katex >}}\bold{x_1},\bold{x_2},\dots,\bold{x_m}{{< /katex >}} は一次独立であるから

{{< katex display >}}
c_i(\lambda_i-\lambda_{m+1})=0\;(i=1,2,\dots,m)
{{< /katex >}}

ここで {{< katex >}}\lambda_i-\lambda_{m+1}\ne0\enspace(i=1,2,\dots,m){{< /katex >}} であるので

{{< katex display >}}
c_1=c_2=\cdots=c_m=0
{{< /katex >}}

これを (1) に代入すると

{{< katex display >}}
\begin{aligned}
c_{m+1}\bold{x_{m+1}}&=\bold{0}\\
\therefore c_{m+1}&=0
\end{aligned}
{{< /katex >}}

以上より {{< katex >}}\bold{x_1},\bold{x_2},\dots,\bold{x_{m+1}}{{< /katex >}} は一次独立。
{{< /details >}}

### 求め方

{{< katex display >}}
\begin{aligned}
A\bold{x}&=\lambda\bold{x}\\
(A-\lambda E)\bold{x}&=\bold{0}
\end{aligned}
{{< /katex >}}

ここで、上記の式が {{< katex >}}\bold{x}=\bold{0}{{< /katex >}} 以外の解をもつことから

{{< katex display >}}
\begin{aligned}
|A-\lambda E|=0
\end{aligned}
{{< /katex >}}

が導け、これを**固有方程式**という。
固有方程式は {{< katex >}}\lambda{{< /katex >}} についての {{< katex >}}n{{< /katex >}} 元連立方程式である。


### 例題

- {{< katex >}}A=\left(\begin{matrix}2&3\\4&1\end{matrix}\right){{< /katex >}} の固有値・固有ベクトルを求めよ
- {{< katex >}}A=\left(\begin{matrix}2&1&1\\1&2&1\\1&1&2\end{matrix}\right){{< /katex >}} の固有値・固有ベクトルを求めよ

## 対角化

{{< katex >}}n{{< /katex >}}次正方行列 {{< katex >}}A{{< /katex >}} に対し、適切な正則行列 {{< katex >}}P{{< /katex >}} が存在して

{{< katex display >}}
P^{-1}AP=\left(\begin{array}{cccc}
\lambda_1&0&\cdots&0\\
0&\lambda_2&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&\lambda_n
\end{array}\right)
{{< /katex >}}

のような対角行列にできる時、行列 {{< katex >}}A{{< /katex >}} は**対角化可能**であるといい、このときの行列 {{< katex >}}P{{< /katex >}} を**変換行列**という。

ここで {{< katex >}}\lambda_0,\lambda_1\,\cdots,\lambda_n{{< /katex >}} は行列 {{< katex >}}A{{< /katex >}} の固有値である。

{{< details title="行列 P が逆行列をもつことの証明" >}}
{{< katex display >}}
\begin{aligned}
(\bold{x_1},\bold{x_2},\cdots,\bold{x_n})\left(\begin{array}{c}
c_1\\
c_2\\
\vdots\\
c_n
\end{array}\right)=0
\end{aligned}
{{< /katex >}}

とする。

ここで {{< katex >}}\text{rank}(P)<n{{< /katex >}} とすると、 {{< katex >}}c_1=c_2=\cdots=c_n=0{{< /katex >}} という自明な解以外の解をもってしまうので、これは {{< katex >}}\bold{x_1},\bold{x_2},\cdots,\bold{x_n}{{< /katex >}} が一次独立であることに矛盾する。

よって {{< katex >}}\text{rank}(P)=n{{< /katex >}} であり、{{< katex >}}P{{< /katex >}} は正則である。(逆行列をもつ)
{{< /details >}}

{{< details title="P^(-1)AP が対角行列であることの証明" >}}
{{< katex display >}}
\begin{aligned}
P^{-1}AP&=P^{-1}A(\bold{x_1},\bold{x_2},\cdots,\bold{x_n})\\
&=P^{-1}(A\bold{x_1},A\bold{x_2},\cdots,A\bold{x_n})\\
&=P^{-1}(\lambda_1\bold{x_1},\lambda_2\bold{x_2},\cdots,\lambda_n\bold{x_n})\\
&=P^{-1}(\bold{x_1},\bold{x_2},\cdots,\bold{x_n})\left(\begin{array}{cccc}
\lambda_1&0&\cdots&0\\
0&\lambda_2&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&0&\lambda_n
\end{array}\right)\\
&=\left(\begin{array}{cccc}
\lambda_1&0&\cdots&0\\
0&\lambda_2&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&0&\lambda_n
\end{array}\right)
\end{aligned}
{{< /katex >}}
{{< /details >}}

### 定理

{{< katex >}}n{{< /katex >}}次正方行列 {{< katex >}}A{{< /katex >}} の {{< katex >}}n{{< /katex >}} 個の一次独立な固有ベクトルを {{< katex >}}\bold{x_1},\bold{x_2},\cdots,\bold{x_n}{{< /katex >}} とする。
それらを並べた行列 {{< katex >}}(\bold{x_1},\bold{x_2},\cdots,\bold{x_n}){{< /katex >}} を {{< katex >}}P{{< /katex >}} とすると、行列 {{< katex >}}A{{< /katex >}} は次のように対角化できる。

{{< katex display >}}
P^{-1}AP=\left(\begin{array}{cccc}
\lambda_1&0&\cdots&0\\
0&\lambda_2&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&\lambda_n
\end{array}\right)
{{< /katex >}}

### 対角化できない例

{{< katex display >}}
A=\left(\begin{matrix}
-3&-1\\
1&-1
\end{matrix}\right)\\
{{< /katex >}}

行列 {{< katex >}}A{{< /katex >}} の固有方程式を解くと

{{< katex display >}}
\begin{aligned}
\begin{vmatrix}
-3-\lambda&-1\\
1&-1-\lambda
\end{vmatrix}&=(-3-\lambda)(-1-\lambda)+1\\
&=\lambda^2+4\lambda+4\\
&=(\lambda+2)^2=0\\
\therefore\lambda&=-2\\
\left(\begin{matrix}
-1&-1\\
1&1
\end{matrix}\right)\left(\begin{matrix}
x\\
y
\end{matrix}\right)&=\left(\begin{matrix}
0\\
0
\end{matrix}\right)\iff{x+y=0}
\end{aligned}
{{< /katex >}}

ここで {{< katex >}}x=s{{< /katex >}} とおくと {{< katex >}}y=-s{{< /katex >}}

{{< katex display >}}
\therefore{\left(\begin{matrix}
x\\
y
\end{matrix}\right)=s\left(\begin{matrix}
1\\
-1
\end{matrix}\right)}
{{< /katex >}}

これ以外に独立な固有ベクトルがとれないので**対角化不可能**。

### 応用例: 対角化を使った A^n の計算

{{< katex display >}}
\begin{aligned}
(P^{-1}AP)^k&=(P^{-1}AP)(P^{-1}AP)\cdots(P^{-1}AP)\\
&=P^{-1}A^kP\\
A^k&=P(P^{-1}AP)^kP^{-1}\\
&=P\left(\begin{matrix}
\lambda_1^k&0&\cdots&0\\
0&\lambda_2^k&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&\lambda_n^k
\end{matrix}\right)P^{-1}
\end{aligned}
{{< /katex >}}

と求められる。

### 例題

- 行列 {{< katex >}}A=\left(\begin{matrix}-2&1\\5&2\end{matrix}\right){{< /katex >}} を変換行列 {{< katex >}}P{{< /katex >}} を用いて対角化せよ
- 行列 {{< katex >}}A=\left(\begin{matrix}-2&2&4\\-2&3&2\\-2&1&4\end{matrix}\right){{< /katex >}} を変換行列 {{< katex >}}P{{< /katex >}} を用いて対角化せよ

## 参考文献

- ヨビノリたくみ, [線形代数 - YouTube](https://youtube.com/playlist?list=PLDJfzGjtVLHnc1vTpBaCNKMUl6HauQv1a), 2019
- Wikipedia, [正則行列](https://ja.wikipedia.org/wiki/%E6%AD%A3%E5%89%87%E8%A1%8C%E5%88%97)
- Wikipedia, [余因子展開](https://ja.wikipedia.org/wiki/%E4%BD%99%E5%9B%A0%E5%AD%90%E5%B1%95%E9%96%8B)
