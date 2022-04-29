---
title: "群論"
date: 2022-04-21T01:30:53+09:00
categories: ["数学"]
tags: ["数学", "代数学", "群論", "勉強ノート"]
---

## 群

### 定義

集合 {{< katex >}}G{{< /katex >}} に対して二項演算 {{< katex >}}\circ{{< /katex >}}

{{< katex display >}}
G\to G\\
(a,b)\mapsto a\circ b
{{< /katex >}}

が与えられていて、以下の条件を全て満たすとき、{{< katex >}}G{{< /katex >}} を**群**という。

- **結合律**

   {{< katex display >}}
   \forall{a,b,c\in G},(a\circ b)\circ c=a\circ(b\circ c)
   {{< /katex >}}

- **単位元の存在**

   {{< katex >}}a\circ e=e\circ a=a{{< /katex >}} を {{< katex >}}G{{< /katex >}} のどんな元 {{< katex >}}a{{< /katex >}} に対しても満たすような
   {{< katex >}}G{{< /katex >}} の元 {{< katex >}}e{{< /katex >}} が存在する。

   {{< katex display >}}
   \forall{a\in G},\exist{e\in G},a\circ e=e\circ a=a
   {{< /katex >}}
   
   e は存在すれば一意であり、e を G の**単位元**という。

- **逆元の存在**

   {{< katex >}}G{{< /katex >}} のどんな元 {{< katex >}}a{{< /katex >}} に対しても
   {{< katex >}}a\circ x=x\circ a=e{{< /katex >}} となるような {{< katex >}}G{{< /katex >}} の元 {{< katex >}}x{{< /katex >}} が存在する。

   {{< katex display >}}
   \forall{a\in G},\exist{x\in G},a\circ x=x\circ a=e
   {{< /katex >}}
   
   {{< katex >}}x{{< /katex >}} は存在すれば一意である。
   {{< katex >}}x{{< /katex >}} を **{{< katex >}}a{{< /katex >}} の {{< katex >}}G{{< /katex >}} における逆元**といい、{{< katex >}}a^{-1}{{< /katex >}} で表す。

また、群 {{< katex >}}G{{< /katex >}} の元の個数を {{< katex >}}G{{< /katex >}} の**位数**といい、{{< katex >}}|G|{{< /katex >}} で表す。

**以降、{{< katex >}}a\circ b{{< /katex >}} を {{< katex >}}ab{{< /katex >}} で表す。**

### 定理

- 群 {{< katex >}}G{{< /katex >}} に対し、単位元は一意である。

   {{< details title="証明" >}}
   2つの単位元を {{< katex >}}e,e'{{< /katex >}} とする。

   {{< katex >}}e{{< /katex >}} は単位元であることから

   {{< katex display >}}
   ee'=e'\tag{1}
   {{< /katex >}}

   {{< katex >}}e'{{< /katex >}} は単位元であることから

   {{< katex display >}}
   ee'=e\tag{2}
   {{< /katex >}}

   (1), (2) より

   {{< katex display >}}
   ee'=e=e'
   {{< /katex >}}
   {{< /details >}}

- 任意の {{< katex >}}a\in G{{< /katex >}} に対し、逆元は一意である。

   {{< details title="証明" >}}
   {{< katex >}}a{{< /katex >}} の2つの逆元を {{< katex >}}b,b'{{< /katex >}} とする。
   {{< katex >}}b'a=e{{< /katex >}} より

   {{< katex display >}}
   b=(b'a)b=b'(ab)=b'
   {{< /katex >}}
   {{< /details >}}

<!-- TODO 群となる集合と演算の例 -->

## 可換群

任意の {{< katex >}}a,b\in G{{< /katex >}} に対して**交換法則**を満たすとき、具体的には

{{< katex display >}}
ab=ba
{{< /katex >}}

が成立するとき、{{< katex >}}G{{< /katex >}} を**可換群 (アーベル群)** という。

<!-- TODO 対称群 -->

## 部分群

### 定義

群 {{< katex >}}G{{< /katex >}} の空でない部分集合 {{< katex >}}H{{< /katex >}} が {{< katex >}}G{{< /katex >}} の二項演算によって群になるとき、{{< katex >}}H{{< /katex >}} を {{< katex >}}G{{< /katex >}} の部分群といい、{{< katex >}}H\le G{{< /katex >}} と表す。

### 定理

- {{< katex >}}H{{< /katex >}} の単位元 {{< katex >}}e'{{< /katex >}} と {{< katex >}}G{{< /katex >}} の単位元 {{< katex >}}e{{< /katex >}} は一致する。

   {{< details title="証明" >}}
   {{< katex >}}e'{{< /katex >}} の {{< katex >}}G{{< /katex >}} での逆元 {{< katex >}}x\in G{{< /katex >}} をとると

   {{< katex display >}}
   e'=(xe')e'=x(e'e')=e
   {{< /katex >}}
   {{< /details >}}

