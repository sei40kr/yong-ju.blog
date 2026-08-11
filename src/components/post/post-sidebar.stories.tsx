import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { SAMPLE_HEADINGS } from "../../../.storybook/fixtures";
import { PostSidebar } from "./post-sidebar";

const meta = {
  title: "Post/PostSidebar",
  component: PostSidebar,
  tags: ["autodocs"],
  args: {
    slug: "sample-post",
    title: "サンプル記事のタイトル",
    headings: SAMPLE_HEADINGS,
    activeHeadingId: "heading-2",
  },
} satisfies Meta<typeof PostSidebar>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

/** A post with no headings drops the table of contents entirely. */
export const WithoutToc: Story = {
  name: "Without TOC",
  args: { headings: [] },
};
