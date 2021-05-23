---
title: "解析学"
date: 2021-01-05T04:53:19+09:00
tags: ["勉強ノート", "数学"]
---

## 前提知識

* 微分
* 積分
* 複素数

## オイラーの公式

{{< katex display >}}
e^{iy}=\cos{y}+i\sin{y}
{{< /katex >}}

この関係式を **オイラーの公式** という。この公式を用いれば、複素数の極座標表示は

{{< katex display >}}
z=r(\cos{\theta}+i\sin{\theta})=re^{i\theta}
{{< /katex >}}

と表せる。

## テイラー展開

{{< katex display >}}
\begin{aligned}
f(x)&=f(a)+f{'}(a)(x-a)+\frac{1}{2!}f{''}(x)(x-a)^2+\frac{1}{3!}f{'''}(a)(x-a)^3+\dots\\
&=\sum_{n=0}^\infty{\frac1{n!}f^{(n)}(a)(x-a)^n}
\end{aligned}
{{< /katex >}}

{{< katex >}}a=0{{< /katex >}} のときのテイラー展開を **マクローリン展開** という。

テイラー展開をすることによって、複雑な関数を基本的な関数系で表せる。

## フーリエ解析

### フーリエ級数展開

ある関数 {{< katex >}}f(x){{< /katex >}} の性質が知りたい場合、より基本的な関数系 {{< katex >}}\{\varphi_0(x),\varphi_1(x),\varphi_2(x),\dots\}{{< /katex >}} で級数展開する。

{{< katex display >}}
f(x)=\sum_{n=0}^\infty{c_n\varphi_n(x)}
{{< /katex >}}

1. {{< katex >}}f(x){{< /katex >}} が無限回微分可能な場合
   → {{< katex >}}\{1,x,x^2,x^3,\dots\}{{< /katex >}} で級数展開 (**マクローリン展開**)

   {{< katex display >}}
f(x)=\sum_{n=0}^\infty\frac{f^{(n)}(0)}{n!}x^n
   {{< /katex >}}
1. {{< katex >}}f(x){{< /katex >}} が周期関数である場合
   → {{< katex >}}\{1,\cos{x},\sin{x},\cos{2x},\sin{2x},\dots\}{{< /katex >}} (三角関数系) で級数展開 (**フーリエ級数展開**)

   {{< katex display >}}
f(x)=a+\sum_{n=1}^\infty(a_n\cos{nx}+b_n\sin{nx})
   {{< /katex >}}
   
級数展開に三角関数を使う利点は、**直交性** (自身以外との内積が 0) であること。

{{< hint info >}}
**関数の内積**

{{< katex >}}f(x),g(x){{< /katex >}} を周期 {{< katex >}}2\pi{{< /katex >}} の周期関数とすると、その内積は

{{< katex display >}}
\int_{-\pi}^\pi{f(x)g(x)dx}
{{< /katex >}}

で定義される。
{{< /hint >}}

{{< details title="三角関数系が直交性をもつことの証明">}}
{{< katex display >}}
\begin{aligned}
&\int_{-\pi}^\pi{\sin{mx}\cdot\sin{nx}}\\
=&\int_{-\pi}^\pi\frac{\cos(m-n)x-\cos(m+n)x}2dx\\
=&\begin{cases}
0&(m\ne n)\\
\pi&(m=n)
\end{cases}\\
\end{aligned}
{{< /katex >}}

同様に

{{< katex display >}}
\begin{aligned}
\int_{-\pi}^\pi{\cos{mx}\cdot\cos{nx}}&=\begin{cases}
0\,(m\ne n)\\
\pi\,(m=n)
\end{cases}\\
\int_{-\pi}^\pi{\cos{mx}\cdot\sin{nx}}&=0
\end{aligned}
{{< /katex >}}

また、三角関数と {{< katex >}}1{{< /katex >}} との直交性は自明である。
{{< /details >}}


### フーリエ係数

{{< katex display >}}
\begin{aligned}
\frac{a_0}2+\sum_{n=1}^\infty(a_n\cos{nx}+b_n\sin{nx})\\
a_n=\frac1\pi\int_{-\pi}^\pi{f(x)\cos{nx}dx}\\
b_n=\frac1\pi\int_{-\pi}^\pi{f(x)\sin{nx}dx}
\end{aligned}
{{< /katex >}}

このような形で表される級数を {{< katex >}}f(x){{< /katex >}} の**フーリエ級数**といい、{{< katex >}}a_n,b_n{{< /katex >}} を**フーリエ係数**という。

{{< details title="フーリエ係数の導出">}}
{{< katex display >}}
f(x)=a+\sum_{n=1}^\infty(a_n\cos{nx}+b_n\sin{nx})\tag1
{{< /katex >}}

