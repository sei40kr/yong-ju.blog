import { component$ } from "@builder.io/qwik";
import { type StaticGenerateHandler, routeLoader$, useLocation, useNavigate } from "@builder.io/qwik-city";
import { PostList } from "~/components/post-list";
import { findRecentPostInfos, getPostInfos } from "~/repositories/post-infos";

const POSTS_PER_PAGE = 5;

export const usePostInfoPage = routeLoader$(async (requestEvent) => {
  const currentPage = Number.parseInt(requestEvent.params.page);
  return findRecentPostInfos(
    (currentPage - 1) * POSTS_PER_PAGE,
    POSTS_PER_PAGE,
  );
});

export default component$(() => {
  const { params } = useLocation();
  const currentPage = Number.parseInt(params.page);

  const page = usePostInfoPage().value;
  const totalPages = Math.ceil(page.totalCount / POSTS_PER_PAGE);

  const nav = useNavigate();

  return (
    <PostList
      totalPages={totalPages}
      currentPage={currentPage}
      posts={page.items}
      onPageChange$={async (page) => await nav(`/page/${page}`)}
    />
  );
});

export const onStaticGenerate: StaticGenerateHandler = async () => {
  const postInfos = await getPostInfos();
  const totalPages = Math.ceil(postInfos.length / POSTS_PER_PAGE);
  return { params: Array.from({ length: totalPages }, (_, i) => ({ page: `${i + 1}` })) };
};
