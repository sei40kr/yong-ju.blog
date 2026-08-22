import { promises as fs } from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import {
  estimateReadMinutes,
  extractHeadings,
  toExcerpt,
} from "~/lib/post-content";
import { type Paginated, POSTS_PER_PAGE } from "~/models/paginated";
import type { PostHeading } from "~/models/post-heading";
import type { PostData } from "~/models/post-data";

const POSTS_DIR = path.join(process.cwd(), "content", "posts");

interface PostFrontmatter {
  title: string;
  date: Date;
  tags?: string[];
}

const getPostSource = (slug: string): Promise<string> =>
  fs.readFile(path.join(POSTS_DIR, `${slug}.mdx`), "utf-8");

const byDateDesc = (a: PostData, b: PostData) =>
  b.date.getTime() - a.date.getTime();

const collectPostData = async (): Promise<PostData[]> => {
  const files = await fs.readdir(POSTS_DIR);
  const postData = await Promise.all(
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
  return postData.sort(byDateDesc);
};

let cachedPostData: Promise<PostData[]> | null = null;

// Collected once per build; development skips the cache so post edits show up.
export const getPostDataNewestFirst = (): Promise<PostData[]> =>
  process.env.NODE_ENV === "development"
    ? collectPostData()
    : (cachedPostData ??= collectPostData());

export const getPostHeadings = async (slug: string): Promise<PostHeading[]> => {
  const { content } = matter(await getPostSource(slug));
  return extractHeadings(content);
};

const paginate = <T>(
  items: T[],
  page: number,
  perPage: number,
): Paginated<T> => ({
  totalCount: items.length,
  items: items.slice((page - 1) * perPage, page * perPage),
});

export const findRecentPostData = async (
  page: number,
  perPage: number = POSTS_PER_PAGE,
): Promise<Paginated<PostData>> =>
  paginate(await getPostDataNewestFirst(), page, perPage);

export const findPostDataByTag = async (
  tag: string,
  page: number,
  perPage: number = POSTS_PER_PAGE,
): Promise<Paginated<PostData>> =>
  paginate(
    (await getPostDataNewestFirst()).filter((post) => post.tags.has(tag)),
    page,
    perPage,
  );

/** A post plus its date-order neighbors, for the prev/next links. */
export const findPostWithNeighbors = async (
  slug: string,
): Promise<{ post: PostData; newer?: PostData; older?: PostData }> => {
  const posts = await getPostDataNewestFirst();
  const index = posts.findIndex((post) => post.slug === slug);
  return {
    post: posts[index],
    newer: index > 0 ? posts[index - 1] : undefined,
    older: index < posts.length - 1 ? posts[index + 1] : undefined,
  };
};
