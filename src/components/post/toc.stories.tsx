import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { SAMPLE_HEADINGS } from "../../../.storybook/fixtures";
import { Toc } from "./toc";

const meta = {
  title: "Post/Toc",
  component: Toc,
  tags: ["autodocs"],
  args: { headings: SAMPLE_HEADINGS, activeHeadingId: null },
} satisfies Meta<typeof Toc>;

export default meta;

type Story = StoryObj<typeof meta>;

/** Top of the post: no heading is in view yet. */
export const Default: Story = {};

export const ActiveHeading: Story = {
  args: { activeHeadingId: "heading-2" },
};

/** An active h3 — check the indent against the left rule. */
export const ActiveSubHeading: Story = {
  args: { activeHeadingId: "heading-2-1" },
};
