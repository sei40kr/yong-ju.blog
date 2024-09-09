import { getPostInfos } from "./post-infos";

export const getCategories = async () =>
  new Set([
    ...(await getPostInfos()).flatMap(({ categories }) => [...categories]),
  ]);
