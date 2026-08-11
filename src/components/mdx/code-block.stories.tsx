import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { highlight } from "~/lib/shiki";
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

// Mirrors what the `pre` mapper in src/mdx-components.tsx feeds the component.
const fence = (code: string, language?: string): Story => ({
  args: { code, highlighted: highlight(code, language) },
});

export const Nix = fence(
  `{ pkgs, ... }:
{
  packages = with pkgs; [ hello ];
  program.enable = true;
}`,
  "nix",
);

export const Bash = fence(
  `# comment
echo "hello" | tr a-z A-Z`,
  "bash",
);

export const Sql = fence(
  `select name, count(*) as total
from sample
group by name
order by total desc
limit 10;`,
  "sql",
);

/** A fence with no language: no highlighting, same frame. */
export const NoLanguage = fence(`$ command --flag
output line`);