- {{< katex >}}H{{< /katex >}} と {{< katex >}}G{{< /katex >}} の逆元は一致する。

   {{< details title="証明" >}}
   {{< katex >}}c\in H{{< /katex >}} の {{< katex >}}H,G{{< /katex >}} での逆元をそれぞれ {{< katex >}}c',x{{< /katex >}} とすると

   {{< katex display >}}
   c'=c'e=c'(cx)=(cc')x=x
   {{< /katex >}}
   {{< /details >}}

- 群 {{< katex >}}G{{< /katex >}} の空でない部分集合 {{< katex >}}H{{< /katex >}} に対し

  {{< katex display >}}
  H\,\text{は}\,G\,\text{の部分群}\iff\forall a,b\in H,a^{-1}b\in H
  {{< /katex >}}

  が成立。

  {{< details title="証明" >}}
  {{< katex >}}\implies{{< /katex >}} の成立は自明であるため、{{< katex >}}\impliedby{{< /katex >}} の成立を示す。

  {{< katex >}}H\ne\empty{{< /katex >}} より、{{< katex >}}a\in H{{< /katex >}} がとれ

  {{< katex >}}a^{-1},b\in H{{< /katex >}} に対し

  {{< katex display >}}
  (a^{-1})^{-1}b=ab\in H
  {{< /katex >}}

  よって**演算に対して閉じている**。

  {{< katex >}}a\in H{{< /katex >}} より、{{< katex >}}a^{-1}a=e\in H{{< /katex >}}

  {{< katex display >}}
  a^{-1}a=e\in H
  {{< /katex >}}

  よって**単位元が存在**。

  {{< katex >}}a,e\in H{{< /katex >}} より、{{< katex >}}a^{-1}e=a^{-1}\in H{{< /katex >}}

  {{< katex display >}}
  a^{-1}e=a^{-1}\in H
  {{< /katex >}}

  よって**逆元が存在**。

  {{< katex >}}H{{< /katex >}} が {{< katex >}}G{{< /katex >}} と同じ演算について閉じているので、**結合律の成立は明らか**。
  {{< /details >}}

<!-- TODO 部分群の例 -->

## 同値関係/同値類

### 同値関係の定義

集合 {{< katex >}}S{{< /katex >}} において、関係 {{< katex >}}\sim{{< /katex >}} が定義されていて、2元 {{< katex >}}x,y\in S{{< /katex >}} に対し、{{< katex >}}x\sim y{{< /katex >}} であるか、{{< katex >}}x\sim y{{< /katex >}} でないかのいずれかが成立し、かつ次の3条件を満たすとき、関係 {{< katex >}}\sim{{< /katex >}} を**同値関係**という。

- **反射律**を満たす

  {{< katex display >}}
  x\sim x
  {{< /katex >}}

- **対称律**を満たす

  {{< katex display >}}
  x\sim y\implies y\sim x
  {{< /katex >}}

- **推移律**を満たす

  {{< katex display >}}
  x\sim y\land y\sim z\implies x\sim z
  {{< /katex >}}

### 同値類の定義

{{< katex >}}\sim{{< /katex >}} を集合 {{< katex >}}S{{< /katex >}} 上の同値関係とする。
{{< katex >}}x\in S{{< /katex >}} に対し

{{< katex display >}}
C(x)=\{y\in S\mid x\sim y\}
{{< /katex >}}

を **{{< katex >}}x{{< /katex >}} の同値類**という。

### 同値類の定理

