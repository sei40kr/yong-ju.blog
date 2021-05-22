---
title: "高校数学"
date: 2021-05-22T16:54:25+09:00
tags: ["勉強ノート", "数学"]
---

## 三角関数

### 基本定理

{{< katex display >}}
\begin{aligned}
\sin(-\theta)&=-\sin\theta \\
\cos(-\theta)&=\cos\theta \\
\tan(-\theta)&=-\tan\theta \\
\sin^2\theta+\cos^2\theta&=1
\end{aligned}
{{< /katex >}}

### 余弦定理

{{< katex display >}}
\begin{aligned}
a^2=b^2+c^2-2bc\cos\theta
\end{aligned}
{{< /katex >}}

### 加法定理

{{< katex display >}}
\begin{aligned}
\sin(\alpha+\beta)&=\sin\alpha\cos\beta+\cos\alpha\sin\beta \\
\sin(\alpha-\beta)&=\sin\alpha\cos\beta-\cos\alpha\sin\beta \\
\cos(\alpha+\beta)&=\cos\alpha\cos\beta-\sin\alpha\sin\beta \\
\cos(\alpha-\beta)&=\cos\alpha\cos\beta+\sin\alpha\sin\beta \\
\tan(\alpha+\beta)&=\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta} \\
\tan(\alpha-\beta)&=\frac{\tan\alpha-\tan\beta}{1+\tan\alpha\tan\beta}
\end{aligned}
{{< /katex >}}

### 2倍角の公式

{{< katex display >}}
\begin{aligned}
\sin2\alpha&=\sin(\alpha+\alpha) \\
&=2\sin\alpha\cos\alpha \\
\cos2\alpha&=\cos(\alpha+\alpha) \\
&=\cos^2\alpha-\sin^2\alpha=2\cos^2\alpha-1=1-2\sin^2\alpha
\end{aligned}
{{< /katex >}}

### 半角の公式

{{< katex display >}}
\begin{aligned}
\sin^2\frac\alpha2&=\frac{1-\cos\alpha}2 \\
\cos^2\frac\alpha2&=\frac{1+\cos\alpha}2 \\
\tan^2\frac\alpha2&=\frac{\sin^2\frac\alpha2}{\cos^2\frac\alpha2}=\frac{1-\cos\alpha}{1+\cos\alpha}
\end{aligned}
{{< /katex >}}

#### 半角の公式の導出

{{< katex >}}\cos2\alpha=1-2\sin^2\alpha{{< /katex >}} より

{{< katex display >}}
sin^2\alpha=\frac{1-\cos2\alpha}2
{{< /katex >}}

ここで {{< katex >}}\alpha{{< /katex >}} を {{< katex >}}\frac\alpha2{{< /katex >}} に置き換えると

{{< katex display >}}
\sin^2\frac\alpha2=\frac{1-\cos\alpha}2
{{< /katex >}}

となる。

同様に {{< katex >}}\cos2\alpha=2\cos^2\alpha-1{{< /katex >}} より

{{< katex display >}}
\cos^2\frac\alpha2=\frac{1+\cos\alpha}2
{{< /katex >}}

が導ける。

### 積和の公式

{{< katex display >}}
\begin{aligned}
\sin\alpha\cos\beta&=\frac12\{\sin(\alpha+\beta)+\sin(\alpha-\beta)\} \\
\cos\alpha\cos\beta&=\frac12\{\cos(\alpha+\beta)+\cos(\alpha-\beta)\} \\
\sin\alpha\sin\beta&=-\frac12\{\cos(\alpha+\beta)-\cos(\alpha-\beta)\}
\end{aligned}
{{< /katex >}}

### 和積の公式

{{< katex display >}}
\begin{aligned}
\sin x+\sin y&=2\sin\frac{x+y}2\cos\frac{x-y}2 \\
\sin x-\sin y&=2\cos\frac{x+y}2\sin\frac{x-y}2 \\
\cos x+\cos y&=2\cos\frac{x+y}2\cos\frac{x-y}2 \\
\cos x-\cos y&=-2\sin\frac{x+y}2\sin\frac{x-y}2 \\
\end{aligned}
{{< /katex >}}

#### 和積の公式の導出

積和の公式 {{< katex >}}\sin\alpha\cos\beta=\frac12\{\sin(\alpha+\beta)+\sin(\alpha-\beta)\}{{< /katex >}} に {{< katex >}}(\alpha,\beta)=(\frac{x+y}2,\frac{x-y}2){{< /katex >}} を代入すると

{{< katex display >}}
\begin{aligned}
\sin\frac{x+y}2\cos\frac{x-y}2&=\frac12\{\sin(\frac{x+y}2+\frac{x-y}2)+\sin(\frac{x+y}2-\frac{x-y}2)\} \\
&=\frac12(\sin x+\sin y) \\
\sin x+\sin y&=2\sin\frac{x+y}2\cos\frac{x-y}2
\end{aligned}
{{< /katex >}}

となる。

また、同式に {{< katex >}}(\alpha,\beta)=(\frac{x-y}2,\frac{x+y}2){{< /katex >}} を代入して整理すると

{{< katex display >}}
\sin x-\sin y=2\cos\frac{x+y}2\sin\frac{x-y}2
{{< /katex >}}

となる。

同様に、{{< katex >}}\cos\alpha\cos\beta=\frac12\{\cos(\alpha+\beta)+\cos(\alpha-\beta)\}{{< /katex >}} に、 {{< katex >}}(\alpha,\beta)=(\frac{x+y}2,\frac{x-y}2){{< /katex >}} を代入して整理すると

{{< katex display >}}
\cos x+\cos y=2\cos\frac{x+y}2\cos\frac{x-y}2
{{< /katex >}}

{{< katex >}}\sin\alpha\sin\beta=\frac12\{\cos(\alpha+\beta)-\cos(\alpha-\beta)\}{{< /katex >}} に {{< katex >}}(\alpha,\beta)=(\frac{x+y}2,\frac{x-y}2){{< /katex >}} を代入して整理すると

{{< katex display >}}
\cos x-\cos y=2\sin\frac{x+y}2\sin\frac{x-y}2
{{< /katex >}}

が導ける。
