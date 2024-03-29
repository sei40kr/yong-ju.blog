---
title: "複素関数論"
date: 2022-02-18T03:55:11+09:00
categories: ["数学"]
tags: ["複素関数論", "複素解析", "複素数", "大学数学", "数学", "勉強ノート", "WIP"]
---

## ド・モアブルの定理

{{< katex >}}z=r(\cos\theta+i\sin\theta){{< /katex >}} のとき

{{< katex display >}}
z^n=r^n(\cos{n\theta}+i\sin{n\theta})
{{< /katex >}}

ただし、{{< katex >}}n{{< /katex >}} は任意の整数

{{< details title="証明" >}}
オイラーの公式より

{{< katex display >}}
\begin{aligned}
z&=r(\cos\theta+i\sin\theta)\\
&=re^{i\theta}
\end{aligned}
{{< /katex >}}

両辺を {{< katex >}}n{{< /katex >}} 乗して

{{< katex display >}}
\begin{aligned}
z^n&=r^ne^{in\theta}\\
&=r^n(\cos{n\theta}+i\sin{n\theta})
\end{aligned}
{{< /katex >}}
{{< /details >}}

<!-- TODO 複素数の対数関数 -->
<!-- TODO 複素数の累乗関数 -->

## コーシー・リーマンの関係式

複素関数 {{< katex >}}f(x+iy)=u(x,y)+iv(x,y){{< /katex >}} において、以下の関係を**コーシー・リーマンの関係式** (以下、CRの関係式) という。

{{< katex display >}}
\begin{aligned}
\dfrac{\partial u}{\partial x}(x,y)&=\dfrac{\partial v}{\partial y}(x,y)\\
\dfrac{\partial u}{\partial y}(x,y)&=-\dfrac{\partial v}{\partial x}(x,y)
\end{aligned}
{{< /katex >}}

**{{< katex >}}f(z){{< /katex >}} が {{< katex >}}z{{< /katex >}} で微分可能であることは、{{< katex >}}u(x,y),v(x,y){{< /katex >}} が全微分可能かつCRの関係式が成り立つことに等しい。**

{{< details title="CRの関係式の導出" >}}
{{< katex >}}f(z){{< /katex >}} において {{< katex >}}z{{< /katex >}} が {{< katex >}}\Delta z{{< /katex >}} だけ増加したときの変化の割合を求めると

{{< katex display >}}
\begin{aligned}
&=\dfrac{f(z+\Delta z)-f(z)}{\Delta z}\\
&=\dfrac{\{u(x+\Delta x,y+\Delta y)+iv(x+\Delta x,y+\Delta y)\}-\{u(x,y)+iv(x,y)\}}{\Delta x+i\Delta y}\\
&=\dfrac{\{u(x+\Delta x,y+\Delta y)-u(x,y)\}+i\{v(x+\Delta x,y+\Delta y)-v(x,y)\}}{\Delta x+i\Delta y}
\end{aligned}
{{< /katex >}}

{{< katex >}}\lim\Delta y\rightarrow0{{< /katex >}} の場合 (実軸と平行に近づけて微分した場合)

{{< katex display >}}
\begin{aligned}
&=\lim_{\Delta x\rightarrow0}\dfrac{\{u(x+\Delta x,y)-u(x,y)\}+i\{v(x+\Delta x,y)-v(x,y)\}}{\Delta x}\\
&=\dfrac{\partial u}{\partial x}(x,y)+i\dfrac{\partial v}{\partial x}(x,y)=f'(z)
\end{aligned}
{{< /katex >}}

{{< katex >}}\lim\Delta x\rightarrow0{{< /katex >}} の場合 (虚軸と平行に近づけて微分した場合)

{{< katex display >}}
\begin{aligned}
&=\lim_{\Delta y\rightarrow0}\dfrac{\{u(x,y+\Delta y)-u(x,y)\}+i\{v(x,y+\Delta y)-v(x,y)\}}{i\Delta y}\\
&=-i\dfrac{\partial u}{\partial y}(x,y)+\dfrac{\partial v}{\partial y}(x,y)=f'(z)
\end{aligned}
{{< /katex >}}

