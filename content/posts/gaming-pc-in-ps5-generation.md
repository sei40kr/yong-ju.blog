---
title: "PS5 世代ゲーミング PC のパーツ構成"
date: 2020-08-05T00:15:53+09:00
tags: ["自作PC"]
---

## CPU

### PS5

- AMD Ryzen カスタムモデル (Zen2) 8C/16T 3.5GHz

### PC

- AMD Ryzen 7 3700X (Zen2) 8C/16T 3.6GHz ― **¥39,280**

---

RDNA2 ベースの AMD GPU を待つなら同じく 2020 年内発売の Zen3 ベースの AMD CPU も待ったほうがいいだろう。
Zen2 と比べ 50% の電力性能比の向上を公表している。

Ryzen 7 3700X は PS5 と比べ若干クロックが速いが、OS のオーバーヘッドは確実に PC の方が大きいため、ゲームに同等の演算リソースを確保するにはもう少し性能が欲しいところだ。

- [Ryzen - Wikipedia](https://ja.wikipedia.org/wiki/Ryzen)
- [ASCII.jp：AMD、Zen 3 の CPU を 10 月 8 日に RDNA 2 の GPU を 10 月 28 日に発表予定](https://ascii.jp/elem/000/004/026/4026524/)

## GPU

### PS5

- AMD カスタムモデル (RDNA2) 10.28TFlOps

### PC

- AMD Radeon RX 5700XT (RDNA) GDDR6 8GB IO: 448GB/s 9.75TFlOps ― **¥43,978**
- NVIDIA GeForce RTX 2080 GDDR6 8GB IO: 448GB/s 10TFlOps

---

- [AMD Radeon - Wikipedia](https://ja.wikipedia.org/wiki/AMD_Radeon)
- [NVIDIA GeForce - Wikipedia](https://ja.wikipedia.org/wiki/NVIDIA_GeForce)

### グラフィックメモリのトラウマ

PS4 が発売された当時、PC 向けグラフィックカードに搭載されているメモリはミドルクラスで 2GB, アッパーミドルクラスで 4GB 程度だった。
PS4 に搭載されていた GPU はミドルクラス相当だが、メモリはシステムと共有で 8GB と、システムで使うメモリ空間とグラフィック演算で使うメモリ空間が共有されていた。

PS4 世代後半に差し掛かると 4GB 以上のグラフィックスメモリを推奨する PC ゲームが増えた。
多くのゲームエンジンが PS4 のグラフィックメモリ容量を有効活用する方向にシフトしたのだ。(主に U○i とか)

また自分が購入した GDDR5 4GB 搭載を謳う GTX 970 は、実際には GDDR5 3.5GB + DDR3 0.5GB 構成であることが発覚した。
この頃 AMD は「AMD Radeon の 4GB は 4GB に相当します!」と Twitter で煽っていた。

![4GB MEANS 4GB](/img/4gb-means-4gb.jpg)

- [Playstation 4 - Wikipedia](https://ja.wikipedia.org/wiki/PlayStation_4)
- [AMD is rubbing salt on NVIDIA's wound: Our 4Gb means 4Gb - Tech4Gamers](https://tech4gamers.com/amd-rubbing-salt-nvidias-wound-4gb-means-4gb/)

結果として **PS4 の 2 倍以上の演算性能を誇る GTX 970 でも PS4 よりローグラフィック, Low FPS で頻繁なスラッシングを発生させるゲームが登場し始めた。**

### レイトレーシング

次世代の GPU はレイトレーシングと呼ばれる処理をハードウェアレベルでサポートする。
これは光源の伝播をシミュレートする技術である。

{{< youtube WoQr0k2IA9A >}}

PS4 時代にも水面やガラス、鏡など一部のマテリアルには光源の反射表現が用いられてきた。特に光の反射は PS4 ならではの高いテクスチャ解像度を強調するのにうってつけであり、個人的には

- やたらと雨のシーンが多い
- ずっと晴天なのに地面にいつまでも蒸散しない水溜まりがある

というようなケースが PS4 のゲームには多かったような気がする。
また実際に光源の伝播をシミュレートするのではなく、別のカメラから描画したワールドを表面に薄く描画する、というのがメインであり、複雑な反射は表現できなかった。

それ以前のゲームでは表面に写るワールドを決め打ちでプリレンダしていた。その結果、ビルのない平原で車のガラスに高層ビルが写ったり、反射表現を向上させる MOD を解析してみると作者と思しき人の顔画像をグレースケール化したものを薄く描画してるだけだと発覚したこともあった。

レイトレーシングでは素材の平滑率から光源の反射表現を適用する部分を特定し、そこに写る光源を逆算する。
この計算をハードウェアで高速化するのがレイトレーシング専用チップだ。

上記で上げた AMD RX 5700 XT のベースになっている RDNA にはこのレイトレーシング専用チップがない。
**ハードウェアレベルのレイトレーシングに対応した RDNA2 ベースの AMD GPU は 2020 年内発売となっているので、こちらを待ったほうが良さそうだ。**

- [レイトレーシング - Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%AC%E3%82%A4%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%B3%E3%82%B0)
- [環境マッピング - Wikipedia](https://ja.wikipedia.org/wiki/%E7%92%B0%E5%A2%83%E3%83%9E%E3%83%83%E3%83%94%E3%83%B3%E3%82%B0)

## メモリ

### PS5

- GDDR6 16GB IO: 448GB/s

### PC

- DDR4 3200MHz IO: 25.6GB/s

---

DDR4 3200MHz は上記 Ryzen 7 3700X が対応する中で最速のメモリ規格。
これでも IO 性能差では GDDR6 をシステムメモリにも採用している PS5 ともはや勝負になっていない。
8GBx2 デュアルチャネル構成でメモリインターリーブの恩恵を受けたとしても実に 8 倍以上の性能差がある。

Zen2 の次, Zen3 が DDR4 を採用する最後のアーキテクチャである。
つまり 2021 年の Zen4 まで待てばシステムメモリに DDR5 を使えるというわけだ。
DDR5 は DDR4 より 85% 高速化するという噂だが、それでも PS5 とは 4 倍以上の IO 性能差が残る。

システムメモリとグラフィックメモリの IO 性能でなぜこれほどの差があるのか。
自分はメモリチップ配置の自由度が影響していると考える。

高性能を実現する GDDR6 では電気が伝わる速度ですらネックになる。
様々なフォームファクタをもつ PC のマザーボード上ではメモリとそれを利用する CPU までの距離も様々だ。
このような条件下でメモリチップの IO を高速化したとしてもメモリチップを跨ぐアクセスを同期するのにかえって時間がかかってしまうのではないだろうか。

グラフィックカードに搭載されている GDDR6 メモリチップはそれを利用する GPU を囲むように配置され、GPU から各メモリチップまでの距離が最短かつ均等になるよう設計されている。
PS5 のようなコンシューマハードウェアも CPU やメモリをプラグインにする必要がないためメモリチップの配置を自由に決めることができる。

もしこれが本当だとすればこの差は数年では埋まらないだろう。

- [DDR4 SDRAM - Wikipedia](https://ja.wikipedia.org/wiki/DDR4_SDRAM)
- [DDR5 SDRAM - Wikipedia](https://ja.wikipedia.org/wiki/DDR5_SDRAM)
- [メモリインターリーブ - Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%A1%E3%83%A2%E3%83%AA%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%AA%E3%83%BC%E3%83%96)

## ストレージ

### PS5

- 825GB PCIe Gen4 SSD read: 8 〜 9GB/s (圧縮時)

### PC

- PCIe Gen4 SSD read: 5GB/s ― 1TB ¥24,000

---

PCIe Gen4 対応の PC 向け SSD が市販され始め read 性能も PCIe Gen4 の高速化に合わせて 2 倍になっている。

[PCI Express - Wikipedia](https://ja.wikipedia.org/wiki/PCI_Express)

しかし PS5 のようなハードウェアベースの圧縮処理専用チップを搭載するチップセットが市販される可能性は低いと考えている。

2020/09/26 追記: DirectX 12 に DirectStorage というストレージ API が組み込まれることになった。
これは PS5 のような専用チップで SSD ストレージの実効 I/O 速度を高速化するものではなく、ストレージ上に存在するゲームデータの解凍に GPU のリソースを使えるようになるというもの。

[DirectStorage is coming to PC | DirectX Developer Blog](https://devblogs.microsoft.com/directx/directstorage-is-coming-to-pc/)

PS5 の圧縮時の read 性能 8 〜 9GB/s を達成するには 2 台の PCIe Gen4 対応 SSD でストライピング構成を取る方法がある。
理論上 read 性能は 1 台構成と比べ 2 倍になる。あくまで理論値であるため、これで PS5 のハードウェアベースの圧縮に対抗できるかどうかは不明。

PS5 のリードアーキテクト、マーク・サーニー氏はこのストレージの SSD の転送速度がローディング時間のみならずゲームプレイをも変える可能性をもっていることを示唆している。
これはゲームデータのローディングが次のシーケンスで必要なデータをすべてメモリ上に配置するオーバーレイ方式から、次の数秒で必要になりうるデータをリアルタイムにメモリ上に配置する方式に変わり、今までにないゲーム体験を創造することが可能になるという解釈をすることにした。

{{< youtube ph8LyNIT9sg >}}

## その他

[Playstation 5 - Wikipedia](https://ja.wikipedia.org/wiki/PlayStation_5)
