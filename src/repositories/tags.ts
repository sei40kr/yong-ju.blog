import { getPostInfos } from "./post-infos";

export const getUniqueTags = async () =>
  new Set([...(await getPostInfos()).flatMap(({ tags }) => [...tags])]);

/** Tag → number of posts, sorted by count descending. */
export const getTagCounts = async (): Promise<Map<string, number>> => {
  const counts = new Map<string, number>();
  for (const { tags } of await getPostInfos()) {
    for (const tag of tags) {
      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }
  return new Map([...counts.entries()].sort((a, b) => b[1] - a[1]));
};