- {{< katex >}}\forall{y,z\in C(x)},y\sim z{{< /katex >}}

  {{< details title="証明" >}}
  {{< katex >}}y\in C(x){{< /katex >}} より
  {{< katex display >}}
  x\sim y
  {{< /katex >}}

  {{< katex >}}z\in C(x){{< /katex >}} より
  {{< katex display >}}
  x\sim z\\
  \therefore{z\sim x}
  {{< /katex >}}

  よって、推移律より

  {{< katex display >}}
  x\sim z
  {{< /katex >}}
  {{< /details >}}

- {{< katex >}}y\in C(x)\implies C(x)=C(y){{< /katex >}}

  {{< details title="証明" >}}
  {{< katex >}}y\in C(x){{< /katex >}} より

  {{< katex display >}}
  \forall{z\in C(x)},y\sim z
  {{< /katex >}}

  よって

  {{< katex display >}}
  z\in C(y)\\
  \therefore C(x)\subset C(y)\tag{1}
  {{< /katex >}}

  {{< katex >}}y\in C(x){{< /katex >}} より
  
  {{< katex display >}}
  x\sim y\\
  \therefore{y\sim x}
  {{< /katex >}}

  {{< katex >}}x\in C(y){{< /katex >}} であり

  {{< katex display >}}
  \forall{w\in C(y)},x\sim w\\
  \therefore{w\in C(x)}
  {{< /katex >}}
  
  よって

  {{< katex display >}}
  C(x)\supset C(y)\tag{2}
  {{< /katex >}}

  (1), (2) より

  {{< katex display >}}
  C(x)=C(y)
  {{< /katex >}}
  {{< /details >}}

- {{< katex >}}C(x)\land C(y)\ne\empty\implies C(x)=C(y){{< /katex >}}

  {{< details title="証明" >}}

  {{< katex >}}z\in C(x)\land C(y){{< /katex >}} をとる。

  このとき、{{< katex >}}C(x)=C(z),C(y)=C(z){{< /katex >}} となるので

  {{< katex display >}}
  C(x)=C(y)
  {{< /katex >}}
  {{< /details >}}

## 商集合

集合 {{< katex >}}S{{< /katex >}} の同値関係 {{< katex >}}\sim{{< /katex >}} から定まる、同値類すべてを集めた集合のことを、
{{< katex >}}S{{< /katex >}} の {{< katex >}}\sim{{< /katex >}} による商集合であるといい、{{< katex >}}S/\sim{{< /katex >}} で表す。

{{< katex display >}}
S/\sim:=\{C(x_1),C(x_2),C(x_3),\dots\}
{{< /katex >}}

{{< hint info >}}
{{< katex >}}C(x_1),C(x_2),C(x_3),\dots{{< /katex >}} の各集合の要素に重複はない。
{{< /hint >}}

## 剰余類

### 定義

{{< katex >}}H{{< /katex >}} を群 {{< katex >}}G{{< /katex >}} の部分群とする。
{{< katex >}}a,b\in G{{< /katex >}} に対し、{{< katex >}}a^{-1}b\in H{{< /katex >}} となるとき {{< katex >}}a\sim b{{< /katex >}} と定義する。

これは同値関係であり、{{< katex >}}a\in G{{< /katex >}} の同値類を {{< katex >}}a{{< /katex >}} の {{< katex >}}H{{< /katex >}} による**左剰余類**という。
また、{{< katex >}}a,b\in H{{< /katex >}} に対し、{{< katex >}}ba^{-1}\in H{{< /katex >}} を {{< katex >}}a\sim b{{< /katex >}} の定義としたものを、{{< katex >}}a{{< /katex >}} の {{< katex >}}H{{< /katex >}} による**右剰余類**という。

{{< hint info >}}
{{< katex >}}G{{< /katex >}} が可換群であれば、左剰余類と右剰余類は同じ。
{{< /hint >}}

{{< details title="関係 ~ が同値関係であることの証明" >}}
{{< katex >}}a{{< /katex >}} を {{< katex >}}H{{< /katex >}} の左剰余類とする。

{{< katex >}}x\in G{{< /katex >}} より

{{< katex display >}}
x^{-1}x=e\in H\\
\therefore x\sim x
{{< /katex >}}

よって、**反射律**を満たす。

{{< katex >}}x,y\in G{{< /katex >}} で {{< katex >}}x\sim y{{< /katex >}} とすると

{{< katex display >}}
x^{-1}y\in H
{{< /katex >}}

{{< katex >}}H{{< /katex >}} は部分群なので

