---
title: "線形代数"
date: 2021-04-08T03:07:05+09:00
---

## 階数

任意の行列 {{< katex >}}A{{< /katex >}} は行基本変形を繰り返すことによって階段行列にすることができる。
このとき、この階段行列の中の少なくとも 1 つは {{< katex >}}0{{< /katex >}} ではない成分をもつ行の個数を行列 {{< katex >}}A{{< /katex >}} の**階数**といい、 {{< katex >}}
\text{rank}(A)
{{< /katex >}} で表す。

{{< katex >}}n{{< /katex >}} 元連立方程式の係数行列を {{< katex >}}A{{< /katex >}}, 定数項ベクトルを {{< katex >}}b{{< /katex >}} とする。
ここで、拡大係数行列を {{< katex >}}Ab{{< /katex >}} で表すとする。

1. {{< katex >}}\text{rank}(A)=n{{< /katex >}} である場合
   連立一次方程式の**解は１つ**。
1. {{< katex >}}\text{rank}(A) \lt n{{< /katex >}} である場合
   連立一次方程式の**解は不定**であり、 {{< katex >}}n-\text{rank}(A){{< /katex >}} 個の任意定数で表せる。
1. {{< katex >}}\text{rank}(A)\ne\text{rank}(Ab){{< /katex >}}
   連立方程式の**解はなし** (**不能**)。

また、{{< katex >}}b=0{{< /katex >}} なら、連立一次方程式は必ず解をもつ。

## 固有ベクトルと固有値

ある {{< katex >}}n{{< /katex >}} 次正方行列 {{< katex >}}A{{< /katex >}} に対し

{{< katex display >}}
Ax=\lambda x
{{< /katex >}}

 を満たす {{< katex >}}n{{< /katex >}} 次元列ベクトル {{< katex >}}x (x\ne\text{\O}){{< /katex >}} が存在するとき、 {{< katex >}}\lambda{{< /katex >}} を {{< katex >}}A{{< /katex >}} の**固有値**といい、 {{< katex >}}x{{< /katex >}} を {{< katex >}}\lambda{{< /katex >}} に対する**固有ベクトル**という。

{{< katex display >}}
\left(\begin{array}{cc}
2&3\\
4&1
\end{array}\right)\left(\begin{array}{c}
1\\
1
\end{array}\right)=\left(\begin{array}{c}
5\\
5
\end{array}\right)=5\left(\begin{array}{c}
1\\
1
\end{array}\right)
{{< /katex >}}

### 求め方

{{< katex display >}}
\begin{aligned}
Ax&=\lambda x\\
(A-\lambda E)x&=\text{\O}
\end{aligned}
{{< /katex >}}

ここで、上記の式が {{< katex >}}x=\text{\O}{{< /katex >}} 以外の解をもつことから

{{< katex display >}}
\begin{aligned}
|A-\lambda E|=0
\end{aligned}
{{< /katex >}}

が成り立つ。
これを**固有方程式**という。
固有方程式は {{< katex >}}\lambda{{< /katex >}} の {{< katex >}}n{{< /katex >}} 次方程式である。

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
それらを並べた行列 {{< katex >}}(x_1,x_2,\cdots,x_n){{< /katex >}} を {{< katex >}}P{{< /katex >}} とすると、行列 {{< katex >}}A{{< /katex >}} は次のように対角化できる。

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

### 応用

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

## 参考文献

- ヨビノリたくみ, [線形代数 - YouTube](https://youtube.com/playlist?list=PLDJfzGjtVLHnc1vTpBaCNKMUl6HauQv1a), 2019