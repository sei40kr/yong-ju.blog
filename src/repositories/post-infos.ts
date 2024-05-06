import matter from "gray-matter";
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
        date: string;
        tags?: string[];
      };

      const date = new Date(frontmatter.date);
      if (Number.isNaN(date.getTime())) {
        throw new Error(`Invalid date in post ${id}`);
      }

      const tags = frontmatter.tags
        ? new Set(frontmatter.tags)
        : (new Set() as Set<string>);

      return {
        id,
        title: frontmatter.title,
        date,
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
