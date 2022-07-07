---
title: "動的計画法"
date: 2022-07-07T23:45:17+09:00
tags: ["動的計画法", "アルゴリズム", "競プロ"]
categories: ["競プロ"]
---

## LCS

数列 (あるいは文字列) {{< katex >}}\bold{a,b}{{< /katex >}} の最長共通部分列 (longest common subsequence, LCS) の長さを {{< katex >}}O(|\bold{a}||\bold{b}|){{< /katex >}} で求めることができる。

{{< katex display >}}
\begin{aligned}
dp_{0,j}&=dp_{i,0}=0\\
dp_{i+1,j+1}&=\begin{cases}
dp_{i,j}+1&(\bold{a}_i=\bold{b}_j)\\
\max(dp_{i+1,j},dp_{i,j+1})&(\text{otherwise})
\end{cases}
\end{aligned}\\[2ex]
\text{where:}\\
1\le i\le|\bold{a}|, 1\le j\le|\bold{b}|\\
dp_{i,j}:\{\bold{a}_1\dots\bold{a}_i\}\,\text{と}\,\{\bold{b}_1\dots\bold{b}_j\}\,\text{のLCSの長さ}\\
{{< /katex >}}

このとき、{{< katex >}}dp_{|\bold{a}|,|\bold{b}|}{{< /katex >}} が、求める数列 {{< katex >}}\bold{a,b}{{< /katex >}} の最長共通部分列の長さである。

{{< hint info >}}
{{< katex >}}dp_{0,j},dp_{i,0}{{< /katex >}} は空数列とのLCSの長さ (必ず 0) になるので、実装するときは数列を表す配列の添字を 1-indexed として扱うと実装しやすい。
{{< /hint >}}
