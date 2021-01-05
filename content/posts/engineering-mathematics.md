---
title: "工業数学"
date: 2021-01-05T04:53:19+09:00
tags: ["勉強ノート", "数学"]
---

## 前提知識

* 微分
* 積分
* 複素数

## 微分方程式

### 変数分離形

$$\frac{dy}{dx}=f(x)g(x)$$

1. $x$ に関する部分を左辺に、 $y$ に関する部分を右辺に分離する

   $$\frac{1}{g(y)}dy=f(x)dx$$

1. 両辺を積分する

   $$\int{\frac{1}{g(y)}}dy=\int{f(x)}dx$$

### 同次形

$$\frac{dy}{dx}=g(\frac{y}{x})$$

1. $\frac{y}{x}=u$ として方程式を書き直す。

   $u$ は $x$ の関数なので、 $y=ux$ より

   $$\frac{dy}{dx}=x\frac{du}{dx}+u$$

   となるので最初の式は

   $$x\frac{du}{dx}+u=g(u)$$

   となる。

1. 後は変数分離形として解くことができる。

   $$x\frac{1}{dx}=\frac{g(u)-u}{du}$$
   $$\frac{1}{g(u)-u}du=\frac{1}{x}dx$$

   両辺を積分して

   $$\int{\frac{1}{g(u)-u}}du=\int{\frac{1}{x}dx}=log|x|+C$$

### 一階線形微分方程式

$$y'+f(x)y=g(x)$$

$g(x)=0$ のとき

$$y'+f(x)y=0$$

という形になり、同次方程式になる。

1. 一回線形微分方程式の一般解の公式を当てはめて解く。

   $$h(x)=e^{\int{f(x)dx}}$$
   $$y=\frac{1}{h(x)}\\{\int{g(x)h(x)}dx+C\\}$$

## フーリエ変換

### フーリエ級数

横軸を $t$ として、同じような波形が繰り返して現れる関数 $f(t)$ は、三角関数の無限級数に分解することができる → **フーリエ級数**

$$f(t)=a_0+\sum_{n=1}^\infty{a_n\cos{n\omega t}}+\sum_{n=1}^\infty{b_n\sin{n\omega t}}$$

フーリエ級数の式の $a_0$, $a_n$, $b_n$ は、それぞれフーリエ係数と呼ばれ、次式のように計算される。

$$
a_0=\frac{1}{T}\int_{-\frac{T}2}^{+\frac{T}2}f(t)dt\newline
a_n=\frac{2}T\int_{-\frac{T}2}^{+\frac{T}2}f(t)\cos{n\omega t}dt\newline
b_n=\frac{2}T\int_{-\frac{T}2}^{+\frac{T}2}f(t)\sin{n\omega t}dt
$$

また、角速度 $\omega$ は、波形の周期を $T$ とすると

$$\omega=\frac{2\pi}{T}$$

となる。

* $f(-x)=f(x)$ が成り立つとき、 $f(x)$ を **偶関数** といい、$b_n=0$ となる。
* $f(-x)=-f(x)$ が成り立つとき、 $f(x)$ を **奇関数** といい、$a_0=a_n=0$ となる。
