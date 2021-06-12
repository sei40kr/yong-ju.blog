---
title: "線形代数"
date: 2021-04-08T03:07:05+09:00
categories: ["数学"]
tags: ["勉強ノート", "大学数学"]
---

## 階数

任意の行列 {{< katex >}}A{{< /katex >}} は行基本変形を繰り返すことによって階段行列にすることができる。
このとき、この階段行列の中の少なくとも1つは {{< katex >}}0{{< /katex >}} ではない成分をもつ行の個数を行列 {{< katex >}}A{{< /katex >}} の**階数**といい

{{< katex display >}}
\text{rank}(A)
{{< /katex >}}

で表す。

{{< katex >}}n{{< /katex >}} 元連立方程式の係数行列を {{< katex >}}A{{< /katex >}}, 定数項ベクトルを {{< katex >}}b{{< /katex >}} とする。
ここで、拡大係数行列を {{< katex >}}Ab{{< /katex >}} で表すとする。

- {{< katex >}}\text{rank}(A)=\text{rank}(Ab){{< /katex >}}
    - {{< katex >}}\text{rank}(A)=n{{< /katex >}} →
      連立一次方程式の**解は1つ**
    - {{< katex >}}\text{rank}(A)\lt n{{< /katex >}} →
      連立一次方程式の**解は不定**であり、{{< katex >}}n-\text{rank}(A){{< /katex >}} 個の任意定数で表せる
- {{< katex >}}\text{rank}(A)\ne\text{rank}(Ab){{< /katex >}} → 連立方程式の**解はなし** (**不能**)

また、{{< katex >}}b=0{{< /katex >}} なら、連立一次方程式は必ず解をもつ。

## 行列式

行列式とは、正方行列に対して定義される量であり、行列 {{< katex >}}A{{< /katex >}} の行列式を

{{< katex display >}}
|A|,\det{A}
{{< /katex >}}

で表す。

### 性質

- **転置不変性** ({{< katex >}}|A|=|A^t|{{< /katex >}})
- **交代性** (行 or 列を入れ替えると、行列式の値は {{< katex >}}-1{{< /katex >}} 倍になる)
- **多重線形性** (ある行 or 列の定数倍を他の行 or 列に加えても行列式の値は変化しない)

### 求め方

#### サラスの方法

サラスの方法は、2次あるいは3次正方行列において、左下から右下へ向かう方向に +, 右上から左下に向う方向に - の符号を付けて積をとり、それらの和をとることで行列式を求める。

2次正方行列 {{< katex >}}A=\left(\begin{matrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{matrix}\right){{< /katex >}} の行列式は

{{< katex display >}}
|A|=a_{11}a_{22}-a_{12}a_{21}
{{< /katex >}}

で計算できる。

3次正方行列 {{< katex >}}A=\left(\begin{matrix}a_{11}&a_{12}&a_{13}\\a_{21}&a_{22}&a_{23}\\a_{31}&a_{32}&a_{33}\end{matrix}\right){{< /katex >}} の行列式は

{{< katex display >}}
|A|=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}-a_{31}a_{22}a_{13}-a_{32}a_{23}a_{11}-a_{33}a_{21}a_{12}
{{< /katex >}}

で計算できる。

**4次以上の正方行列に対してサラスの方法は使えない。**

#### 余因子展開

行列 {{< katex >}}A{{< /katex >}} から {{< katex >}}i{{< /katex >}} 行 {{< katex >}}j{{< /katex >}} 列を取り除いた小行列式を {{< katex >}}M_{i,j}{{< /katex >}} と表すとき

{{< katex >}}
(-1)^{i+j}M_{i,j}
{{< /katex >}}

を {{< katex >}}A{{< /katex >}} の {{< katex >}}(i,j){{< /katex >}} 余因子といい、{{< katex >}}\tilde{a}_{i,j}{{< /katex >}} で表す。

行列 {{< katex >}}A{{< /katex >}} を {{< katex >}}n{{< /katex >}} 次正方行列とすると、{{< katex >}}A{{< /katex >}} の行列式は次のように与えられる。

