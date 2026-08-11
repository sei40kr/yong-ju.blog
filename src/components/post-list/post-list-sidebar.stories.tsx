import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { SAMPLE_TAGS } from "../../../.storybook/fixtures";
import { PostListSidebar } from "./post-list-sidebar";

const meta = {
  title: "PostList/PostListSidebar",
  component: PostListSidebar,
  tags: ["autodocs"],
  args: { tags: SAMPLE_TAGS },
} satisfies Meta<typeof PostListSidebar>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};
