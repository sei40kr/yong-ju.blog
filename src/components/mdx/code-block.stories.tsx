import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { withArticleBody } from "../../../.storybook/article";
import { CodeBlock } from "./code-block";

const meta = {
  title: "MDX/CodeBlock",
  component: CodeBlock,
  tags: ["autodocs"],
  decorators: [withArticleBody],
} satisfies Meta<typeof CodeBlock>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Nix: Story = {
  args: {
    language: "nix",
    code: `{ pkgs, ... }:
{
  packages = with pkgs; [ hello ];
  program.enable = true;
}`,
  },
};

export const Bash: Story = {
  args: {
    language: "bash",
    code: `# comment
echo "hello" | tr a-z A-Z`,
  },
};

export const Sql: Story = {
  args: {
    language: "sql",
    code: `select name, count(*) as total
from sample
group by name
order by total desc
limit 10;`,
  },
};

/** A fence with no language: no highlighting, same frame. */
export const NoLanguage: Story = {
  args: {
    code: `$ command --flag
output line`,
  },
};