これらの式の実部と虚部を比較すると

{{< katex display >}}
\begin{cases}
\dfrac{\partial u}{\partial x}(x,y)&=\dfrac{\partial v}{\partial y}(x,y)\\
\dfrac{\partial u}{\partial y}(x,y)&=-\dfrac{\partial v}{\partial x}(x,y)
\end{cases}
{{< /katex >}}

が導ける。
{{< /details >}}

## 複素関数の積分

区分的に滑らかな積分路 {{< katex >}}C{{< /katex >}} における複素関数 {{< katex >}}f(z){{< /katex >}} の積分は、{{< katex >}}z(t)=x(t)+y(t)\;(a\le t\le b){{< /katex >}} とおくと

{{< katex display >}}
\int_Cf(z)dz=\int_a^bf(z(t))
\dfrac{dz(t)}{dt}dt
{{< /katex >}}

と表せる。

### 性質

1. {{< katex display >}}\int_C\{f(z)+g(z)\}dz=\int_Cf(z)dz+\int_Cg(z)dz{{< /katex >}}
1. {{< katex display >}}\int kf(z)dz=k\int f(z)dz{{< /katex >}}
1. {{< katex display >}}\int_{-C}f(z)dz=-\int_Cf(z)dz{{< /katex >}}
1. {{< katex display >}}\int_Cf(z)dz=\int_{C_1}f(z)dz+\int_{C_2}f(z)dz{{< /katex >}}

## コーシーの積分定理

{{< katex >}}f(z)=u+iv{{< /katex >}} は {{< katex >}}D{{< /katex >}} で正則であり、かつ {{< katex >}}u,v{{< /katex >}} は {{< katex >}}C^1{{< /katex >}} 級であるとする。 
単純閉曲線 {{< katex >}}C{{< /katex >}} で囲まれた領域を {{< katex >}}\Omega{{< /katex >}} として、{{< katex >}}\bar\Omega{{< /katex >}} が {{< katex >}}D{{< /katex >}} に含まれるならば、次が成り立つ。

{{< katex display >}}
\oint_{C}f(z)dz=0
{{< /katex >}}

{{< details title="証明" >}}
{{< katex display >}}
\begin{aligned} 
\oint_Cf(z)dz&=\int_a^bf(z(t))z'(t)dt\\
&=\int_a^b\{u(x(t),y(t))+iv(x(t),y(t))\}\{x'(t)+iy'(t)\}dt\\
&=\int_a^b\{u(x(t),y(t))x'(t)-v(x(t),y(t))y'(t)\}dt+i\int_a^b\{u(x(t),y(t))y'(t)+v(x(t),y(t))x'(t)\}dt\\
&=\oint_C\{u(x,y)dx-v(x,y)dy\}+i\oint_C\{u(x,y)dy+v(x,y)dx\}
\end{aligned}
{{< /katex >}}

グリーンの定理 (後述) より

{{< katex display >}}
\oint_Cf(z)dz=\iint_\Omega\left(-\dfrac{\delta u}{\delta y}-\dfrac{\delta v}{\delta x}\right)dxdy+\iint_\Omega\left(\dfrac{\delta u}{\delta x}-\dfrac{\delta v}{\delta y}\right)dxdy
{{< /katex >}}

コーシー・リーマンの方程式より

{{< katex display >}}
\begin{cases}
-\dfrac{\delta u}{\delta y}-\dfrac{\delta v}{\delta x}&=0\\
\dfrac{\delta u}{\delta x}-\dfrac{\delta v}{\delta y}&=0 
\end{cases}
{{< /katex >}}

代入して

{{< katex display >}}
\oint_Cf(z)dz=0
{{< /katex >}}
{{< /details >}}

{{< hint info >}}
**グリーンの定理**

