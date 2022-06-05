---
title: "量子力学"
date: 2022-06-04T14:08:03+09:00
categories: ["物理学"]
tags: ["物理学", "大学物理", "量子論", "量子力学", "勉強ノート", "WIP"]
---

## 前提知識

- [微分方程式]({{< ref "differential-equation" >}})

## ド・ブロイの関係式

質量 {{< katex >}}m{{< /katex >}} の粒子が速さ {{< katex >}}v{{< /katex >}} (運動量 {{< katex >}}mv=p{{< /katex >}}) で運動する場合、その粒子は以下の式で示される波長 {{< katex >}}\lambda{{< /katex >}} に相当する波 **(ド・ブロイ波, de Broglie wave)** であるとみなせる。

{{< katex display >}}
\lambda=\dfrac{h}{mv}=\dfrac{h}p,\nu=\dfrac{E}h
{{< /katex >}}

式中の {{< katex >}}h\thickspace(\simeq6.63\times10^{-34}){{< /katex >}} を**プランク定数 (Planck constant)** という。
また、ド・ブロイ波の波長 {{< katex >}}\lambda{{< /katex >}} を**ド・ブロイ波長 (de Broglie wavelength)** という。

## 不確定性関係

粒子の位置と運動量が両方確定している状態は存在しない。

{{< katex display >}}
\Delta{x}\Delta{p}\ge\hbar\;(\hbar=\dfrac{h}{2\pi})
{{< /katex >}}

<!-- TODO 小澤の不等式の説明 -->

{{< hint info >}}
不確定性関係は、確率的に振る舞う量子の特性について述べたもので、系を測定する行為そのものが系に影響を与えてしまう観測者効果とは本質的に異なるものである。
{{< /hint >}}

## シュレディンガー方程式

**シュレディンガー方程式 (Schrodinger equation)** (以下、S.eq) は、量子の状態を表す波動関数を解にもつ、量子力学における基礎方程式である。

{{< katex display >}}
i\hbar\dfrac\delta{\delta t}\psi(\bold{r},t)=\left\{-\dfrac{\hbar^2}{2m}\nabla^2+V(\bold{r})\right\}\psi(\bold{r},t)
{{< /katex >}}

系の全エネルギー **(ハミルトニアン, Hamiltonian)** に相当する {{< katex >}}-\dfrac{\hbar^2}{2m}\nabla^2+V(\bold{r}){{< /katex >}} を {{< katex >}}\hat{H}{{< /katex >}} で表すことがある。<br />
{{< katex >}}\hat{H}{{< /katex >}} を用いると、前述のS.eqは

{{< katex display >}}
i\hbar\dfrac\delta{\delta t}\psi(\bold{r},t)=\hat{H}\psi(\bold{r},t)
{{< /katex >}}

と表せる。

{{< details title="導出" >}}
ドブロイの関係式 {{< katex >}}\lambda=\dfrac{h}p,\nu=\dfrac{E}h{{< /katex >}} より、{{< katex >}}\sin\left(\dfrac{p}\hbar x-\dfrac{E}\hbar t\right),\cos\left(\dfrac{p}\hbar x-\dfrac{E}\hbar t\right){{< /katex >}} を組み合わせて運動量 {{< katex >}}p{{< /katex >}} をもつ一次元の波 {{< katex >}}\psi(r,t){{< /katex >}} を考える。

<!-- TODO 波の公式を復習 -->

{{< katex >}}\Delta p=0,\Delta x=\infty\implies|\psi(r,t)|^2=\text{一定}{{< /katex >}} であることから

{{< katex display >}}
\begin{aligned}
\psi(x,t)&=A\left\{\cos\left(\dfrac{p}\hbar x-\dfrac{E}\hbar t\right)+i\sin\left(\dfrac{p}\hbar x-\dfrac{E}\hbar t\right)\right\}\\
&=A\exp\left\{i\left(\frac{p}\hbar x-\frac{E}\hbar t\right)\right\}
\end{aligned}
{{< /katex >}}

