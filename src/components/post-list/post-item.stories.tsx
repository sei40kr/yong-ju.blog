import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { SAMPLE_POSTS } from "../../../.storybook/fixtures";
import { PostItem } from "./post-item";

const meta = {
  title: "PostList/PostItem",
  component: PostItem,
  tags: ["autodocs"],
  args: { post: SAMPLE_POSTS[0] },
} satisfies Meta<typeof PostItem>;

export default meta;

type Story = StoryObj<typeof meta>;

/** Only the first two tags are shown. */
export const Default: Story = {};

/** Without tags the metadata moves to the left. */
export const WithoutTags: Story = {
  args: { post: SAMPLE_POSTS[2] },
};

/** The excerpt clamps to two lines. */
export const LongTitleAndExcerpt: Story = {
  args: {
    post: {
      ...SAMPLE_POSTS[1],
      title:
        "折り返しを確認するための、必要以上に長いサンプル記事のタイトルの例",
      excerpt: SAMPLE_POSTS[1].excerpt.repeat(3),
    },
  },
};
