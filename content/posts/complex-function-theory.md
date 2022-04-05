---
title: "複素関数論"
date: 2022-02-18T03:55:11+09:00
categories: ["数学"]
tags: ["数学", "複素解析", "複素数", "勉強ノート"]
---

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

## コーシーの積分公式

単純閉曲線 {{< katex >}}C{{< /katex >}} で囲まれる領域を {{< katex >}}D{{< /katex >}} とし、{{< katex >}}f(z){{< /katex >}} は {{< katex >}}\bar{D}{{< /katex >}} で正則であるとする。
このとき、任意の {{< katex >}}z\in D{{< /katex >}} に対し、次が成り立つ。

{{< katex display >}}
f(z)=\dfrac1{2\pi i}\oint_C\dfrac{f(\zeta)}{\zeta-z}d\zeta
{{< /katex >}}

{{< hint info "light-bulb" >}}
コーシーの積分公式では、ある点 {{< katex >}}f(z){{< /katex >}} の周囲の値から、その点での関数 {{< katex >}}f{{< /katex >}} の値 {{< katex >}}f(z){{< /katex >}} を求めることができている。
{{< /hint >}}