(1) の両辺に {{< katex >}}\cos{mx}{{< /katex >}} をかけて、{{< katex >}}[-\pi,\pi]{{< /katex >}} で積分する。

{{< katex display >}}
\begin{aligned}
\int_{-\pi}^\pi{f(x)\cos{mx}dx}&=\int_{-\pi}^\pi{a\cos{mx}d x}+\sum_{n=1}^\infty\int_{-\pi}^\pi{(a_n\cos{nx}\cos{mx}+b_n\sin{nx}\cos{mx})dx}\\
&=\pi a_m\\
a_m&=\frac1\pi\int_{-\pi}^\pi{f(x)\cos{mx}dx}
\end{aligned}
{{< /katex >}}

同様に、(1) の両辺に {{< katex >}}\sin{mx}{{< /katex >}} をかけて、{{< katex >}}[-\pi,\pi]{{< /katex >}} で積分する。

{{< katex display >}}
\begin{aligned}
\int_{-\pi}^\pi{f(x)\sin{mx}dx}&=\int_{-\pi}^\pi{a\sin{mx}d x}+\sum_{n=1}^\infty\int_{-\pi}^\pi{(a_n\cos{nx}\sin{mx}+b_n\sin{nx}\sin{mx})dx}\\
&=\pi b_m\\
b_m&=\frac1\pi\int_{-\pi}^\pi{f(x)\sin{mx}dx}
\end{aligned}
{{< /katex >}}

同様に、(1) の両辺を積分すると

{{< katex display >}}
\begin{aligned}
\int_{-\pi}^\pi{f(x)dx}&=\int_{-\pi}^\pi{ad x}+\sum_{n=1}^\infty\int_{-\pi}^\pi{(a_n\cos{nx}+b_n\sin{nx})dx}\\
&=2\pi a\\
a&=\frac1{2\pi}\int_{-\pi}^\pi{f(x)dx}
\end{aligned}
{{< /katex >}}

よって

{{< katex display >}}
\begin{aligned}
a_n&=\frac1\pi\int_{-\pi}^\pi{f(x)\cos{nx}dx}\\
b_n&=\frac1\pi\int_{-\pi}^\pi{f(x)\sin{nx}dx}\\
a&=\frac1{2\pi}\int_{-\pi}^\pi{f(x)dx}=\frac{a_0}2
\end{aligned}
{{< /katex >}}
{{< /details >}}

### 複素フーリエ級数
{{< katex display >}}
\sum_{n=-\infty}^\infty{c_ne^{inx}}\\
c_n=\frac1{2\pi}\int_{-\pi}^\pi{f(x)e^{-inx}dx}
{{< /katex >}}

{{< hint info >}}
**{{< katex >}}c_n{{< /katex >}} の性質**

{{< katex >}}f(x){{< /katex >}} が実関数であるとき、{{< katex >}}c_{-n}=c_n^*{{< /katex >}} が成り立つ。
{{< /hint >}}

{{< details title="複素フーリエ級数の導出" >}}
{{< katex display >}}
\begin{aligned}
\begin{cases}
e^{inx}&=\cos{nx}+i\sin{nx}\\
e^{-inx}&=\cos{nx}-i\sin{nx}
\end{cases}
\end{aligned}
{{< /katex >}}

より

{{< katex display >}}
\begin{aligned}
\cos{nx}&=\frac{e^{inx}+e^{-inx}}2\\
\sin{nx}&=\frac{e^{inx}+-^{-inx}}{2i}
\end{aligned}
{{< /katex >}}

{{< katex display >}}
\begin{aligned}
&\frac{a_0}2+\sum_{n=1}^\infty(a_n\cos{nx}+b_n\sin{nx})\\
=&\frac{a_0}2+\sum_{n=1}^\infty(\frac{a_n-ib_n}2e^{inx}+\frac{a_n+ib_n}2e^{-inx})\\
=&\sum_{n=-\infty}^\infty{c_ne^{inx}}
\end{aligned}
{{< /katex >}}
{{< /details >}}

## 参考文献

- 井上 満, 工業数学がわかる, 技術評論社, 2010
- ヨビノリたくみ, [【大学数学】テイラー展開の気持ち【解析学】 - YouTube](https://www.youtube.com/watch?v=qzd5iXKHkiU), 2017
- ヨビノリたくみ, [【大学数学】フーリエ解析入門①(フーリエ級数展開 I)/全 5 講【解析学】](https://www.youtube.com/watch?v=HNHb0_mOTYw), 2017
- ヨビノリたくみ, [【大学数学】フーリエ解析入門②(フーリエ級数展開 II)/全 5 講【解析学】](https://www.youtube.com/watch?v=8F2B7wcGHHA), 2017
