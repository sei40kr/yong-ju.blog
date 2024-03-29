---
title: "強化学習"
date: 2022-04-29T03:04:10+09:00
categories: ["機械学習"]
tags: ["強化学習", "機械学習", "数学", "勉強ノート", "WIP"]
---

<!-- TODO エピソードタスクと連続タスク -->

## 方策

エージェントがどのように行動を決めるかを表したものを**方策 (policy)** という。
現在の状態 {{< katex >}}s{{< /katex >}} のみによって行動 {{< katex >}}a{{< /katex >}} が決まるような、確率に依らない方策を**決定論的 (deterministic) な方策**といい、これを定式化すると以下のようになる。

{{< katex display >}}
s'=\mu(s)
{{< /katex >}}

一方、決定論的でない (確率に依る) 方策を**確率的な方策**といい、方策 {{< katex >}}\pi{{< /katex >}} が状態 {{< katex >}}s{{< /katex >}} から行動 {{< katex >}}a{{< /katex >}} を選ぶ確率を {{< katex >}}\pi(a\mid s){{< /katex >}} で表す。

<!-- TODO 探索と活用の説明 -->

## 状態遷移確率

**状態遷移確率 (state transition probability)** は状態 {{< katex >}}s{{< /katex >}} から行動 {{< katex >}}a{{< /katex >}} を選択したとき、状態 {{< katex >}}s'{{< /katex >}} に遷移する確率であり、{{< katex >}}p(s'\mid s,a){{< /katex >}} で表す。

{{< hint info >}}
状態遷移確率は現実問題における**不確実 (あるいは計算が難しい) な挙動**を表すのに用いられる。
例えば、ロボットを移動させる際の床の摩擦やモーターの故障などが挙げられる。
{{< /hint >}}

{{< hint info >}}
方策 {{< katex >}}\pi{{< /katex >}} によって状態 {{< katex >}}s{{< /katex >}} から次の状態 {{< katex >}}s'{{< /katex >}} に状態遷移する確率は以下のように表せる。

{{< katex display >}}
\sum_a\pi(a\mid s)p(s'\mid s,a)
{{< /katex >}}
{{< /hint >}}

## マルコフ決定過程

状態遷移において、今の状態 {{< katex >}}s{{< /katex >}} と行動 {{< katex >}}a{{< /katex >}} のみによって次の状態が一意に決まる性質を**マルコフ性**という。
また、マルコフ性をもつ過程を**マルコフ決定過程** (Markov Decision Process, 以下MDP) という。

マルコフ性を定式化すると以下のようになる。

{{< katex display >}}
s'=f(s,a)
{{< /katex >}}

## 報酬関数

**報酬関数 (reward function)** は状態 {{< katex >}}s{{< /katex >}} から行動 {{< katex >}}a{{< /katex >}} を選択し状態 {{< katex >}}s'{{< /katex >}} に遷移したときに得られる報酬であり、{{< katex >}}r(s',a,s){{< /katex >}} で表す。

## 収益

**収益 (return)** は時刻 {{< katex >}}t{{< /katex >}} から得る報酬の和であり、{{< katex >}}G_t{{< /katex >}} で表す。

ただし、終わりがないタスク (連続タスク) において収益は無限大に発散しうるため、将来の報酬に**割引率** {{< katex >}}\gamma\;(\gamma<1){{< /katex >}} を乗算することで、収益が発散することを防ぐ。

{{< katex display >}}
\begin{aligned}
G_t&=R_t+\gamma R_{t+1}+\gamma R_{t+2}+\cdots\\
&=R_t+\gamma G_{t+1}
\end{aligned}
{{< /katex >}}

## 状態価値関数

**状態価値関数 (state value function)** (あるいは単に**価値関数**とも) は、状態 {{< katex >}}s{{< /katex >}} から方策 {{< katex >}}\pi{{< /katex >}} に従って行動したときの収益の期待値であり、{{< katex >}}v_\pi(s){{< /katex >}} で表す。

{{< katex display >}}
v_\pi(s)=E_\pi[G_t\mid S_t=s]
{{< /katex >}}

