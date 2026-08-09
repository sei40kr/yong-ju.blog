import type { Metadata } from "next";
import { TagArchive } from "~/containers/tag-archive";
import { getTagCounts } from "~/repositories/tags";

export const metadata: Metadata = {
  title: "タグ",
};

export default async function TagsPage() {
  const tags = await getTagCounts();

  return <TagArchive tags={tags} />;
}
