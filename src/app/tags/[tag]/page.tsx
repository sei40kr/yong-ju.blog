import type { Metadata } from "next";
import { TagArchive, TagResults } from "~/containers/tag-archive";
import { POSTS_PER_PAGE } from "~/models/paginated";
import { withDevEncodedVariants } from "~/lib/static-params";
import { findPostInfosByTag, getPostInfos } from "~/repositories/post-infos";
import { getTagCounts } from "~/repositories/tags";

export const dynamicParams = false;

export async function generateStaticParams() {
  const postInfos = await getPostInfos();
  const tags = new Set(postInfos.flatMap(({ tags }) => [...tags]));
  return withDevEncodedVariants([...tags].map((tag) => ({ tag })));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ tag: string }>;
}): Promise<Metadata> {
  const tag = decodeURIComponent((await params).tag);
  return { title: tag };
}

// The old site redirected `/tags/:tag` to `/tags/:tag/page/1`. Static export
// cannot emit server redirects, so render the first page directly instead.
export default async function TagIndexPage({
  params,
}: {
  params: Promise<{ tag: string }>;
}) {
  const tag = decodeURIComponent((await params).tag);

  const [paginatedPostInfos, tags] = await Promise.all([
    findPostInfosByTag(tag, 0, POSTS_PER_PAGE),
    getTagCounts(),
  ]);

  return (
    <TagArchive tags={tags} currentTag={tag}>
      <TagResults
        tag={tag}
        posts={paginatedPostInfos.items}
        totalCount={paginatedPostInfos.totalCount}
        currentPage={1}
      />
    </TagArchive>
  );
}
