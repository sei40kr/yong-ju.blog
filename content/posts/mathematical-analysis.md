---
title: "解析学"
date: 2021-01-05T04:53:19+09:00
categories: ["数学"]
tags: ["解析学", "数学", "大学数学", "勉強ノート"]
---

## 前提知識

* 微分
* 積分
* 複素数

## テイラー展開

**テイラー展開** (Taylor expansion) は、関数のある一点での導関数たちの値から計算される項の無限和として関数を表したものである。

{{< katex display >}}
\begin{aligned}
f(x)&=f(a)+f{'}(a)(x-a)+\frac{1}{2!}f{''}(x)(x-a)^2+\frac{1}{3!}f{'''}(a)(x-a)^3+\dots\\
&=\sum_{n=0}^\infty{\frac1{n!}f^{(n)}(a)(x-a)^n}
\end{aligned}
{{< /katex >}}

特に {{< katex >}}a=0{{< /katex >}} のときのテイラー展開を**マクローリン展開** (Maclaurin expansion) という。

{{< katex display >}}
f(x)=\sum_{n=0}^\infty{\frac1{n!}f^{(n)}(0)x^n}
{{< /katex >}}

{{< hint info >}}
テイラー展開 (マクローリン展開) をすることによって、複雑な関数を多項式で表せる。
{{< /hint >}}

## オイラーの公式

