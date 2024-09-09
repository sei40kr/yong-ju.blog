import matter from "gray-matter";
import type { Page } from "~/models/page";
import type { PostInfo } from "~/models/post-info";

export const getPostInfos = (): Promise<PostInfo[]> =>
  Promise.all(
    Object.entries(
      import.meta.glob("/src/routes/posts/*/index.mdx", {
        query: "?raw",
        import: "default",
      }),
    ).map(async ([path, getContent]) => {
      const id = path.replace(/^\/src\/routes\/posts\/(.+)\/index.mdx$/, "$1");
      const frontmatter = matter((await getContent()) as string).data as {
        title: string;
        date: Date;
        categories?: string[];
        tags?: string[];
      };

      if (Number.isNaN(frontmatter.date.getTime())) {
        throw new Error(`Invalid date in post ${id}`);
      }

      const categories = frontmatter.categories
        ? new Set(frontmatter.categories)
        : (new Set() as Set<string>);
      const tags = frontmatter.tags
        ? new Set(frontmatter.tags)
        : (new Set() as Set<string>);

      return {
        id,
        title: frontmatter.title,
        date: frontmatter.date,
        categories,
        tags,
      };
    }),
  );

export const findRecentPostInfos = (
  offset: number,
  count: number,
): Promise<Page<PostInfo>> =>
  getPostInfos().then((posts) => ({
    totalCount: posts.length,
    items: posts
      .sort((a, b) => b.date.getTime() - a.date.getTime())
      .slice(offset, offset + count),
  }));

export const findPostInfosByCategory = (
  category: string,
  offset: number,
  count: number,
): Promise<Page<PostInfo>> =>
  getPostInfos().then((posts) => {
    const filteredPosts = posts.filter((post) => post.categories.has(category));
    return {
      totalCount: filteredPosts.length,
      items: filteredPosts.slice(offset, offset + count),
    };
  });

export const findPostsInfoByTag = (
  tag: string,
  offset: number,
  count: number,
): Promise<Page<PostInfo>> =>
  getPostInfos().then((posts) => {
    const filteredPosts = posts.filter((post) => post.tags.has(tag));
    return {
      totalCount: filteredPosts.length,
      items: filteredPosts.slice(offset, offset + count),
    };
  });
