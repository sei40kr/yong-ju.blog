import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { withArticleBody } from "../../../.storybook/article";
import { Mermaid } from "./mermaid";

const meta = {
  title: "MDX/Mermaid",
  component: Mermaid,
  tags: ["autodocs"],
  decorators: [withArticleBody],
} satisfies Meta<typeof Mermaid>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Flowchart: Story = {
  args: {
    code: `flowchart TD
  A[記事を書く] --> B{ビルドは通る?}
  B -- はい --> C[main にマージ]
  B -- いいえ --> D[型エラーを直す]
  D --> B
  C --> E[S3 に同期]`,
  },
};

export const Sequence: Story = {
  args: {
    code: `sequenceDiagram
  participant B as ブラウザ
  participant CF as CloudFront
  participant S3
  B->>CF: GET /posts/nixos/
  CF->>CF: url-rewrite.js
  CF->>S3: GET /posts/nixos/index.html
  S3-->>B: 200 OK`,
  },
};

/** 記事幅より広い図は縮小されて収まる（横スクロールにはしない）。 */
export const Wide: Story = {
  args: {
    code: `flowchart LR
  A[取得] --> B[パース] --> C[抜粋の生成] --> D[目次の抽出] --> E[レンダリング] --> F[静的エクスポート]`,
  },
};

/** 構文エラーは記事を落とさず、その場にエラーとして出る。 */
export const SyntaxError: Story = {
  args: {
    code: `flowchart TD
  A[開き括弧だけ --> B`,
  },
};
