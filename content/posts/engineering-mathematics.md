---
title: "工業数学"
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

と表される。

## テイラー展開

{{< katex display >}}
f(x)=f(a)+f{'}(a)(x-a)+\frac{1}{2!}f{''}(x)(x-a)^2+\frac{1}{3!}f{'''}(a)(x-a)^3+\cdots
{{< /katex >}}

{{< katex >}}a=0{{< /katex >}} のときのテイラー展開を **マクローリン展開** という。

テイラー展開をすることによって、複雑な関数を多項式で表せる。

## フーリエ変換

### フーリエ級数

横軸を {{< katex >}}t{{< /katex >}} として、同じような波形が繰り返して現れる関数 {{< katex >}}f(t){{< /katex >}} は、三角関数の無限級数に分解することができる → **フーリエ級数**

{{< katex display >}}
f(t)=a_0+\sum_{n=1}^\infty{a_n\cos{n\omega t}}+\sum_{n=1}^\infty{b_n\sin{n\omega t}}
{{< /katex >}}

フーリエ級数の式の {{< katex >}}a_0,a_n,b_n{{< /katex >}} は、それぞれフーリエ係数と呼ばれ、次式のように計算される。

{{< katex display >}}
a_0=\frac{1}{T}\int_{-\frac{T}2}^{+\frac{T}2}f(t)dt\newline
a_n=\frac{2}T\int_{-\frac{T}2}^{+\frac{T}2}f(t)\cos{n\omega t}dt\newline
b_n=\frac{2}T\int_{-\frac{T}2}^{+\frac{T}2}f(t)\sin{n\omega t}dt
{{< /katex >}}

また、角速度 {{< katex >}}\omega{{< /katex >}} は、波形の周期を {{< katex >}}T{{< /katex >}} とすると

{{< katex display >}}
\omega=\frac{2\pi}{T}
{{< /katex >}}

となる。

* {{< katex >}}f(-x)=f(x){{< /katex >}} が成り立つとき、 {{< katex >}}f(x){{< /katex >}} を **偶関数** といい、{{< katex >}}b_n=0{{< /katex >}} となる。
* {{< katex >}}f(-x)=-f(x){{< /katex >}} が成り立つとき、 {{< katex >}}f(x){{< /katex >}} を **奇関数** といい、{{< katex >}}a_0=a_n=0{{< /katex >}} となる。

## 参考文献

- 井上 満, 工業数学がわかる, 技術評論社, 2010
- ヨビノリたくみ, [【大学数学】テイラー展開の気持ち【解析学】 - YouTube](https://www.youtube.com/watch?v=qzd5iXKHkiU), 2017
