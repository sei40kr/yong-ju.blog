---
title: "微分方程式"
date: 2021-04-04T16:59:44+09:00
categories: ["数学"]
tags: ["勉強ノート", "大学数学"]
---

## 変数分離形

### 定義

{{< katex display >}}
y'=f(x)g(y)
{{< /katex >}}

### 解法

{{< katex display >}}
\frac{dy}{dx}=f(x)g(y)
{{< /katex >}}

{{< katex >}}g(y)\ne0{{< /katex >}} のとき

{{< katex display >}}
\begin{aligned}
\frac{1}{g(y)}\frac{dy}{dx}&=f(x)\\
\int{\frac{1}{g(y)}\frac{dy}{dx}dx}&=\int{f(x)dx}\\
\int{\frac{1}{g(y)}dy}&=\int{f(x)dx}
\end{aligned}
{{< /katex >}}

<!-- TODO 置換積分の注釈 -->

### 例題

1. {{< katex >}}y'=2xy,y(0)=1{{< /katex >}}
1. {{< katex >}}y'=1-y^2{{< /katex >}}

## 同次形

### 定義

{{< katex display >}}
y'=f(\frac{y}{x})
{{< /katex >}}

### 解法

{{< katex >}}u=\dfrac{y}{x}{{< /katex >}} とおく。このとき
{{< katex >}}y=ux{{< /katex >}} であるので
{{< katex >}}y'=u'x+u{{< /katex >}} を代入して

{{< katex display >}}
\begin{aligned}
u'x+u&=f(u)\\
\frac{du}{dx}&=\frac{1}{x}\{f(u)-u\}
\end{aligned}
{{< /katex >}}

となり、変数分離形と同じように解ける。

### 例題

1. {{< katex >}}y'=\dfrac{y^2}{x^2+xy}{{< /katex >}}
1. {{< katex >}}y'=\dfrac{y}x+\cos^2\dfrac{y}x,y(1)=\dfrac\pi4{{< /katex >}}

## 一階線形微分方程式

### 定義

{{< katex display >}}
y'+p(x)y=q(x)
{{< /katex >}}

{{< katex >}}q(x)=0{{< /katex >}} の場合、上式を**同次方程式**といい、変数分離形と同じように解ける。
{{< katex >}}q(x)\ne0{{< /katex >}} の場合、上式を**非同次方程式**という。

### 解法

#### 特殊解 {{< katex >}}\alpha(x){{< /katex >}} が分かっている場合

{{< katex display >}}
\begin{cases}
\begin{aligned}
y'+p(x)y&=q(x)\\
\alpha'+p(x)\alpha&=q(x)
\end{aligned}
\end{cases}
{{< /katex >}}

より

{{< katex display >}}
(y-\alpha)'+p(x)(y-\alpha)=0
{{< /katex >}}

{{< katex >}}Y=y-\alpha{{< /katex >}} とおくと

{{< katex display >}}
Y'+p(x)Y=0
{{< /katex >}}

これは同次方程式となり、変数分離形と同じように解ける。

#### 定数変化法

同次方程式 {{< katex >}}y'+p(x)y=0{{< /katex >}} を解く。

{{< katex display >}}
\begin{aligned}
y'+p(x)y&=0\\
y&=C_1e^{-\int{p(x)dx}}
\end{aligned}
{{< /katex >}}

ここで、 定数 {{< katex >}}C_1{{< /katex >}} を関数 {{< katex >}}C_1(x){{< /katex >}} に変化させ {{< katex >}}y{{< /katex >}} を代入する。

{{< katex display >}}
\begin{aligned}
(C_1(x)e^{-\int{p(x)dx}})'+p(x)C_1(x)e^{-\int{p(x)dx}}&=q(x)\\
C_1'(x)e^{-\int{p(x)dx}}-p(x)C_1(x)e^{-\int{p(x)dx}}+p(x)C_1(x)e^{-\int{p(x)dx}}&=q(x)\\
C_1'(x)e^{-\int{p(x)dx}}&=q(x)\\
C_1'(x)&=q(x)e^{\int{p(x)dx}}+C_2\\
C_1(x)&=\int{q(x)e^{\int{p(x)dx}}+C_2}
\end{aligned}
{{< /katex >}}

よって

{{< katex display >}}
y=\{\int{q(x)e^{\int{p(x)dx}}}+C_2\}e^{-\int{p(x)dx}}
{{< /katex >}}

ここで {{< katex >}}h(x)=e^{\int{p(x)dx}}{{< /katex >}} とおくと

{{< katex display >}}
y=\frac{1}{h(x)}\{\int{q(x)h(x)dx}+C_2\}
{{< /katex >}}

#### 積分因子

{{< katex display >}}
y'+p(x)y=q(x)
{{< /katex >}}

の両辺に積分因子 {{< katex >}}e^{\int{p(x)dx}}{{< /katex >}} をかけて

