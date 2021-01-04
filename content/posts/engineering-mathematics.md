---
title: "工業数学"
date: 2021-01-05T04:53:19+09:00
tags: ["勉強ノート", "数学"]
---

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
