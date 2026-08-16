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

const byDateDesc = (a: PostInfo, b: PostInfo) =>
  b.date.getTime() - a.date.getTime();

const collectPostInfos = async (): Promise<PostInfo[]> => {
  const files = await fs.readdir(POSTS_DIR);
  const postInfos = await Promise.all(
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
  return postInfos.sort(byDateDesc);
};

let cachedPostInfos: Promise<PostInfo[]> | null = null;

// Collected once per build; development skips the cache so post edits show up.
export const getPostInfosNewestFirst = (): Promise<PostInfo[]> =>
  process.env.NODE_ENV === "development"
    ? collectPostInfos()
    : (cachedPostInfos ??= collectPostInfos());

export const getPostHeadings = async (slug: string): Promise<PostHeading[]> => {
  const { content } = matter(await getPostSource(slug));
  return extractHeadings(content);
};

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
  paginate(await getPostInfosNewestFirst(), offset, count);

export const findPostInfosByTag = async (
  tag: string,
  offset: number,
  count: number,
): Promise<Paginated<PostInfo>> =>
  paginate(
    (await getPostInfosNewestFirst()).filter((post) => post.tags.has(tag)),
    offset,
    count,
  );

/** A post plus its date-order neighbors, for the prev/next links. */
export const findPostWithNeighbors = async (
  slug: string,
): Promise<{ post: PostInfo; newer?: PostInfo; older?: PostInfo }> => {
  const posts = await getPostInfosNewestFirst();
  const index = posts.findIndex((post) => post.slug === slug);
  return {
    post: posts[index],
    newer: index > 0 ? posts[index - 1] : undefined,
    older: index < posts.length - 1 ? posts[index + 1] : undefined,
  };
};
