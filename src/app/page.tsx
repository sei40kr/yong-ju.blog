import { PostListPage } from "~/components/post-list/post-list";
import { findRecentPostInfos } from "~/repositories/post-infos";
import { getTagCounts } from "~/repositories/tags";

// The old site redirected `/` to `/page/1` (in production, a CloudFront
// function rewrites `/` to `/page/1/index.html`). Static export cannot emit
// server redirects, so render the first page directly instead.
export default async function HomePage() {
  const [paginatedPostInfos, tags] = await Promise.all([
    findRecentPostInfos(1),
    getTagCounts(),
  ]);

  return (
    <PostListPage
      totalCount={paginatedPostInfos.totalCount}
      currentPage={1}
      posts={paginatedPostInfos.items}
      basePath="/page"
      tags={tags}
    />
  );
}
