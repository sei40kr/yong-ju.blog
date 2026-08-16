import { PostListPage } from "~/components/post-list/post-list";
import { POSTS_PER_PAGE } from "~/models/paginated";
import { findRecentPostInfos, getPostInfosNewestFirst } from "~/repositories/post-infos";
import { getTagCounts } from "~/repositories/tags";

export const dynamicParams = false;

export async function generateStaticParams() {
  const postInfos = await getPostInfosNewestFirst();
  const totalPages = Math.ceil(postInfos.length / POSTS_PER_PAGE);
  return Array.from({ length: totalPages }, (_, i) => ({ page: `${i + 1}` }));
}

export default async function RecentPostsPage({
  params,
}: {
  params: Promise<{ page: string }>;
}) {
  const currentPage = Number.parseInt((await params).page);

  const [paginatedPostInfos, tags] = await Promise.all([
    findRecentPostInfos((currentPage - 1) * POSTS_PER_PAGE, POSTS_PER_PAGE),
    getTagCounts(),
  ]);

  return (
    <PostListPage
      totalCount={paginatedPostInfos.totalCount}
      currentPage={currentPage}
      posts={paginatedPostInfos.items}
      basePath="/page"
      tags={tags}
    />
  );
}