単純閉曲線で囲まれた領域を {{< katex >}}\Omega{{< /katex >}} とし、{{< katex >}}\bar\Omega=(\Omega+\partial\Omega){{< /katex >}} で {{< katex >}}C^1{{< /katex >}} 級である {{< katex >}}P(x,y),Q(x,y){{< /katex >}} に対して、次が成り立つ。

{{< katex display >}}
\oint_{\partial\Omega}(Pdx+Qdy)=\iint_\Omega\left(\dfrac{\partial Q}{\partial x}-\dfrac{\partial
P}{\partial y}\right)dxdy
{{< /katex >}}
{{< /hint >}}

## 積分路の変形I

{{< katex >}}f(z){{< /katex >}} が単連結領域 {{< katex >}}D{{< /katex >}} で正則とする。2つの曲線 {{< katex >}}C_1,C_2\in D{{< /katex >}} が共通の始点と終点をもつとき

{{< katex display >}}
\int_{C_1}f(z)dz=\int_{C_2}f(z)dz
{{< /katex >}}

{{< hint info "light-bulb" >}}
単連結な正則領域では積分が経路に依らない。
{{< /hint >}}

{{< details title="証明" >}}

{{< katex >}}C_1,C_2{{< /katex >}} が端点以外で交差していない場合を考える。

コーシーの積分定理より

{{< katex display >}}
\begin{aligned}
\oint_{C_1-C_2}f(z)dz&=\oint_{C_1}f(z)dz-\oint_{C_2}f(z)dz=0\\
\therefore\oint_{C_1}f(z)dz&=\oint_{C_2}f(z)dz
\end{aligned}
{{< /katex >}}

また、{{< katex >}}C_1,C_2{{< /katex >}} が交差する場合でも、交差する点で積分路を分割すると自明に成り立つ。
{{< /details >}}

## 積分路の変形II

単純閉曲線 {{< katex >}}C_1,C_2{{< /katex >}} で囲まれた環状領域を {{< katex >}}D{{< /katex >}} とし、{{< katex >}}\bar D{{< /katex >}} で正則な {{< katex >}}f(z){{< /katex >}} に対して、次が成り立つ。

{{< katex display >}}
\oint_{C_1}f(z)dz=\oint_{C_2}f(z)dz
{{< /katex >}}

## コーシーの積分公式

単純閉曲線 {{< katex >}}C{{< /katex >}} で囲まれる領域を {{< katex >}}D{{< /katex >}} とし、{{< katex >}}f(z){{< /katex >}} は {{< katex >}}\bar{D}{{< /katex >}} で正則であるとする。
このとき、任意の {{< katex >}}z\in D{{< /katex >}} に対し、次が成り立つ。

{{< katex display >}}
f(z)=\dfrac1{2\pi i}\oint_C\dfrac{f(\zeta)}{\zeta-z}d\zeta
{{< /katex >}}

{{< hint info "light-bulb" >}}
コーシーの積分公式では、ある点 {{< katex >}}f(z){{< /katex >}} の周囲の値から、その点での関数 {{< katex >}}f{{< /katex >}} の値 {{< katex >}}f(z){{< /katex >}} を求めることができている。
{{< /hint >}}

<!-- TODO コーシーの積分公式を証明 -->

## グルサの公式

単純閉曲線 {{< katex >}}C{{< /katex >}} で囲まれる領域を {{< katex >}}D{{< /katex >}} とし、{{< katex >}}f(z){{< /katex >}} は {{< katex >}}\bar{D}{{< /katex >}} で正則であるとする。
このとき、{{< katex >}}f(z){{< /katex >}} は {{< katex >}}D{{< /katex >}} 内の点 {{< katex >}}z{{< /katex >}} で何回でも微分可能となる。

また、任意の自然数 {{< katex >}}n{{< /katex >}} に対して {{< katex >}}f^{(n)}(z){{< /katex >}} は {{< katex >}}D{{< /katex >}} 上で正則となり次が成り立つ。

