import { promises as fs } from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import {
  estimateReadMinutes,
  extractHeadings,
  type PostHeading,
  toExcerpt,
} from "~/lib/post-content";
import type { Paginated } from "~/models/paginated";
import type { PostInfo } from "~/models/post-info";

export type { PostHeading };

const POSTS_DIR = path.join(process.cwd(), "content", "posts");

interface PostFrontmatter {
  title: string;
  date: Date;
  tags?: string[];
}

const getPostSource = (slug: string): Promise<string> =>
  fs.readFile(path.join(POSTS_DIR, `${slug}.mdx`), "utf-8");

const collectPostInfos = async (): Promise<PostInfo[]> => {
  const files = await fs.readdir(POSTS_DIR);
  return Promise.all(
    files
      .filter((file) => file.endsWith(".mdx"))
      .map(async (file) => {
        const slug = file.replace(/\.mdx$/, "");
        const { data, content } = matter(await getPostSource(slug));
        const frontmatter = data as PostFrontmatter;

        if (Number.isNaN(frontmatter.date.getTime())) {
          throw new Error(`Invalid date in post ${slug}`);
        }

        return {
          slug,
          title: frontmatter.title,
          date: frontmatter.date,
          tags: new Set(frontmatter.tags ?? []),
          excerpt: toExcerpt(content),
          readMinutes: estimateReadMinutes(content),
        };
      }),
  );
};

let cachedPostInfos: Promise<PostInfo[]> | null = null;

// Built once per build; development skips the cache so post edits show up.
export const getPostInfos = (): Promise<PostInfo[]> =>
  process.env.NODE_ENV === "development"
    ? collectPostInfos()
    : (cachedPostInfos ??= collectPostInfos());

export const getPostHeadings = async (slug: string): Promise<PostHeading[]> => {
  const { content } = matter(await getPostSource(slug));
  return extractHeadings(content);
};

const byDateDesc = (a: PostInfo, b: PostInfo) =>
  b.date.getTime() - a.date.getTime();

const paginate = <T>(
  items: T[],
  offset: number,
  count: number,
): Paginated<T> => ({
  totalCount: items.length,
  items: items.slice(offset, offset + count),
});

export const findRecentPostInfos = async (
  offset: number,
  count: number,
): Promise<Paginated<PostInfo>> =>
  paginate([...(await getPostInfos())].sort(byDateDesc), offset, count);

export const findPostInfosByTag = async (
  tag: string,
  offset: number,
  count: number,
): Promise<Paginated<PostInfo>> =>
  paginate(
    (await getPostInfos())
      .filter((post) => post.tags.has(tag))
      .sort(byDateDesc),
    offset,
    count,
  );
