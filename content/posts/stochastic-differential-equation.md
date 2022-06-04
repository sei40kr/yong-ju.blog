---
title: "確率微分方程式"
date: 2022-06-04T19:09:52+09:00
categories: ["数学"]
tags: ["数学", "大学数学", "確率統計", "確率微分方程式", "WIP"]
---

## 前提知識

- [確率統計]({{< ref "statistics" >}})

## ランダムウォーク

{{< katex display >}}
\begin{aligned}
S_n&=X_1+X_2+\cdots+X_n\\
P[X_i=\sigma]&=P[X_i=-\sigma]=\dfrac12\;(1\le i\le n)
\end{aligned}
{{< /katex >}}

で与えられる確率変数 {{< katex >}}S_n{{< /katex >}} を (1次元) **ランダムウォーク (random walk)** という。

{{< katex >}}X_i{{< /katex >}} の平均 {{< katex >}}E[X_i]{{< /katex >}} と分散 {{< katex >}}V[X_i]{{< /katex >}} は以下のようになる。

{{< katex display >}}
\begin{aligned}
E[X_i]&=0\\
V[X_i]&=\sigma^2
\end{aligned}
{{< /katex >}}

また、{{< katex >}}X_1,X_2,\dots,X_n{{< /katex >}} は互いに独立であることから

{{< katex display >}}
\begin{aligned}
E[S_n]&=E[X_1+X_2+\cdots+X_n]\\
&=E[X_1]+E[X_2]+\cdots+E[X_n]\\
&=0\\
V[S_n]&=V[X_1+X_2+\cdots+X_n]\\
&=V[X_1]+V[X_2]+\cdots+V[X_n]\\
&=\sigma^2n
\end{aligned}
{{< /katex >}}

が導ける。