{{< katex display >}}
(x^{-1}y)^{-1}=y^{-1}x\in H\\
\therefore y\sim x
{{< /katex >}}

よって、**対象律**を満たす。

{{< katex >}}x,y\in G{{< /katex >}} で {{< katex >}}x\sim y,y\sim z{{< /katex >}} とすると

{{< katex display >}}
x^{-1}y,y^{-z}z\in H
{{< /katex >}}

{{< katex >}}H{{< /katex >}} は部分群なので

{{< katex display >}}
(x^{-1}y)(y^{-1}z)=x^{-1}(yy^{-1})z=x^{-1}z\in H\\
\therefore{x\sim z}
{{< /katex >}}

よって、**推移律**を満たす。

以上より関係 {{< katex >}}\sim{{< /katex >}} は同値関係である。

また、右剰余類についても同様に証明できる。
{{< /details >}}

{{< hint info >}}
**左剰余類の意味の考察**

左剰余類は {{< katex >}}a{{< /katex >}} を定数として群 {{< katex >}}G{{< /katex >}} の部分群 {{< katex >}}H{{< /katex >}} の元を左から掛けたもの。

{{< katex display >}}
\begin{aligned}
C(a)&=\{x\in G\mid a\sim x\}\\
&=\{x\in G\mid a^{-1}x\in H\}\\
&=\{ah\mid h\in H\}\\
&=aH
\end{aligned}
{{< /katex >}}
{{< /hint >}}

### 定理

- {{< katex >}}\forall a,b\in G,|aH|=|bH|{{< /katex >}}

  {{< details title="証明" >}}
  {{< katex >}}\forall a\in G,|H|=|aH|{{< /katex >}} を示せばよい。

  {{< katex display >}}
  \begin{aligned}
  f:&H&\to&\enspace aH\\
  &h&\mapsto&\enspace ah
  \end{aligned}
  {{< /katex >}}

  {{< katex >}}f{{< /katex >}} は全単射になっており、{{< katex >}}\therefore|H|=|aH|{{< /katex >}}

  {{< /details >}}

## 正規部分群

### 定義

{{< katex >}}H{{< /katex >}} を {{< katex >}}G{{< /katex >}} の部分群とする。
すべての {{< katex >}}a\in G{{< /katex >}} に対し、{{< katex >}}aH=Ha{{< /katex >}} となるとき、{{< katex >}}H{{< /katex >}} を **{{< katex >}}G{{< /katex >}} の正規部分群**といい、{{< katex >}}H\trianglelefteq G{{< /katex >}} と表す。

{{< hint info >}}
可換群 {{< katex >}}G{{< /katex >}} の部分群はすべて正規部分群。
{{< /hint >}}

{{< hint info >}}
**正規部分群の意味の考察**

{{< katex display >}}
aH\cdot bH=abH\;(a,b\in G,H\le G)
{{< /katex >}}

を満たす群 {{< katex >}}H{{< /katex >}} を考える。

この演算がwell-definedであるためには

{{< katex display >}}
aH=a'H,bH=b'H\implies abH=a'b'H
{{< /katex >}}

を満たさなければならない。

ここで {{< katex >}}a'=ah_1,b'=bh_2\\;(h_1,h_2\in H){{< /katex >}} とおくと

{{< katex display >}}
a'b'H=ah_1bh_2H
{{< /katex >}}

**もし {{< katex >}}H{{< /katex >}} が正規部分群であれば**

{{< katex display >}}
\begin{aligned}
a'b'&=abh_1'h_2\;(h_1'\in H)\\
&=abH\\
\therefore a'b'H&=abH
\end{aligned}
{{< /katex >}}

となり成立する。
{{< /hint >}}

### 正規部分群の剰余類

{{< katex >}}N{{< /katex >}} を {{< katex >}}G{{< /katex >}} の正規部分群とする。
剰余類 {{< katex >}}aN{{< /katex >}} と {{< katex >}}bN{{< /katex >}} の積を {{< katex >}}aN\cdot bN=abN{{< /katex >}} と定義すると、
{{< katex >}}G/N{{< /katex >}} はこの演算によって群となり、この群を **{{< katex >}}G{{< /katex >}} の正規部分群 {{< katex >}}N{{< /katex >}} に関する剰余類**という。