がこれを満たす。

<!-- TODO 虚数を使った理由を説明 -->

次に、{{< katex >}}\psi(x,t){{< /katex >}} を使って、運動エネルギーの式 {{< katex >}}E=\dfrac{p^2}{2m}{{< /katex >}} を表してみる。

{{< katex display >}}
\begin{cases}
\dfrac\partial{\partial t}\psi(x,t)=-i\dfrac{E}\hbar\psi(x,t)\\
\dfrac{\partial^2}{\partial x^2}\psi(x,t)=-\dfrac{p^2}{\hbar^2}\psi(x,t)
\end{cases}
{{< /katex >}}
より

{{< katex display >}}\begin{cases}
E&=-i\hbar\dfrac\partial{\partial t}\psi(x,t)\\
\dfrac{p^2}{2m}&=-\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2}\psi(x,t)
\end{cases}
{{< /katex >}}
となり、{{< katex >}}E=\dfrac{p^2}{2m}{{< /katex >}} は

{{< katex display >}}
i\hbar\dfrac{\partial}{\partial t}\psi(x,t)=-\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2}\psi(x,t)

{{< /katex >}}
と表せる。

ここで、ポテンシャル {{< katex >}}V(x){{< /katex >}} を考慮する。<br />
具体的には {{< katex >}}-\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2}\psi(x,t){{< /katex >}} ({{< katex >}}E{{< /katex >}} に相当する部分) を {{< katex >}}-\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2}\psi(x,t)+V(x){{< /katex >}} で置き換える。

{{< katex display >}}
i\hbar\dfrac{\partial}{\partial t}\psi(x,t)=\left\{-\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2}\psi(x,t)+V(x)\right\}\psi(x,t)
{{< /katex >}}

位置 {{< katex >}}x{{< /katex >}} を、三次元に拡張すると

{{< katex display >}}
i\hbar\dfrac\delta{\delta t}\psi(\bold{r},t)=\left\{-\dfrac{\hbar^2}{2m}\nabla^2+V(\bold{r})\right\}\psi(\bold{r},t)
{{< /katex >}}

が導ける。
{{< /details >}}

## 定常状態

{{< katex >}}\psi(\bold{r},t){{< /katex >}} が {{< katex >}}\psi(\bold{r},t)=\varphi(\bold{r})f(t){{< /katex >}} の形 (変数分離形) で表せるようなS.eqの解 (特解) を考える。

S.eqに {{< katex >}}\psi(\bold{r},t)=\varphi(\bold{r})f(t){{< /katex >}} を代入して

{{< katex display >}}
\begin{aligned}
i\hbar\varphi(\bold{r})\dfrac{d}{dt}f(t)&=f(t)\hat{H}\varphi(\bold{r})\\
\dfrac{i\hbar}{f(t)}\dfrac{d}{dt}f(t)&=\dfrac1{\varphi(\bold{r})}\hat{H}{\varphi(\bold{r})}
\end{aligned}
{{< /katex >}}

ここで、{{< katex >}}\dfrac{i\hbar}{f(t)}\dfrac{d}{dt}f(t)=\dfrac1{\varphi(\bold{r})}\hat{H}{\varphi(\bold{r})}=E{{< /katex >}} とおくと

1. {{< katex >}}\dfrac{i\hbar}{f(t)}\dfrac{d}{dt}f(t)=E{{< /katex >}} より

   {{< katex display >}}
   \begin{aligned}
   \dfrac{d}{dt}f(t)&=-i\dfrac{E}\hbar f(t)\\
   f(t)&=C\exp\left(-i\frac{E}\hbar t\right)\;(C\text{ は積分定数})
   \end{aligned}
   {{< /katex >}}

