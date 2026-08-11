import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Tag } from "./tag";

const meta = {
  title: "Tag/Tag",
  component: Tag,
  tags: ["autodocs"],
  args: { tag: "サンプル" },
} satisfies Meta<typeof Tag>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

/** The tag cloud and the sidebar show a post count. */
export const WithCount: Story = {
  args: { count: 12 },
};

/** The tag currently being filtered on, in the tag archive. */
export const Selected: Story = {
  args: { count: 12, selected: true },
};
