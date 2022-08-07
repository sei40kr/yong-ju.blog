---
title: "回帰分析"
date: 2022-08-07T19:54:24+09:00
categories: ["数学", "勉強ノート"]
tags: ["数学", "大学数学", "勉強ノート"]
---

## 前提知識

- [確率統計]({{< ref "statistics" >}})

## 最小二乗法

**最小二乗法 (least squares method)** は、測定で得られたデータセットを一次関数 (直線) で近似するときに、二乗誤差の和が最小になるように一次関数の係数を決定する方法である。

{{< katex >}}n{{< /katex >}} 個のデータ {{< katex >}}(X,Y)=\{(x_1,y_1),(x_2,y_2),\dots,(x_i,y_i){{< /katex >}} を最小二乗法で一次関数 {{< katex >}}y=ax+b{{< /katex >}} の形に近似すると、一次関数の係数 {{< katex >}}a,b{{< /katex >}} は

{{< katex display >}}
\begin{aligned}
a&=\dfrac{\text{Cov}[X,Y]}{\Bbb{V}[X]}\\
b&=-a\Bbb{E}[X]+\Bbb{E}[Y]
\end{aligned}
{{< /katex >}}

となる。

{{< details title="導出" >}}
    
一次関数 {{< katex >}}y=ax+b{{< /katex >}} の形で近似したときの二条誤差の和 {{< katex >}}\epsilon(a,b){{< /katex >}} は

{{< katex display >}}
\epsilon(a,b)=\sum_i(y_i-ax_i-b)^2
{{< /katex >}}
    
となる。
  
{{< katex >}}a{{< /katex >}} を定数とみなすと、{{< katex >}}\epsilon(a,b){{< /katex >}} は下に凸な二次関数であるため

{{< katex display >}}
\begin{aligned}
\dfrac{\partial\epsilon(a,b)}{\partial b}&=0\\
-2\sum_i(y_i-ax_i-b)&=0\\
a\sum_i{x_i}+bn&=\sum_i{y_i}\\
a\Bbb{E}[X]+bn&=\Bbb{E}[Y]
\end{aligned}
{{< /katex >}}

同様に {{< katex >}}b{{< /katex >}} を定数とみなすと、{{< katex >}}\epsilon(a,b){{< /katex >}} は下に凸な二次関数であるため

{{< katex display >}}
\begin{aligned}
\dfrac{\partial\epsilon(a,b)}{\partial a}&=0\\
-2\sum_ix_i(y_i-ax_i-b)&=0\\
a\sum_i{x_i^2}+b\sum_i{x_i}&=\sum_i{x_iy_i}
\end{aligned}
{{< /katex >}}

ここで {{< katex >}}b=\dfrac{-a\Bbb{E}[X]+\Bbb{E}[Y]}n{{< /katex >}} を代入して

{{< katex display >}}
a\sum_i{x_i^2}+\left(\dfrac{-a\Bbb{E}[X]+\Bbb{E}[Y]}n\right)\sum_i{x_i}=\sum_i{x_iy_i}
{{< /katex >}}

両辺を {{< katex >}}n{{< /katex >}} で割ると

{{< katex display >}}
\begin{aligned}
a\Bbb{E}[X^2]+(-a\Bbb{E}[X]+\Bbb{E}[Y])\Bbb{E}[X]&=\Bbb{E}[XY]\\
a&=\dfrac{\Bbb{E}[XY]-\Bbb{E}[X]\Bbb{E}[Y]}{\Bbb{E}[X^2]-\Bbb{E}[X]^2}
\end{aligned}
{{< /katex >}}

ここで {{< katex >}}\Bbb{E}[XY]-\Bbb{E}[X]\Bbb{E}[Y]=\text{Cov}[X,Y],\Bbb{E}[X^2]-\Bbb{E}[X]^2=\Bbb{V}[X]{{< /katex >}} より

{{< katex display >}}
\begin{aligned}
a&=\dfrac{\text{Cov}[X,Y]}{\Bbb{V}[X]}\\
b&=-a\Bbb{E}[X]+\Bbb{E}[Y]
\end{aligned}
{{< /katex >}}
{{< /details >}}

## TODO

- [ ] 語句の定義
- [ ] 最小二乗法の幾何学的な導出
- [ ] 分類問題
- [ ] 混同行列と分類問題の評価
- [ ] ロジスティック回帰
- [ ] 相関と因果
- [ ] 分析結果の解釈

## 参考

- ヨビノリたくみ, [確率統計 - YouTube](https://www.youtube.com/playlist?list=PLDJfzGjtVLHmx7qMP410-9gx0weC9d90X)
- 杉山 聡, 本質を捉えたデータ分析のための分析モデル入門, 2022
