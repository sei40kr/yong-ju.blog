import type { PostData } from "~/models/post-data";
import type { PostHeading } from "~/models/post-heading";

/**
 * Sample data for the stories. It deliberately does not mirror anything in
 * content/: a story should show how a given shape of data is typeset, not how
 * one particular post happens to look, and editing a post must not change what
 * the stories render.
 *
 * What varies here is only what the components react to — Japanese/Latin mix,
 * tagged vs untagged, and length. Dates are absolute so `humanizeDate` prints
 * the same string on every run.
 */
export const SAMPLE_POSTS: PostData[] = [
  {
    slug: "sample-post",
    title: "サンプル記事のタイトル",
    date: new Date("2024-02-11T22:01:36+09:00"),
    tags: new Set(["サンプル", "ダミー", "Placeholder"]),
    excerpt:
      "本文の書き出しから抜粋が作られる。日本語と Latin script が混ざったときの字面と行間、それに 2 行でクランプされたときの収まりを確認するためのダミーテキストです。",
    readMinutes: 8,
  },
  {
    slug: "sample-post-2",
    title: "少し長めのサンプル記事のタイトル",
    date: new Date("2023-11-03T10:20:00+09:00"),
    tags: new Set(["サンプル", "長めのタグ名"]),
    excerpt:
      "2 件目のダミー記事。タグが 2 つ、日付は 1 件目より古い。抜粋はここでは 1 行に収まる長さにしてある。",
    readMinutes: 14,
  },
  {
    slug: "sample-post-untagged",
    title: "タグのないサンプル記事",
    date: new Date("2023-08-19T09:00:00+09:00"),
    tags: new Set(),
    excerpt:
      "タグを持たない記事。メタ情報の行が左に寄り、タグ分の gap が消えることを確認する。",
    readMinutes: 5,
  },
];

/** Mixed tag widths, to show wrapping and the count badge. */
export const SAMPLE_TAGS = new Map<string, number>([
  ["サンプル", 24],
  ["ダミー", 18],
  ["Placeholder", 12],
  ["長めのタグ名サンプル", 9],
  ["テスト", 7],
  ["Lorem", 6],
  ["日本語タグ", 4],
  ["ABC", 3],
]);

/** h2 and h3 mixed, for the table of contents' indent and active state. */
export const SAMPLE_HEADINGS: PostHeading[] = [
  { depth: 2, text: "はじめの見出し", id: "heading-1" },
  { depth: 2, text: "次の見出し", id: "heading-2" },
  { depth: 3, text: "サブ見出し", id: "heading-2-1" },
  { depth: 3, text: "少し長いサブ見出しの例", id: "heading-2-2" },
  { depth: 2, text: "Latin Heading", id: "heading-3" },
];