1. {{< katex >}}\dfrac1{\varphi(\bold{r})}\hat{H}\varphi(\bold{r})=E{{< /katex >}} より

   {{< katex display >}}
   \hat{H}\varphi(\bold{r})=E\varphi(\bold{r})
   {{< /katex >}}
 
   が導ける。この方程式を**固有値方程式 (eigen equation)** という。
 
   固有値方程式を解くと {{< katex >}}(E,\varphi(\bold{r}))=(E_1,\varphi_1(\bold{r})),(E_2,\varphi_2(\bold{r})),\dots{{< /katex >}} のように独立な多数の解が得られる。<br />
   このときの、{{< katex >}}E_1,E_2,\dots{{< /katex >}} を**エネルギー固有値 (energy eigenvalue)** といい、{{< katex >}}\varphi_1(\bold{r}),\varphi_2(\bold{r}),\dots{{< /katex >}} を**エネルギー固有状態 (energy eigenstate)** という。

   とりうる状態の中でエネルギー固有値が最も低い状態を**基底状態 (ground state)**、それ以外の状態を**励起状態 (excited state)** という。<br />
   また、基底状態のときのエネルギー固有値を**零点エネルギー (zero-point energy)** という。
   
   このように、エネルギー {{< katex >}}E{{< /katex >}} が確定している状態のことを、量子力学における**定常状態 (steady state)** と定義する。
   
   {{< hint info >}}
   本来、物理学における定常状態は時間に依存しないはずだが、{{< katex >}}\psi(\bold{r},t){{< /katex >}} は時間 {{< katex >}}t{{< /katex >}} に依存しているように見える。

   しかし、物理的に意味があるのは {{< katex >}}\psi(\bold{r},t){{< /katex >}} そのものではなく {{< katex >}}|\psi(\bold{r},t)|^2{{< /katex >}} であり、これは

   {{< katex display >}}
   \begin{aligned}
   |\psi(\bold{r},t)|^2&=
   \left|\varphi(\bold{r})C\exp\left({-i\dfrac{E}\hbar t}\right)\right|^2\\
   &=|C|^2|\varphi(\bold{r})|^2
   \end{aligned}
   {{< /katex >}}
   
   となるため、量子力学における定常状態も本質的には時間 {{< katex >}}t{{< /katex >}} に依存しないことが言える。
   {{< /hint >}}

なお、S.eqの一般解は

{{< katex display >}}
\psi(\bold{r},t)=\sum_nC_n\exp\left(-i\dfrac{E_n}\hbar t\right)\varphi_n(\bold{r})
{{< /katex >}}

となる。

<!-- TODO エネルギー固有値が連続スペクトルをもつ場合の一般解を書く -->

## 無限に深い井戸型ポテンシャル

一次元のS.eq

{{< katex display >}}
\left\{-\dfrac{t^2}{2m}\dfrac{d^2}{dx^2}+V(x)\right\}\varphi(x)=E\varphi(x)
{{< /katex >}}

において

{{< katex display >}}
V(x)=\begin{cases}
0&(|x|\le a)\\
\infty&(|x|>a)
\end{cases}
{{< /katex >}}

のようなポテンシャルの形 (無限に深い井戸型ポテンシャル) を考える。

{{< katex >}}V(x){{< /katex >}} を代入すると

{{< katex display >}}
\begin{cases}
\begin{aligned}
-\dfrac{\hbar^2}{2m}\dfrac{d^2}{dx^2}\varphi(x)&=E\varphi(x)&(|x|\le a)\\
\varphi(x)&=0&(|x|>a)
\end{aligned}
\end{cases}
{{< /katex >}}

{{< hint info >}}
{{< katex >}}\varphi(x)=0\thickspace(|x|>a){{< /katex >}} より、無限に深い井戸型ポテンシャルでは粒子は限られた範囲にのみ存在することが言える。<br />
このような状態を**束縛状態 (bound state)** という。
{{< /hint >}}

{{< katex >}}|x|\le a{{< /katex >}} において

{{< katex display >}}
\dfrac{d^2}{dx^2}\varphi(x)=-\dfrac{2mE}{\hbar^2}\varphi(x)
{{< /katex >}}

ここで {{< katex >}}k=\dfrac{\sqrt{2mE}}\hbar{{< /katex >}} とおくと

