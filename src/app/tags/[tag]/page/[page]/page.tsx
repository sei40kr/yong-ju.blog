import type { Metadata } from "next";
import { TagArchive, TagResults } from "~/containers/tag-archive";
import { POSTS_PER_PAGE } from "~/models/paginated";
import { withDevEncodedVariants } from "~/lib/static-params";
import { findPostInfosByTag } from "~/repositories/post-infos";
import { getTagCounts } from "~/repositories/tags";

export const dynamicParams = false;

export async function generateStaticParams() {
  const postCountByTag = await getTagCounts();
  return withDevEncodedVariants(
    Array.from(postCountByTag.entries()).flatMap(([tag, count]) => {
      const totalPages = Math.ceil(count / POSTS_PER_PAGE);
      return Array.from({ length: totalPages }, (_, i) => ({
        tag,
        page: `${i + 1}`,
      }));
    }),
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ tag: string; page: string }>;
}): Promise<Metadata> {
  const tag = decodeURIComponent((await params).tag);
  return { title: tag };
}

export default async function TagPostsPage({
  params,
}: {
  params: Promise<{ tag: string; page: string }>;
}) {
  const { tag: rawTag, page } = await params;
  const tag = decodeURIComponent(rawTag);
  const currentPage = Number.parseInt(page);

  const [paginatedPostInfos, tags] = await Promise.all([
    findPostInfosByTag(tag, (currentPage - 1) * POSTS_PER_PAGE, POSTS_PER_PAGE),
    getTagCounts(),
  ]);

  return (
    <TagArchive tags={tags} currentTag={tag}>
      <TagResults
        tag={tag}
        posts={paginatedPostInfos.items}
        totalCount={paginatedPostInfos.totalCount}
        currentPage={currentPage}
      />
    </TagArchive>
  );
}