{{< details title="G/N が群であることの証明" >}}
- 演算に対して閉じていることは明らか。
- 単位元 {{< katex >}}eN{{< /katex >}} が存在。
- {{< katex >}}aN{{< /katex >}} の逆元 {{< katex >}}a^{-1}N{{< /katex >}} が存在。

よって結合律の成立を示す。

{{< katex display >}}
\begin{aligned}
(aN\cdot bN)\cdot cN&=abN\cdot cN\\
&=abcN\\
&=aN\cdot(bN\cdot cN)
\end{aligned}
{{< /katex >}}

となり、結合律が成り立つため、{{< katex >}}G/N{{< /katex >}} は群である。
{{< /details >}}

## 準同型写像

### 定義

{{< katex >}}G,G'{{< /katex >}} が群であり、かつ写像 {{< katex >}}f:G\to G'{{< /katex >}} が

{{< katex display >}}
\forall{x,y\in G},f(xy)=f(x)f(y)
{{< /katex >}}

を満たすとき {{< katex >}}f{{< /katex >}} を準同型写像という。

### 定理

- {{< katex >}}f(e)=e'{{< /katex >}} ({{< katex >}}e'{{< /katex >}} は {{< katex >}}G'{{< /katex >}} の単位元)

  {{< details title="証明" >}}
  {{< katex display >}}
  \begin{aligned}
  f(e)&=f(ee)=f(e)f(e)\\
  &=e'
  \end{aligned}
  {{< /katex >}}
  {{< /details >}}

- {{< katex >}}f(x^{-1})=f(x)^{-1}{{< /katex >}}

  {{< details title="証明" >}}
  {{< katex display >}}
  \begin{aligned}
  f(x)f(x^{-1})=f(xx^{-1})=f(e)=e'\\
  f(x^{-1})f(x)=f(x^{-1}x)=f(e)=e'
  \end{aligned}
  {{< /katex >}}

  よって

  {{< katex display >}}
  f(x^{-1})=f(x)^{-1}
  {{< /katex >}}
  {{< /details >}}

### 核と像

群の準同型写像 {{< katex >}}f{{< /katex >}} に対して

{{< katex display >}}
\begin{aligned}
\ker{f}&=\{x\in G\mid f(x)=e'\}\\
\text{im}f&=\{f(x)\in G'\mid x\in G\}
\end{aligned}
{{< /katex >}}

### 核と像の定理

- {{< katex >}}\ker{f}\trianglelefteq G{{< /katex >}}

  {{< details title="証明" >}}
  {{< katex display >}}
  \begin{aligned}
  \forall{a,b\in\ker{f}},f(a^{-1}b)&=f(a^{-1})f(b)=f(a)^{-1}f(b)=e'^{-1}e'=e'e'\\
  &=e'
  \end{aligned}
  {{< /katex >}}

  よって {{< katex >}}\ker{f}\le G{{< /katex >}}

  {{< katex display >}}
  \begin{aligned}
  \forall{a\in\ker{f}},\forall{x\in G},f(xax^{-1})&=f(x)f(a)f(x)^{-1}\\
  &=f(x)f(x)^{-1}\\
  &=e'\\
  \therefore xax^{-1}&\in\ker{f}
  \end{aligned}
  {{< /katex >}}

  よって {{< katex >}}\ker{f}\trianglelefteq G{{< /katex >}}
  {{< /details >}}

- {{< katex >}}\text{im}f\le G{{< /katex >}}

  {{< details title="証明" >}}
  {{< katex display >}}
  \forall{f(a),f(b)\in\text{im}f},f(a)^{-1}f(b)=f(a^{-1}b)\in\text{im}f
  {{< /katex >}}

  よって {{< katex >}}\text{im}f\le G{{< /katex >}}
  {{< /details >}}

## 準同型定理

{{< katex >}}f:G\to G'{{< /katex >}} を準同型写像とする。このとき

{{< katex display >}}
\begin{aligned}
\varphi:&G/\ker{f}&\to\text{im}f\\
&x\ker{f}&\mapsto f(x)
\end{aligned}
{{< /katex >}}

は同型写像である。すなわち

{{< katex display >}}
G/\ker{f}\simeq\text{im}f
{{< /katex >}}

特に {{< katex >}}f{{< /katex >}} が全射であるとき

{{< katex display >}}
G/\ker{f}\simeq{G'}
{{< /katex >}}

が成り立つ。

<!-- TODO 準同型定理の証明 -->