{{< katex display >}}
\begin{aligned}
\dfrac{d^2}{dx^2}\varphi(x)&=-k^2\varphi(x)\\
\varphi(x)&=A\sin{kx}+B\cos{kx}
\end{aligned}
{{< /katex >}}

ここで、波動関数に連続性を課すと

{{< katex display >}}
\begin{cases}
\varphi(a)&=A\sin{ka}+B\cos{ka}=0\\
\varphi(-a)&=-A\sin{ka}+B\cos{ka}=0
\end{cases}
{{< /katex >}}

{{< katex >}}A=B=0{{< /katex >}} でない解を考えると

{{< katex display >}}
A=0,ka=\dfrac{n\pi}2\;(n=1,3,5,\dots)\\
B=0,ka=\dfrac{n\pi}2\;(n=2,4,6,\dots)
{{< /katex >}}

したがって、{{< katex >}}k=\dfrac{\sqrt{2mE}}\hbar{{< /katex >}} より

{{< katex display >}}
\begin{aligned}
E&=\dfrac{\hbar^2k^2}{2m}=\dfrac{\hbar^2\pi^2}{8ma^2}n^2\;(n=1,2,3,\dots)\\
\varphi(x)&=\begin{cases}
B\cos\dfrac{n\pi}{2a}x\;(n=1,3,5,\dots)\\
A\sin\dfrac{n\pi}{2a}x\;(n=2,4,6,\dots)
\end{cases}
\end{aligned}
{{< /katex >}}

よって

{{< katex display >}}
\text{束縛状態である}\implies\text{とりうるエネルギーの値が離散的}
{{< /katex >}}

ということが言える。

## 一般的性質

1. 束縛状態はすべて異なるエネルギー固有値をもつ (「**縮退 (degeneracy)** なし」という)

   <!-- TODO 証明 -->

1. {{< katex >}}V(x){{< /katex >}} が偶関数であるとき、束縛状態の波動関数は偶関数か奇関数のどちらかになる

   <!-- TODO 証明 -->

## 有限の深さの井戸型ポテンシャル

一次元のS.eq

{{< katex display >}}
\left\{-\dfrac{t^2}{2m}\dfrac{d^2}{dx^2}+V(x)\right\}\varphi(x)=E\varphi(x)
{{< /katex >}}

において

{{< katex display >}}
V(x)=\begin{cases}
0&(|x|\le a)\\
V_0&(|x|>a)
\end{cases}
{{< /katex >}}

のようなポテンシャルの形 (有限の深さの井戸型ポテンシャル) を考える。

{{< katex >}}k=\dfrac{\sqrt{2mE}}\hbar{{< /katex >}} とおくと

1. {{< katex >}}|x|\le a{{< /katex >}} のとき

   {{< katex display >}}
   \varphi(x)=A\sin{kx}+B\cos{kx}
   {{< /katex >}}

1. {{< katex >}}|x|>a{{< /katex >}} のとき

   {{< katex display >}}
   \begin{aligned}
   \left(-\dfrac{\hbar^2}{2m}\dfrac{d^2}{dx^2}+V_0\right)\varphi(x)&=E\varphi(x)\\
   \dfrac{d^2}{dx^2}\varphi(x)&=\dfrac{2m(V_0-E)}{\hbar^2}\varphi(x)
   \end{aligned}
   {{< /katex >}}

   ここで {{< katex >}}\rho=\dfrac{\sqrt{2m(V_0-E)}}{\hbar}\;(\rho>0){{< /katex >}} とおくと

   {{< katex display >}}
   \begin{aligned}
   \dfrac{d^2}{dx^2}\varphi(x)&=\rho^2\varphi(x)\\
   \therefore \varphi(x)&=C\exp{\rho x}+D\exp(-\rho x)
   \end{aligned}
   {{< /katex >}}

   {{< katex >}}x\to\pm\infty{{< /katex >}} で {{< katex >}}\varphi(x)\to0{{< /katex >}} となるように任意定数を選ぶと
   
   {{< katex display >}}
   \varphi(x)=\begin{cases}
   C\exp{\rho x}&(x<-a)\\
   D\exp(-\rho x)&(x>a)
   \end{cases}
   {{< /katex >}}

