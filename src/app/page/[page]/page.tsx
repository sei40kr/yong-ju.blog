import { PostListPage } from "~/components/post-list/post-list";
import { POSTS_PER_PAGE } from "~/models/paginated";
import { findRecentPostData, getPostDataNewestFirst } from "~/repositories/post-data";
import { getTagCounts } from "~/repositories/tags";

export const dynamicParams = false;

export async function generateStaticParams() {
  const postData = await getPostDataNewestFirst();
  const totalPages = Math.ceil(postData.length / POSTS_PER_PAGE);
  return Array.from({ length: totalPages }, (_, i) => ({ page: `${i + 1}` }));
}

export default async function RecentPostsPage({
  params,
}: {
  params: Promise<{ page: string }>;
}) {
  const currentPage = Number.parseInt((await params).page);

  const [paginatedPostData, tags] = await Promise.all([
    findRecentPostData(currentPage),
    getTagCounts(),
  ]);

  return (
    <PostListPage
      totalCount={paginatedPostData.totalCount}
      currentPage={currentPage}
      posts={paginatedPostData.items}
      basePath="/page"
      tags={tags}
    />
  );
}