{{< katex display >}}
f^{(n)}(z)=\dfrac{n!}{2\pi i}\oint_C\dfrac{f(\zeta)}{(\zeta-z)^{n+1}}d\zeta
{{< /katex >}}

{{< details title="証明 (注: 厳密でない)" >}}
{{< katex display >}}
f'(z)=\lim_{\Delta z\to0}\dfrac{f(z+\Delta z)-f(z)}{\Delta z}
{{< /katex >}}

コーシーの積分公式より

{{< katex display >}}
\begin{aligned}
f'(z)&=\lim_{\Delta z\to0}\dfrac1{(\Delta z)2\pi i}\oint_C\left\{\dfrac1{\zeta-(z+\Delta z)}-\dfrac1{\zeta-z}\right\}f(\zeta)d\zeta\\
&=\lim_{\Delta z\to0}\dfrac1{2\pi i}\oint_C\dfrac{f(\zeta)}{\{\zeta-(z+\Delta z)\}(\zeta-z)}d\zeta
\end{aligned}
{{< /katex >}}

{{< katex >}}\Delta z\rightarrow0{{< /katex >}} に近づけると

{{< katex display >}}
f'(z)=\dfrac1{2\pi i}\oint_C\dfrac{f(\zeta)}{(\zeta-z)^2}d\zeta
{{< /katex >}}
この操作を繰り返すと、一般に次の式が得られる。

{{< katex display >}}
f^{(n)}(z)=\dfrac{n!}{2\pi i}\oint_C\dfrac{f(\zeta)}{(\zeta-z)^{n+1}}d\zeta
{{< /katex >}}
{{< /details >}}

## 複素関数のテイラー展開

複素関数 {{< katex >}}f(z){{< /katex >}} は閉円板 {{< katex >}}\bar{D}(\alpha,R){{< /katex >}} で正則であるとする。このとき、任意の {{< katex >}}z\in D(\alpha,R){{< /katex >}} に対し、次の等式が成り立つ。

{{< katex display >}}
\begin{aligned}
f(z)&=f(\alpha)+f'(\alpha)(z-\alpha)+\dfrac1{2!}f''(\alpha)(z-\alpha)^2+\cdots\\
&=\sum_{n=0}^\infty\dfrac{f^{(n)}(\alpha)}{n!}(z-\alpha)^n
\end{aligned}
{{< /katex >}}

{{< hint info >}}
実関数のテイラー展開の公式が複素関数にもそのまま使える。
{{< /hint >}}

{{< details title="証明 (注: 厳密でない)" >}}
コーシーの積分公式より

{{< katex display >}}
\begin{aligned}
f(z)&=\dfrac1{2\pi i}\int_C\dfrac{f(\zeta)}{\zeta-z}d\zeta\\
&=\dfrac1{2\pi i}\int_C\dfrac{f(\zeta)}{\zeta-\alpha}\dfrac1{1-\frac{z-\alpha}{\zeta-\alpha}}d\zeta
\end{aligned}
{{< /katex >}}

{{< katex >}}\left|\dfrac{z-a}{\zeta-a}\right|<1{{< /katex >}} であることから、等比級数の公式より

{{< katex display >}}
\begin{aligned}
f(z)&=\dfrac1{2\pi i}\int_C\dfrac{f(\zeta)}{\zeta-\alpha}\sum_{n=0}^\infty(\dfrac{z-\alpha}{\zeta-\alpha})^nd\zeta\\
&=\sum_{n=0}^\infty\dfrac1{n!}\dfrac{n!}{2\pi i}\int_C\dfrac{f(\zeta)}{(\zeta-\alpha)^{n+1}}d\zeta(z-\alpha)^n
\end{aligned}
{{< /katex >}}

グルサの公式より

{{< katex display >}}
f(z)=\sum_{n=0}^\infty\dfrac1{n!}f^{(n)}(\alpha)(z-\alpha)^n
{{< /katex >}}
{{< /details >}}

## ローラン展開

