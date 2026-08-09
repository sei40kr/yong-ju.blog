import GithubSlugger from "github-slugger";

// Regex, not a remark AST pass: @next/mdx already parses each file once, so
// re-parsing here to read headings/prose would be a second, far slower parse
// for identical output. We strip markdown by hand and stay dependency-light.

const EXCERPT_LENGTH = 120;

/** `c_1\bold{a_1}+\cdots` → `c_1a_1+…`, so inline math still reads as text. */
const unwrapMath = (tex: string): string =>
  tex
    .replace(/\\[cl]?dots/g, "…") // \dots / \cdots / \ldots → ellipsis
    .replace(/\\[a-zA-Z]+/g, "") // other LaTeX commands
    .replace(/[{}\\]/g, ""); // braces / stray backslashes

/**
 * Opening prose of a post, flattened to plain text for the list view.
 * Headings, code blocks, display math, tables and MDX components carry no
 * summary value on their own, so they are dropped rather than inlined.
 */
export const toExcerpt = (content: string): string => {
  const prose = content
    .replace(/^```[\s\S]*?^```/gm, "") // fenced code blocks
    .replace(/^[ \t]*\$\$[\s\S]*?^[ \t]*\$\$/gm, "") // display math ($$ … $$)
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, "") // MDX comments ({/* … */})
    .replace(/^#{1,6}\s.*$/gm, "") // ATX headings
    .replace(/^\s*(?:-{3,}|\*{3,}|_{3,})\s*$/gm, "") // thematic breaks
    .replace(/^\s*\|.*$/gm, "") // table rows
    .replace(/<[^>]*>/g, "") // HTML / JSX tags
    .replace(/!\[[^\]]*\]\([^)]*\)/g, "") // images (before links: image embeds a link)
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1") // links → text
    .replace(/\$([^$\n]+)\$/g, (_, tex: string) => unwrapMath(tex)) // inline math
    .replace(/`([^`]*)`/g, "$1") // inline code
    .replace(/[*_~]/g, "") // emphasis / strikethrough markers
    .replace(/^\s*(?:[-+]|\d+\.)\s+/gm, "") // list markers
    .replace(/^\s*>\s?/gm, "") // blockquote markers
    .replace(/\s+/g, " ") // collapse whitespace
    .trim();

  return prose.length > EXCERPT_LENGTH
    ? `${prose.slice(0, EXCERPT_LENGTH)}…`
    : prose;
};

/** Rough Japanese reading speed: ~500 characters per minute. */
export const estimateReadMinutes = (content: string): number =>
  Math.max(1, Math.round(content.replace(/\s/g, "").length / 500));

export interface PostHeading {
  depth: 2 | 3;
  text: string;
  id: string;
}

/**
 * Extract h2/h3 headings for the table of contents. Ids must match what
 * rehype-slug generates at render time, so both use github-slugger.
 */
export const extractHeadings = (content: string): PostHeading[] => {
  // Strip fenced code first: a `#` line inside a code block isn't a heading.
  const withoutCodeBlocks = content.replace(/^```[\s\S]*?^```/gm, "");
  const slugger = new GithubSlugger();
  const headings: PostHeading[] = [];
  for (const line of withoutCodeBlocks.split("\n")) {
    const match = /^(#{2,3})\s+(.+?)\s*$/.exec(line); // ## or ###
    if (!match) {
      continue;
    }
    const text = match[2]
      .replace(/`([^`]*)`/g, "$1") // inline code
      .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1") // links → text
      .replace(/\*\*([^*]*)\*\*/g, "$1"); // bold markers
    headings.push({
      depth: match[1].length as 2 | 3,
      text,
      id: slugger.slug(text),
    });
  }
  return headings;
};