{{< katex display >}}
\begin{aligned}
e^{\int{p(x)dx}}y'+e^{\int{p(x)dx}}p(x)y&=e^{\int{p(x)dx}}q(x)\\
\{e^{\int{p(x)dx}}y\}'&=e^{\int{p(x)dx}}q(x)\\
e^{\int{p(x)dx}}y&=\int{q(x)e^{\int{p(x)dx}}+C}\\
y&=\{\int{q(x)e^{\int{p(x)dx}}}+C\}e^{-\int{p(x)dx}}
\end{aligned}
{{< /katex >}}

ここで {{< katex >}}h(x)=e^{\int{p(x)dx}}{{< /katex >}} とおくと

{{< katex display >}}
y=\frac{1}{h(x)}\{\int{q(x)h(x)dx}+C\}
{{< /katex >}}

### 例題

1. {{< katex >}}y'+2xy=2x{{< /katex >}}
1. {{< katex >}}y'-(2x+1)y=2xe^x{{< /katex >}}

## ベルヌーイの微分方程式

### 定義

{{< katex display >}}
y'+p(x)y=q(x)y^\alpha
{{< /katex >}}

### 解法

{{< katex >}}y^\alpha\ne0{{< /katex >}} のとき、両辺を {{< katex >}}y^\alpha{{< /katex >}} で割って

{{< katex display >}}
y^{-\alpha}y'+p(x)y^{1-\alpha}=q(x)
{{< /katex >}}

{{< katex >}}u=y^{1-\alpha}{{< /katex >}} とおく。このとき
{{< katex >}}u'=(1-\alpha)y^{-\alpha}y'{{< /katex >}} となるので

{{< katex display >}}
\begin{aligned}
\frac{1}{1-\alpha}u'+p(x)u&=q(x)\\
u'+(1-\alpha)p(x)u&=(1-\alpha)q(x)
\end{aligned}
{{< /katex >}}

となり、線形微分方程式と同じように解ける。

<!-- TODO 完全微分方程式について書く -->

### 例題

1. {{< katex >}}y'+y=e^xy^2{{< /katex >}}
1. {{< katex >}}w'=aw^\dfrac23-bw,w(0)=0{{< /katex >}} (von Bertalanffy の成長曲線)

## クレローの微分方程式

### 定義

{{< katex display >}}
y=xy'+f(y')
{{< /katex >}}

### 解法

{{< katex >}}y'=p{{< /katex >}} とおくと

{{< katex display >}}
y=xp+f(p) \tag{*}
{{< /katex >}}

両辺を {{< katex >}}x{{< /katex >}} で微分すると

{{< katex display >}}
\begin{aligned}
y'=p+xp'+f'(p)p'\\
\{x+f'(p)\}p'=0
\end{aligned}
{{< /katex >}}

よって {{< katex >}}p'=0{{< /katex >}} または {{< katex >}}x+f'(p)=0{{< /katex >}}

1. {{< katex >}}p'=0{{< /katex >}} のとき

    {{< katex >}}p=C{{< /katex >}} を {{< katex >}}*{{< /katex >}} に代入すると、一般解が得られる。

    {{< katex display >}}
    y=Cx+f(C)
    {{< /katex >}}

2. {{< katex >}}x+f'(p){{< /katex >}} のとき

    {{< katex display >}}
    \begin{cases}
    \begin{aligned}
    y&=xp+f(p)\\
    x+f'(p)&=0
    \end{aligned}
    \end{cases}
    {{< /katex >}}

    より、**特異解**が得られる。

    {{< katex display >}}
    (x,y)=(-f'(p),-pf'(p)+f(p))
    {{< /katex >}}

### 例題

1. {{< katex >}}y=xy'+(y')^2{{< /katex >}}
1. {{< katex >}}y=xp+\cos{p}{{< /katex >}}

## 参考文献

- 井上 満, 工業数学がわかる, 技術評論社, 2010
- ヨビノリたくみ, [【大学数学】偏微分とは何か【解析学】](https://youtu.be/UWFTIEIruyc), 2018
- ヨビノリたくみ, [【大学数学】全微分とは何か【解析学】](https://youtu.be/ChoArVJnSjQ), 2018
- ヨビノリたくみ, [【大学数学】微分方程式入門①(微分方程式とは)](https://youtu.be/po97dnBfoco), 2020
- ヨビノリたくみ, [【大学数学】微分方程式入門②(変数分離形)](https://youtu.be/uPRY-KUl4fg), 2020
- ヨビノリたくみ, [【大学数学】微分方程式入門③(同次形)](https://youtu.be/QeYOiFU6UNs), 2020
- ヨビノリたくみ, [【大学数学】微分方程式入門④(一階線形微分方程式)](https://youtu.be/Hfby9zyZ0HY)
- ヨビノリたくみ, [【大学数学】微分方程式入門⑤(ベルヌーイの微分方程式)](https://youtu.be/TaVimHlrN4U), 2020
- ヨビノリたくみ, [【大学数学】微分方程式入門⑦(クレローの微分方程式)](https://youtu.be/P1dh8bg2mus), 2020
