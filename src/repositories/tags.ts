import { getPostInfos } from "./post-infos";

export const getTags = async () =>
  new Set([...(await getPostInfos()).flatMap(({ tags }) => [...tags])]);
