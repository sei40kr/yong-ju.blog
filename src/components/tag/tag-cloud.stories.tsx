import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { SAMPLE_TAGS } from "../../../.storybook/fixtures";
import { TagCloud } from "./tag-cloud";

const meta = {
  title: "Tag/TagCloud",
  component: TagCloud,
  tags: ["autodocs"],
  args: { tags: SAMPLE_TAGS },
} satisfies Meta<typeof TagCloud>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithCurrentTag: Story = {
  args: { currentTag: "ダミー" },
};

export const Empty: Story = {
  args: { tags: new Map() },
};