{{< katex >}}D=\{z\in\Bbb{C}\mid R_1<|z-\alpha|<R_2\}\;(0\le R_1<R_2\le\infty){{< /katex >}} とする。
{{< katex >}}f(z){{< /katex >}} が {{< katex >}}\bar{D}{{< /katex >}} で正則な関数であるとき、任意の {{< katex >}}z\in D{{< /katex >}} に対し、次の等式が成り立つ。

{{< katex display >}}
\begin{aligned}
c_n&=\dfrac1{2\pi i}\oint_C\dfrac{f(\zeta)}{(\zeta-\alpha)^{n+1}}d\zeta\;(n=0,\pm1,\pm2,\dots)\\
f(z)&=\cdots+\dfrac{c_{-2}}{(z-\alpha)^2}
+\dfrac{c_{-1}}{(z-\alpha)}+c_0+c_1(z-\alpha)+c_2(z-\alpha)^2+\cdots\\
&=\sum_{n=-\infty}^\infty c_n(z-\alpha)^n
\end{aligned}
{{< /katex >}}

ただし {{< katex >}}C{{< /katex >}} は {{< katex >}}D{{< /katex >}} 内の {{< katex >}}\alpha{{< /katex >}} を内部に含む任意の円。

テイラー展開にはない {{< katex >}}z-\alpha{{< /katex >}} の負のべき乗を含む項の系列を**主要部**という。

## 孤立特異点

{{< katex >}}f(z){{< /katex >}} が {{< katex >}}D=\{z\in \Bbb{C}\mid0<|z-\alpha|<R\}\enspace(R\le\infty){{< /katex >}} で正則であり、{{< katex >}}z=\alpha{{< /katex >}} で正則でないとき、点 {{< katex >}}\alpha{{< /katex >}} を**孤立特異点 (isolated singularity)** という。

特に、{{< katex >}}f(z){{< /katex >}} のローラン級数の主要部が

1. 存在しない場合は**可除特異点 (removable singularity)** という
1. {{< katex >}}k{{< /katex >}} 個存在 (有限かつ {{< katex >}}k\ne0{{< /katex >}}) する場合は **{{< katex >}}k{{< /katex >}} 位の極 (k-th pole)** という
1. {{< katex >}}主要部が特異点{{< /katex >}} である場合は**真性特異点 (essential singularity)** という

## 留数定理

{{< katex >}}\alpha{{< /katex >}} を中心とするローラン展開における {{< katex >}}c_{-1}{{< /katex >}} を {{< katex >}}f(z){{< /katex >}} の {{< katex >}}z=\alpha{{< /katex >}} における**留数 (residue)** といい、{{< katex >}}\text{Res}(f(z),\alpha){{< /katex >}} で表す。

{{< katex >}}f(z){{< /katex >}} が単純閉曲線 {{< katex >}}C{{< /katex >}} とその内部で {{< katex >}}C{{< /katex >}} 内の孤立特異点 {{< katex >}}\alpha_1,\alpha_2,\dots,\alpha_n{{< /katex >}} を除いて正則であるとき次の等式が成り立つ。

{{< katex display >}}
\oint_Cf(z)dz=2\pi i\sum_{k=1}^n\text{Res}(f(z),\alpha_k)
{{< /katex >}}

{{< hint info >}}
{{< katex >}}f(z){{< /katex >}} の周回積分の値が内部の留数の和で求められている。
{{< /hint >}}

{{< details title="証明">}}
{{< katex display >}}
C_n=\dfrac1{2\pi i}\oint\dfrac{f(\zeta)}{(\zeta-\alpha)^{n+1}}d\zeta
{{< /katex >}}

ここで、両辺に {{< katex >}}n=-1{{< /katex >}} を代入すると

{{< katex display >}}
\begin{aligned}
C_{-1}=\text{Res}(f(z),\alpha_k)&=\dfrac1{2\pi i}\oint{f(\zeta)}d\zeta\\
2\pi i\cdot\text{Res}(f(z),\alpha_k)&=\oint_C{f(\zeta)d\zeta}
\end{aligned}
{{< /katex >}}
{{< /details >}}