### 状態価値関数のベルマン方程式

**ベルマン方程式 (Bellman Equation)** は、MDPにおいて成立する、状態価値関数を求める上で重要な方程式である。

{{< katex display >}}
v_\pi(s)=\sum_{a,s'}\pi(a\mid s)p(s'\mid s,a)\{r(s,a,s')+\gamma v_\pi(s')\}
{{< /katex >}}

{{< details title="導出" >}}
{{< katex display >}}
\begin{aligned}
v_\pi(s)&=E_\pi[G_t\mid S_t=s]\\
&=E_\pi[R_t+\gamma G_{t+1}\mid S_t=s]\\
&=E_\pi[R_t\mid S_t=s]+\gamma E_\pi[G_{t+1}\mid S_t=s]
\end{aligned}
{{< /katex >}}

ここで

{{< katex display >}}
\begin{aligned}
E_\pi[R_t\mid S_t=s]&=\sum_{a,s'}\pi(a\mid s)p(s'\mid s,a)r(s,a,s')\\
E_\pi[G_{t+1}\mid S_t=s]&=\sum_{a,s'}\pi(a\mid s)p(s'\mid s,a)E_\pi[G_{t+1}\mid S_{t+1}=s']
\end{aligned}
{{< /katex >}}

より

{{< katex display >}}
v_\pi(s)=\sum_{a,s'}\pi(a\mid s)p(s'\mid s,a)\{r(s,a,s')+\gamma v_\pi(s')\}
{{< /katex >}}
{{< /details >}}

### 状態価値関数のベルマン最適方程式

すべての状態において状態価値関数が最大となるような方策 {{< katex >}}\pi_*{{< /katex >}} を**最大方策**という。
また、最適方策 {{< katex >}}\pi_*{{< /katex >}} に従って行動したときの状態価値関数を {{< katex >}}v_*{{< /katex >}} で表す。

このとき {{< katex >}}v_*{{< /katex >}} について成り立つベルマン方程式を**ベルマン最適方程式 (Bellman Optimality Equation)** といい、次のように表せる。

{{< katex display >}}
v_*(s)=\sum_{a,s'}\pi_*(a\mid s)p(s'\mid s,a)\{r(s,a,s')+\gamma v_*(s')\}
{{< /katex >}}

## 行動価値関数/Q関数

**行動価値関数 (action value function)** は、状態 {{< katex >}}s{{< /katex >}} から行動 {{< katex >}}a{{< /katex >}} を選択し、その後は方策 {{< katex >}}\pi{{< /katex >}} に従って行動したときの収益の期待値であり、{{< katex >}}q_\pi(s){{< /katex >}} で表す。

{{< katex display >}}
\begin{aligned}
q_\pi(s,a)&=E_\pi[G_t\mid S_t=s,A_t=a]\\
&=E_\pi[R_t+\gamma G_{t+1}\mid S_t=s,A_t=a]
\end{aligned}
{{< /katex >}}

行動価値関数は慣習的に**Q関数**と呼ばれ、本記事でも以下Q関数と呼ぶ。

{{< hint info >}}
Q関数は状態価値関数に対して行動 {{< katex >}}a{{< /katex >}} を設定したものである。

状態価値関数 {{< katex >}}v_\pi(s){{< /katex >}} はQ関数 {{< katex >}}q_\pi(s,a){{< /katex >}} を用いて次のように表せる。

{{< katex display >}}
v_\pi(s)=\sum_a\pi(a\mid s)q_\pi(s,a)
{{< /katex >}}
{{< /hint >}}

### Q関数のベルマン方程式

{{< katex display >}}
q_\pi(s,a)=\sum_{s'}p(s'\mid s,a)\left\{r(s,a,s')+\gamma\sum_{a'}\pi(a'\mid s')q_{\pi}(s',a')\right\}
{{< /katex >}}

### Q関数のベルマン最適方程式

{{< katex display >}}
q_\pi(s,a)=\sum_{s'}p(s'\mid s,a)\left\{r(s,a,s')+\gamma\max_{a'}q_\pi(s',a')\right\}
{{< /katex >}}
