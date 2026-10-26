import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { P, withArticleBody } from "../../../.storybook/article";
import { Quiz, QuizItem } from "./quiz";

const meta = {
  title: "MDX/Quiz",
  component: Quiz,
  tags: ["autodocs"],
  decorators: [withArticleBody],
  args: {
    children: [
      <QuizItem
        key="1"
        question="表に出る問いのダミーテキスト。1 行で収まる長さ。"
      >
        <P>
          裏返したときに出てくる答えのダミーテキスト。問いより長くなっても、
          カードの高さが両面で揃うかを見る。
        </P>
      </QuizItem>,
      <QuizItem key="2" question="2 問目の問い。">
        <P>2 問目の答え。</P>
      </QuizItem>,
      <QuizItem key="3" question="3 問目の問い。">
        <P>3 問目の答え。</P>
      </QuizItem>,
    ],
  },
} satisfies Meta<typeof Quiz>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Single: Story = {
  args: {
    children: (
      <QuizItem question="1 問だけのときの問い。">
        <P>1 問だけのときの答え。</P>
      </QuizItem>
    ),
  },
};
