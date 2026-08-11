import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { SAMPLE_POSTS } from "../../../.storybook/fixtures";
import { PostList } from "./post-list";

const meta = {
  title: "PostList/PostList",
  component: PostList,
  tags: ["autodocs"],
  args: {
    heading: "最新の記事",
    totalCount: SAMPLE_POSTS.length,
    currentPage: 1,
    posts: SAMPLE_POSTS,
    basePath: "/page",
  },
} satisfies Meta<typeof PostList>;

export default meta;

type Story = StoryObj<typeof meta>;

/** One page worth of posts: no pagination. */
export const Default: Story = {};

export const Empty: Story = {
  args: { posts: [], totalCount: 0 },
};