第 {{< katex >}}i{{< /katex >}} 列に沿った余因子展開
: {{< katex display >}}
\begin{aligned}
|A|&=a_{i,1}(-1)^{i+1}|M_{i,1}|+a_{i,2}(-1)^{i+2}|M_{i,2}|+\cdots+a_{i,n}(-1)^{i+n}|M_{i,n}|\\
&=\sum_{j'=1}^n{a_{i,j'}(-1)^{i+j'}|M_{i,j'}|}\\
&=\sum_{j'=1}^n{a_{i,j'}\tilde{a}_{i,j'}}
\end{aligned}
{{< /katex >}}

第 {{< katex >}}j{{< /katex >}} 行に沿った余因子展開
: {{< katex display >}}
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

### 定義

正方行列 {{< katex >}}A{{< /katex >}} に対して

{{< katex display >}}
AX=XA=E
{{< /katex >}}

となる正方行列 {{< katex >}}X{{< /katex >}} が存在するとき、**{{< katex >}}A{{< /katex >}} は正則である**といい、{{< katex >}}X{{< /katex >}} を {{< katex >}}A{{< /katex >}} の**逆行列**といい、一般には {{< katex >}}A^{-1}{{< /katex >}} で表す。

また、{{< katex >}}n{{< /katex >}} 次正方行列 {{< katex >}}A{{< /katex >}} が正則であるとき、その逆行列  {{< katex >}}A^{-1}{{< /katex >}} は

{{< katex display >}}
A^{-1}=\frac1{|A|}\tilde{A}
{{< /katex >}}

と表せる。

<!-- TODO 余因子行列について書く -->

<!-- TODO 掃き出し法について書く -->

### 性質

{{< katex >}}n{{< /katex >}} 次正方行列が正則{{< katex >}}\iff\text{rank}(A)=n\iff|A|\ne0{{< /katex >}}

### 例題

- {{< katex >}}A=\left(\begin{matrix}a&b\\c&d\end{matrix}\right){{< /katex >}} の逆行列を求めよ

## 固有ベクトルと固有値

ある {{< katex >}}n{{< /katex >}} 次正方行列 {{< katex >}}A{{< /katex >}} に対し

{{< katex display >}}
Ax=\lambda x
{{< /katex >}}

を満たす  {{< katex >}}n{{< /katex >}} 次元列ベクトル {{< katex >}}x (x\ne\empty){{< /katex >}} が存在するとする。
このとき、{{< katex >}}\lambda{{< /katex >}} を {{< katex >}}A{{< /katex >}} の**固有値**といい、{{< katex >}}x{{< /katex >}} を {{< katex >}}\lambda{{< /katex >}} に対する**固有ベクトル**という。

### 求め方

{{< katex display >}}
\begin{aligned}
Ax&=\lambda x\\
(A-\lambda E)x&=\empty
\end{aligned}
{{< /katex >}}

ここで、上記の式が  {{< katex >}}x=\empty{{< /katex >}} 以外の解をもつことから

{{< katex display >}}
\begin{aligned}
|A-\lambda E|=0
\end{aligned}
{{< /katex >}}

が成り立つ。
これを**固有方程式**という。
固有方程式は {{< katex >}}\lambda{{< /katex >}} の {{< katex >}}n{{< /katex >}} 次方程式である。

### 例題

- {{< katex >}}A=\left(\begin{matrix}2&3\\4&1\end{matrix}\right){{< /katex >}} の固有値・固有ベクトルを求めよ
- {{< katex >}}A=\left(\begin{matrix}2&1&1\\1&2&1\\1&1&2\end{matrix}\right){{< /katex >}} の固有値・固有ベクトルを求めよ

## 対角化

{{< katex >}}n{{< /katex >}} 次正方行列 {{< katex >}}A{{< /katex >}} に対し、適切な正則行列 {{< katex >}}P{{< /katex >}} が存在して

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

### 定理

{{< katex >}}n{{< /katex >}} 次正方行列 {{< katex >}}A{{< /katex >}} の {{< katex >}}n{{< /katex >}} 個の一次独立な固有ベクトルを {{< katex >}}x_1,x_2,\cdots,x_n{{< /katex >}} とする。
それらを並べた行列 {{< katex >}}(x_1,x_2,\cdots,x_n){{< /katex >}} を {{< katex >}}P{{< /katex >}} とすると、行列 {{< katex >}}A{{< /katex >}} は次のように対角化できる。

{{< katex display >}}
P^{-1}AP=\left(\begin{array}{cccc}
\lambda_1&0&\cdots&0\\
0&\lambda_2&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&\lambda_n
\end{array}\right)
{{< /katex >}}

### 証明

#### 行列 {{< katex >}}P{{< /katex >}} が逆行列をもつことの証明

{{< katex display >}}
\begin{aligned}
(x_1,x_2,\cdots,x_n)\left(\begin{array}{c}
c_1\\
c_2\\
\vdots\\
c_n
\end{array}\right)=0
\end{aligned}
{{< /katex >}}

とする。
ここで {{< katex >}}\text{rank}(P)<0{{< /katex >}} とすると、 {{< katex >}}C_1=C_2=\cdots=C_n=0{{< /katex >}} という自明な解以外の解をもってしまうので、これは {{< katex >}}x_1,x_2,\cdots,x_n{{< /katex >}} が一次独立であることに矛盾する。

よって {{< katex >}}\text{rank}(P)=n{{< /katex >}} であり、{{< katex >}}P{{< /katex >}} は正則である。 (逆行列をもつ)

#### {{< katex >}}P^{-1}AP{{< /katex >}} が対角行列であることの証明

{{< katex display >}}
\begin{aligned}
P^{-1}AP&=P^{-1}A(x_1,x_2,\cdots,x_n)\\
&=P^{-1}(Ax_1,Ax_2,\cdots,Ax_n)\\
&=P^{-1}(\lambda_1x_1,\lambda_2x_2,\cdots,\lambda_nx_n)\\
&=P^{-1}(x_1,x_2,\cdots,x_n)\left(\begin{array}{cccc}
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

#### {{< katex >}}A{{< /katex >}} の相異なる固有値 {{< katex >}}\vec{x_1},\vec{x_2},\dots,\vec{x_k}{{< /katex >}} に対する固有ベクトル {{< katex >}}\lambda_1,\lambda_2,\dots,\lambda_k{{< /katex >}} が一次独立であることの証明

- {{< katex >}}k=1{{< /katex >}} のとき、成立は明らか
- {{< katex >}}k=m{{< /katex >}} のとき、成立を仮定する

このとき

{{< katex display >}}
c_1\vec{x_1}+c_2\vec{x_2}+\cdots+c_m\vec{x_m}+c_{m+1}\vec{x_{m+1}}=\vec{0}\tag{*}
{{< /katex >}}

について考える。

{{< katex >}}(\text{*}){{< /katex >}} の両辺に左から {{< katex >}}A{{< /katex >}} をかけると、{{< katex >}}Ax_i=\lambda_ix_i{{< /katex >}} より

{{< katex display >}}
c_1\lambda_1\vec{x_1}+c_2\lambda_2\vec{x_2}+\cdots+c_m\lambda_m \vec{x_m}+c_{m+1}\lambda_{m+1}\vec{x_{m+1}}=\vec{0}\tag{a}
{{< /katex >}}

{{< katex >}}(\text{*}){{< /katex >}} の両辺に左から {{< katex >}}\lambda_{m+1}{{< /katex >}} をかけると

{{< katex display >}}
c_1\lambda_{m+1}\vec{x_1}+c_2\lambda_{m+1}\vec{x_2}+\cdots+c_m\lambda_{m+1} \vec{x_m}+c_{m+1}\lambda_{m+1}\vec{x_{m+1}}=\vec{0}\tag{b}
{{< /katex >}}

ここで {{< katex >}}(\text{a})-(\text{b}){{< /katex >}} を考えると

{{< katex display >}}
c_1(\lambda_1-\lambda_{m+1})\vec{x_1}+c_2(\lambda_2-\lambda_{m+1})\vec{x_2}+\cdots+c_m(\lambda_m-\lambda_{m+1})\vec{x_m}=\vec{0}
{{< /katex >}}

ここで {{< katex >}}\vec{x_1},\vec{x_2},\dots,\vec{x_m}{{< /katex >}} は一次独立であるから

{{< katex display >}}
c_i(\lambda_i-\lambda_{m+1})=\vec{0}~(i=1,2,\dots,m)
{{< /katex >}}

{{< katex >}}\lambda_i-\lambda_{m+1}\ne0~(i=1,2,\dots,m){{< /katex >}} であるので

{{< katex display>}}
c_1=c_2=\cdots=c_m=0
{{< /katex >}}

これを {{< katex >}}(*){{< /katex >}} に代入すると

{{< katex display >}}
\begin{aligned}
c_{m+1}\vec{x_{m+1}}&=\vec{0}\\
\therefore c_{m+1}&=0
\end{aligned}
{{< /katex >}}

以上より {{< katex >}}x_1,x_2,\dots,x_{m+1}{{< /katex >}} は一次独立。

### 対角化できない例

{{< katex display >}}
\begin{aligned}
A&=\left(\begin{matrix}
-3&-1\\
1&-1
\end{matrix}\right)\\[9mu]
\begin{vmatrix}
-3-\lambda&-1\\
1&-1-\lambda
\end{vmatrix}&=(-3-\lambda)(-1-\lambda)+1\\
&=\lambda^2+4\lambda+4\\
&=(\lambda+2)^2\\
&=0\\
\therefore\lambda&=-2\\[9mu]
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

ここで {{< katex >}}x=s_1{{< /katex >}} とおくと {{< katex >}}y=-s_1{{< /katex >}}

{{< katex display >}}
\therefore{x_1=s_1\left(\begin{matrix}
1\\
-1
\end{matrix}\right)}
{{< /katex >}}

これ以外に独立な固有ベクトルがとれないので**対角化不可能**。

### 応用例

#### 対角化を使った {{< katex >}}A^n{{< /katex >}} の計算

{{< katex display >}}
(P^{-1}AP)^n=(P^{-1}AP)(P^{-1}AP)\cdots(P^{-1}AP)
{{< /katex >}}

ここで {{< katex >}}PP^{-1}=E{{< /katex >}} なので

{{< katex display >}}
\begin{aligned}
(P^{-1}AP)^n&=P^{-1}A^nP\\
A^n&=P(P^{-1}AP)^nP^{-1}
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
