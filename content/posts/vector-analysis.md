---
title: "ベクトル解析"
date: 2022-05-07T21:10:30+09:00
categories: ["数学"]
tags: ["数学", "ベクトル", "勉強ノート"]
---

## ベクトル空間

空でない集合 {{< katex >}}\Bbb{V}{{< /katex >}} について {{< katex >}}\Bbb{V}{{< /katex >}} の任意の元 {{< katex >}}\bold{a},\bold{b}{{< /katex >}} に対して {{< katex >}}\bold{a}+\bold{b}\in\Bbb{V}{{< /katex >}}、{{< katex >}}\Bbb{V}{{< /katex >}} の任意の元 {{< katex >}}\bold{a}{{< /katex >}} と {{< katex >}}\Bbb{R}{{< /katex >}} の任意の元 {{< katex >}}k{{< /katex >}} (スカラー) に対して {{< katex >}}k\bold{a}\in\Bbb{V}{{< /katex >}} が定義されていて、以下の性質を全て満たすとき、{{< katex >}}\Bbb{V}{{< /katex >}} を **{{< katex >}}\Bbb{R}{{< /katex >}} 上のベクトル空間**という。

- **ベクトル加法の結合律を満たす。**
    
  {{< katex display >}}
  (\bold{a}+\bold{b})+\bold{c}=\bold{a}+(\bold{b}+\bold{c})
  {{< /katex >}}
    
- **ベクトル加法の可換律を満たす。**

  {{< katex display >}}
  \bold{a}+\bold{b}=\bold{b}+\bold{a}
  {{< /katex >}}
- **ベクトル加法の単位元が存在する。**

  {{< katex display >}}
  \forall{\bold{a}\in\Bbb{V}},\bold{a}+\bold{0}=\bold{a}
  {{< /katex >}}
- **ベクトル加法の逆元が存在する。**
    
  {{< katex display >}}
  \forall{\bold{a}\in\Bbb{V}},\exist{\bold{x}\in\Bbb{V}},\bold{a}+\bold{x}=\bold{0}
  {{< /katex >}}
    
- **ベクトル加法に対するスカラー乗法の分配律を満たす。**

  {{< katex display >}}
  k(\bold{a}+\bold{b})=k\bold{a}+k\bold{b}
  {{< /katex >}}
- **体の加法に対するスカラー乗法の分配律を満たす。**

  {{< katex display >}}
  (k+l)\bold{a}=k\bold{a}+l\bold{a}
  {{< /katex >}}
- **体の乗法とスカラー乗法の条件が両立する。**

  {{< katex display >}}
  k(l\bold{a})=(kl)\bold{a}
  {{< /katex >}}
- **スカラー乗法の単位元が存在する。**
    
  {{< katex display >}}
  1\bold{a}=\bold{a}
  {{< /katex >}}
  
### 定理
  
- {{< katex >}}0\bold{a}=\bold{0}{{< /katex >}}

  {{< details title="証明" >}}
  公理より

  {{< katex display >}}
  k\bold{a}+l\bold{a}=(k+l)\bold{a}
  {{< /katex >}}

  ここで {{< katex >}}k=l=0{{< /katex >}} とすると

  {{< katex display >}}
  \begin{aligned}
  0\bold{a}+0\bold{a}&=0\bold{a}\\
  0\bold{a}+0\bold{a}-0\bold{a}&=0\bold{a}-0\bold{a}\\
  \therefore0\bold{a}&=\bold{0}
  \end{aligned}
  {{< /katex >}}
  {{< /details >}}
- {{< katex >}}(-1)\bold{a}=-\bold{a}{{< /katex >}}

  {{< details title="証明" >}}
  公理より

  {{< katex display >}}
  k\bold{a}+l\bold{a}=(k+l)\bold{a}
  {{< /katex >}}

  ここで {{< katex >}}k=1,l=-1{{< /katex >}} とすると

  {{< katex display >}}
  \begin{aligned}
  1\bold{a}+(-1)\bold{a}&=0\bold{a}\\
  \bold{a}+(-1)\bold{a}&=\bold{0}\\
  \bold{a}+(-\bold{a})+(-1)\bold{a}&=\bold{0}+(-\bold{a})\\
  \therefore(-1)\bold{a}&=-\bold{a}
  \end{aligned}
  {{< /katex >}}
  {{< /details >}}
