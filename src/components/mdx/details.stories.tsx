import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { P, withArticleBody } from "../../../.storybook/article";
import { Details } from "./details";

const meta = {
  title: "MDX/Details",
  component: Details,
  tags: ["autodocs"],
  decorators: [withArticleBody],
  args: {
    title: "折りたたみの見出し",
    children: (
      <P>
        開いたときに出てくる本文のダミーテキスト。閉じた状態からの高さの変化と、
        本文まわりの余白を見る。
      </P>
    ),
  },
} satisfies Meta<typeof Details>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};
