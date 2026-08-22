import { PostListPage } from "~/components/post-list/post-list";
import { findRecentPostData } from "~/repositories/post-data";
import { getTagCounts } from "~/repositories/tags";

// The old site redirected `/` to `/page/1` (in production, a CloudFront
// function rewrites `/` to `/page/1/index.html`). Static export cannot emit
// server redirects, so render the first page directly instead.
export default async function HomePage() {
  const [paginatedPostData, tags] = await Promise.all([
    findRecentPostData(1),
    getTagCounts(),
  ]);

  return (
    <PostListPage
      totalCount={paginatedPostData.totalCount}
      currentPage={1}
      posts={paginatedPostData.items}
      basePath="/page"
      tags={tags}
    />
  );
}