以下の関係式を**オイラーの公式** (Euler's formula) という。

{{< katex display >}}
e^{iy}=\cos{y}+i\sin{y}
{{< /katex >}}

特に {{< katex >}}\theta=\pi{{< /katex >}} のとき

{{< katex display >}}
e^{i\pi}+1=0
{{< /katex >}}

が導かれ、この関係式を**オイラーの等式** (Euler's identity) という。

{{< hint info >}}
オイラー公式を用いれば、複素数の極座標表示は

{{< katex display >}}
z=r(\cos{\theta}+i\sin{\theta})=re^{i\theta}
{{< /katex >}}

と表される。
{{< /hint >}}

{{< details title="証明 (注: 厳密でない)" >}}
{{< katex >}}\cos\theta,\sin\theta{{< /katex >}} をそれぞれマクローリン展開すると

{{< katex display >}}
\begin{aligned}
\cos\theta&=1-\dfrac1{2!}\theta^2+\dfrac1{4!}\theta^4-\dfrac1{6!}\theta^6+\cdots\\
\sin\theta&=\theta-\dfrac1{3!}\theta^3+\dfrac1{5!}\theta^5-\dfrac1{7!}\theta^7+\cdots\tag{1}
\end{aligned}
{{< /katex >}}

{{< katex >}}e^x{{< /katex >}} をマクローリン展開すると

{{< katex display >}}
e^x=1+x+\dfrac1{2!}x^2+\dfrac1{3!}x^3+\dfrac1{4!}x^4+\dfrac1{5!}x^5+\dfrac1{6!}x^6+\dfrac1{7!}x^7+\cdots\tag{2}
{{< /katex >}}

(2) に {{< katex >}}x=i\theta{{< /katex >}} を形式的に代入すると

{{< katex display >}}
\begin{aligned}
e^{i\theta}&=1+i\theta-\dfrac1{2!}\theta^2-\dfrac1{3!}i\theta^3+\dfrac1{4!}\theta^4+\dfrac1{5!}i\theta^5-\dfrac1{6!}\theta^6-\dfrac1{7!}i\theta^7+\cdots\\
&=\left(1-\dfrac1{2!}\theta^2+\dfrac1{4!}\theta^4-\dfrac1{6!}\theta^6+\cdots\right)+i\left(\theta-\dfrac1{3!}i\theta^3+\dfrac1{5!}i\theta^5-\dfrac1{7!}i\theta^7+\cdots\right)\\
&=\cos\theta+i\sin\theta
\end{aligned}
{{< /katex >}}
{{< /details >}}

## ε-δ論法

### 定義

関数 {{< katex >}}f(x){{< /katex >}} は {{< katex >}}x=a{{< /katex >}} で連続であるとは

{{< katex display >}}
\lim_{x\to a}f(x)=b
{{< /katex >}}

が成り立つことである。

これをε-δ論法で定義すると

{{< katex display >}}
^\forall\varepsilon>0,^\exists\delta>0~\mathrm{s.t.}~^\forall x\in \R,|x-a|<\delta\Rightarrow|f(x)-b|<\varepsilon
{{< /katex >}}

となり、これは

任意の正の数 {{< katex >}}\varepsilon{{< /katex >}} に対し、ある適当な正の数 {{< katex >}}\delta{{< /katex >}} が存在して、{{< katex >}}\delta<|x-a|{{< /katex >}} を満たす全ての実数 {{< katex >}}x{{< /katex >}} に対し、{{< katex >}}|f(x)-b|<\varepsilon{{< /katex >}} が成り立つという意味の条件である。

## ガウス積分

### 定義

{{< katex display >}}
\int_{-\infty}^\infty e^{-x^2}dx=\sqrt\pi
{{< /katex >}}

{{< details title="証明" >}}}
{{< katex >}}I=\int_{-\infty}^\infty e^{-x^2}dx{{< /katex >}} とおく

{{< katex display >}}
\begin{aligned}
I^2&=\left(\int_{-\infty}^\infty e^{-x^2}dx\right)\left(\int_{-\infty}^\infty e^{-x^2}dx\right)\\
&=\int_{-\infty}^\infty\int_{-\infty}^\infty e^{-(x^2+y^2)}dxdy
\end{aligned}
{{< /katex >}}

{{< katex >}}x=r\cos\theta,y=r\sin\theta{{< /katex >}} とおく

{{< katex display >}}
\begin{aligned}
I^2&=\int_0^{2\pi}\int_0^\infty e^{-r^2}\{\pi(r+dr)^2\times\frac{d\theta}{2\pi}-\pi r^2\times\frac{d\theta}{2\pi}\}\\
&=\int_0^{2\pi}\int_0^\infty e^{-r^2}(rdrd\theta+\frac12(dr)^2d\theta)\\
&=\int_0^{2\pi}\int_0^\infty e^{-r^2}rdrd\theta\\
&=\int_0^{2\pi}d\theta\int_0^\infty re^{-r^2}dr\\
&=2\pi\left[-\frac12e^{-r^2}\right]_0^\infty\\
&=\pi
\end{aligned}
{{< /katex >}}

{{< katex >}}I>0{{< /katex >}} なので
{{< katex display >}}
I=\sqrt\pi
{{< /katex >}}
{{< /details >}}

## 双曲線関数

### 定義

{{< katex display >}}
\begin{aligned}
\sinh(x)&=\frac{e^x-e^{-x}}{2}\\
\cosh(x)&=\frac{e^x+e^{-x}}{2}\\
\tanh(x)&=\frac{e^x-e^{-x}}{e^x+e^{-x}}
\end{aligned}
{{< /katex >}}

### 性質

双曲線関数は三角関数に似た性質をもっている。

{{< katex display >}}
\begin{aligned}
\cosh^2{x}+\sinh^2{x}&=1\\
\tanh{x}&=\frac{\sinh{x}}{\cosh{x}}\\
1-\tanh^2{x}&=\frac{1}{\cosh^2{x}}\\
(\sinh{x})'&=\cosh{x}\\
(\cosh{x})'&=\sinh{x}\\
(\tanh{x})'&=\frac1{\cosh^2{x}}\\
\int_{-\infty}^\infty e^{-x^2}dx&=\sqrt\pi
\end{aligned}
{{< /katex >}}

{{< details title="なぜ三角関数に性質が似るのか" >}}
オイラーの公式 {{< katex >}}e^{i\theta}=\cos{\theta}+i\sin{\theta}{{< /katex >}} を用いて、三角関数 {{< katex >}}\cos{\theta},\sin{\theta}{{< /katex >}} を表すと

{{< katex display >}}
\begin{aligned}
\cos{\theta}&=\frac{e^{i\theta}+e^{-i\theta}}{2}\\
\sin{\theta}&=\frac{e^{i\theta}-e^{-i\theta}}{2i}
\end{aligned}
{{< /katex >}}

となり、双曲線関数と式の形が似ているため。
{{< /details >}}

## ロピタルの定理

### 定義

{{< katex >}}\lim_{x\rightarrow a}{{< /katex >}} が
{{< katex >}}\dfrac00{{< /katex >}} か
{{< katex >}}\dfrac{\pm\infty}{\pm\infty}{{< /katex >}}
の不定形であり、次の条件をすべて満たすとき

1. {{< katex >}}\lim_{x\rightarrow a}f(x)=\lim_{x\rightarrow a}g(x){{< /katex >}}
   が {{< katex >}}0{{< /katex >}} または {{< katex >}}\pm\infty{{< /katex >}}
1. {{< katex >}}a{{< /katex >}} を含むある開区間から {{< katex >}}a{{< /katex >}}
   を除くすべての点で {{< katex >}}g'(x)\ne0{{< /katex >}}
1. 極限 {{< katex >}}\lim_{x\rightarrow a}\dfrac{f'(x)}{g'(x)}{{< /katex >}}
   が存在する

このとき、極限 {{< katex >}}\lim_{x\rightarrow a}\dfrac{f(x)}{g(x)}{{< /katex >}}
も存在し

{{< katex display >}}
\lim_{x\rightarrow a}\frac{f(x)}{g(x)}=\lim_{x\rightarrow a}\frac{f'(x)}{g'(x)}
{{< /katex >}}

が成り立つ。

### 例題

1. {{< katex >}}\lim_{x\rightarrow0}\dfrac{x+\sin{x}}x{{< /katex >}}
1. {{< katex >}}\lim_{x\rightarrow\infty}\dfrac{x}{e^x}{{< /katex >}}
1. {{< katex >}}\lim_{x\rightarrow0}\dfrac{\sin2x}{x+\sin{x}}{{< /katex >}}
1. {{< katex >}}\lim_{x\rightarrow0}\dfrac{x-\sin{x}}{x^3}{{< /katex >}}

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

{{< details title="関数の内積" >}}
{{< katex >}}f(x),g(x){{< /katex >}} を周期 {{< katex >}}2\pi{{< /katex >}} の周期関数とすると、その内積は

{{< katex display >}}
\int_{-\pi}^\pi{f(x)g(x)dx}
{{< /katex >}}

で定義される。
{{< /details >}}

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

## ライプニッツの法則

ライプニッツの法則は、{{< katex >}}f,g{{< /katex >}} を {{< katex >}}n{{< /katex >}} 回微分可能な関数としたときの、それらの積 {{< katex >}}f\cdot g{{< /katex >}} の {{< katex >}}n{{< /katex >}} 階微分の一般化である。

### 定義

{{< katex display >}}
(f\cdot g)^{(n)}=\sum_{k=0}^n{_nC_kf^{(n-k)}g^{(k)}}
{{< /katex >}}

## sup, inf

### 定義

{{< katex >}}A{{< /katex >}} を空でない実数 {{< katex >}}R{{< /katex >}} の集合とする。

#### max

{{< katex display >}}
\max{A}=\alpha\Rightarrow A~\text{の最大値は}~\alpha
{{< /katex >}}

1. 任意の {{< katex >}}x\in A{{< /katex >}} に対して {{< katex >}}x\le\alpha{{< /katex >}} ({{< katex >}}\alpha{{< /katex >}} は {{< katex >}}A{{< /katex >}} の上界)
1. {{< katex >}}\alpha\in A{{< /katex >}} → **{{< katex >}}\alpha{{< /katex >}} も {{< katex >}}A{{< /katex >}} に入っていけなければならない**

#### sup

{{< katex display >}}
\sup{A}=\alpha\Rightarrow A~\text{の上限は}~\alpha
{{< /katex >}}

1. 任意の {{< katex >}}x\in A{{< /katex >}} に対して {{< katex >}}x \le\alpha{{< /katex >}}
   ({{< katex >}}\alpha{{< /katex >}} は {{< katex >}}A{{< /katex >}} の上界)
1. {{< katex >}}\alpha{{< /katex >}} より小さい任意の実数 {{< katex >}}\beta{{< /katex >}} に対し {{< katex >}}\beta\lt x{{< /katex >}} なる {{< katex >}}x\in A{{< /katex >}} が存在 → **{{< katex >}}\alpha{{< /katex >}} 自体は {{< katex >}}A{{< /katex >}} に入ってなくてもよい**

---

同様に

{{< katex display >}}
\begin{aligned}
\min{A}=\alpha &\Rightarrow A~\text{の最小値は}~\alpha \\
\inf{A}=\alpha &\Rightarrow A~\text{の下限は}~\alpha
\end{aligned}

{{< /katex >}}

### 性質

1. {{< katex >}}\sup{A}\in A\Rightarrow\sup{A}=\max{A}{{< /katex >}}
1. {{< katex >}}A\text{ が上に有界} \Rightarrow \sup{A}\text{ が存在}{{< /katex >}}
1. {{< katex >}}\inf{A}\in A\Rightarrow\inf{A}=min{A}{{< /katex >}}
1. {{< katex >}}A\text{ が下に有界 }\Rightarrow\inf{A}\text{ が存在}{{< /katex >}}

## ガンマ関数

### 定義

{{< katex display >}}
\Gamma(s)=\int_0^\infty{x^{s-1}\exp{(-x)}dx}\,(s>0)
{{< /katex >}}

### 性質

1. {{< katex >}}s>1{{< /katex >}} のとき

   {{< katex display >}}
   \Gamma(s)=(s-1)\Gamma(s-1)
   {{< /katex >}}

   {{< details title="証明">}}
   {{< katex display >}}
   \begin{aligned}
   \Gamma(s)&=\int_0^\infty{x^{s-1}e^{-x}dx}\\
   &=\left[x^{s-1}(-e^{-x})\right]_0^\infty+\int_0^\infty{(s-1)x^{s-2}e^{-x}dx}\\
   &=(s-1)\Gamma(s-1)
   \end{aligned}
   {{< /katex >}}
   {{< /details >}}

1. {{< katex >}}s{{< /katex >}} が正の整数のとき

   {{< katex display >}}
   \Gamma(s)=(s-1)!
   {{< /katex >}}

   {{< details title="s が正の整数のとき Γ(s)=(s-1)! となる証明">}}
   {{< katex display >}}
   \begin{aligned}
   \Gamma(s)&=(s-1)\Gamma(s-1)\\
   &=(s-1)(s-2)\Gamma(s-2)\\
   &=(s-1)(s-2)(s-3)\cdots1\cdot\Gamma(1)\\
   \Gamma(1)&=\int_0^\infty{e^{-x}dx}\\
   &=\left[-e^{-x}\right]_0^\infty\\
   &=1\\
   \therefore \Gamma(s)&=(s-1)!
   \end{aligned}
   {{< /katex >}}
   {{< /details >}}

1. {{< katex display >}}
   \Gamma(\frac12)=\sqrt\pi
   {{< /katex >}}

   {{< details title="Γ(1/2)=√π となる証明" >}}
   {{< katex display >}}
   \Gamma(\frac12)=\int_0^\infty{x^{-\frac12}e^{-x}dx}
   {{< /katex >}}

   ここで {{< katex >}}x=t^2{{< /katex >}} とおくと

   {{< katex display >}}
   dx=2tdt\\
   \begin{array}{c|c}
   x&0\to\infty\\
   \hline t&0\to\infty
   \end{array}
   {{< /katex >}}

   より

   {{< katex display >}}
   \begin{aligned}
   \Gamma(\frac12)&=\int_0^\infty{t^{-1}e^{-t^2}\cdot2tdt}\\
   &=2\int_0^\infty{e^{-t^2}dt}\\
   &=\int_{-\infty}^\infty{e^{-t^2}dt}
   \end{aligned}
   {{< /katex >}}

   となり、ガウス積分より

   {{< katex display >}}
   \Gamma(\frac12)=\sqrt\pi
   {{< /katex >}}
   {{< /details >}}

## 参考文献

- 井上 満, 工業数学がわかる, 技術評論社, 2010
- Wikipedia, [オイラーの公式](https://ja.wikipedia.org/wiki/%E3%82%AA%E3%82%A4%E3%83%A9%E3%83%BC%E3%81%AE%E5%85%AC%E5%BC%8F)
- Wikipedia, [イプシロン-デルタ論法](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%83%97%E3%82%B7%E3%83%AD%E3%83%B3-%E3%83%87%E3%83%AB%E3%82%BF%E8%AB%96%E6%B3%95)
- Wikipedia, [ロピタルの定理](https://ja.wikipedia.org/wiki/%E3%83%AD%E3%83%94%E3%82%BF%E3%83%AB%E3%81%AE%E5%AE%9A%E7%90%86)
- Wikipedia, [一般のライプニッツの法則](https://ja.wikipedia.org/wiki/%E4%B8%80%E8%88%AC%E3%81%AE%E3%83%A9%E3%82%A4%E3%83%97%E3%83%8B%E3%83%83%E3%83%84%E3%81%AE%E6%B3%95%E5%89%87)
- ヨビノリたくみ, [【大学数学】ガウス積分の証明【解析学】](https://youtu.be/TvZpbYRIh48), 2017
- ヨビノリたくみ, [【大学数学】双曲線関数とは何か【解析学】](https://youtu.be/Yvcngy6xtio), 2017
- ヨビノリたくみ, [【大学数学】テイラー展開の気持ち【解析学】 - YouTube](https://youtu.be/qzd5iXKHkiU), 2017
- ヨビノリたくみ, [ロピタルの定理 ①(定理と使用例)](https://youtu.be/dRpnR2Q6GPI), 2020
- ヨビノリたくみ, [【大学数学】フーリエ解析入門 ①(フーリエ級数展開 I)/全 5 講【解析学】](https://youtu.be/HNHb0_mOTYw), 2017
- ヨビノリたくみ, [【大学数学】フーリエ解析入門 ②(フーリエ級数展開 II)/全 5 講【解析学】](https://youtu.be/8F2B7wcGHHA), 2017
- ヨビノリたくみ, [【大学数学】フーリエ解析入門 ③(フーリエ級数展開 III)/全 5 講【解析学】](https://youtu.be/OYqznq3E0p0), 2020
- ヨビノリたくみ, [【大学数学】フーリエ解析入門 ④(フーリエ級数展開 IV)/全 5 講【解析学】](https://youtu.be/0UJhcP-Q8zQ), 2020
- ヨビノリたくみ, [【大学数学】sup と inf(上限と下限)【解析学】](https://youtu.be/pySvmqhB6BY), 2018
- ヨビノリたくみ, [【大学数学】ガンマ関数 ①(定義と性質)【解析学】](https://youtu.be/K-HwL3N4P5Q), 2019