ここで

1. {{< katex >}}\varphi(x){{< /katex >}} が偶関数 ({{< katex >}}D=C{{< /katex >}}) である場合

   {{< katex display >}}
   \varphi(x)=\begin{cases}
   C\exp{\rho x}&(x<-a)\\
   B\cos{kx}&(-a\le x\le a)\\
   C\exp(-\rho x)&(x>a)
   \end{cases}
   {{< /katex >}}

   {{< katex >}}x=a{{< /katex >}} における {{< katex >}}\varphi(x){{< /katex >}} に連続条件を課すと

   {{< katex display >}}
   C\exp(-\rho a)=B\cos{ka}\tag{1}
   {{< /katex >}}

   また、{{< katex >}}x=a{{< /katex >}} における {{< katex >}}\varphi'(x){{< /katex >}} にも連続条件を課すと

   {{< katex display >}}
   C\rho\exp(-\rho a)=Bk\sin{ka}\tag{2}
   {{< /katex >}}

   {{< katex >}}\text{(2)}/\text{(1)}{{< /katex >}} より

   {{< katex display >}}
   \rho=k\tan{ka}
   {{< /katex >}}
   
1. {{< katex >}}\varphi(x){{< /katex >}} が奇関数 ({{< katex >}}D=-C{{< /katex >}}) である場合

   {{< katex display >}}
   \varphi(x)=\begin{cases}
   C\exp{\rho x}&(x<-a)\\
   A\sin{kx}&(-a\le x\le a)\\
   -C\exp(-\rho x)&(x>a)
   \end{cases}
   {{< /katex >}}

   {{< katex >}}x=a{{< /katex >}} における {{< katex >}}\varphi(x){{< /katex >}} に連続条件を課すと
   
   {{< katex display >}}
   -C\exp(-\rho a)=A\sin{ka}\tag{3}
   {{< /katex >}}

   また、{{< katex >}}x=a{{< /katex >}} における {{< katex >}}\varphi'(x){{< /katex >}} にも連続条件を課すと

   {{< katex display >}}
   C\rho\exp(-\rho a)=Ak\cos{ka}\tag{4}
   {{< /katex >}}

   {{< katex >}}\text{(4)}/\text{(3)}{{< /katex >}} より
   
   {{< katex display >}}
   \rho=-k\cot{ka}
   {{< /katex >}}

以上をまとめると

{{< katex display >}}
\begin{aligned}
\rho a&=ka\tan{ka}\\
\rho a&=-ka\cot{ka}
\end{aligned}
{{< /katex >}}

{{< katex >}}y=\rho a,x=ka{{< /katex >}} とおくと

{{< katex display >}}
\begin{aligned}
y&=x\tan{x}\\
y&=-x\cot{x}
\end{aligned}
{{< /katex >}}

また、{{< katex >}}x,y{{< /katex >}} は {{< katex >}}x^2+y^2=\dfrac{2mV_0a^2}{\hbar^2}{{< /katex >}} を満たすので

{{< katex display >}}
\begin{aligned}
y&=x\tan{x}\\
y&=-x\cot{x}\\
x^2+y^2&=\dfrac{2mV_0a^2}{\hbar^2}
\end{aligned}
{{< /katex >}}

の {{< katex >}}x>0,y>0{{< /katex >}} における交点が {{< katex >}}\varphi(x){{< /katex >}} の解となる。

よって

{{< katex display >}}
\begin{aligned}
(n-1)\pi\le\dfrac{\sqrt{2mV_0}a}{\hbar}<n\pi&\implies\text{偶関数解が }n\text{ 個存在}\\
(2n-1)\dfrac\pi2\le\dfrac{\sqrt{2mV_0}a}{\hbar}<(2n+1)\pi&\implies\text{奇関数解が }n\text{ 個存在}
\end{aligned}
{{< /katex >}}

が言える。
