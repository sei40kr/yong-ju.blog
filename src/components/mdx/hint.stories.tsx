import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { P, withArticleBody } from "../../../.storybook/article";
import { Hint } from "./hint";

const meta = {
  title: "MDX/Hint",
  component: Hint,
  tags: ["autodocs"],
  decorators: [withArticleBody],
  args: {
    children: <P>本文中の補足に使う。1 段落だけのいちばん短いかたち。</P>,
  },
} satisfies Meta<typeof Hint>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Info: Story = {
  args: { level: "info" },
};

export const Warn: Story = {
  args: { level: "warn" },
};

export const Danger: Story = {
  args: { level: "danger" },
};

/** MDX allows several paragraphs inside, so check the gap between them. */
export const MultipleParagraphs: Story = {
  args: {
    level: "info",
    children: (
      <>
        <P>1 段落目のダミーテキスト。</P>
        <P>
          2 段落目のダミーテキスト。段落間の余白と、最後の段落の下が詰まることを
          確認する。
        </P>
      </>
    ),
  },
};
