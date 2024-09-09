import { component$ } from "@builder.io/qwik";
import {
  type StaticGenerateHandler,
  routeLoader$,
  useLocation,
  useNavigate,
  type DocumentHead,
} from "@builder.io/qwik-city";
import { PostList } from "~/components/post-list";
import {
  findPostInfosByCategory,
  getPostInfos,
} from "~/repositories/post-infos";

const POSTS_PER_PAGE = 5;

export const usePostInfoPage = routeLoader$(async (requestEvent) => {
  const page = Number.parseInt(requestEvent.params.page);
  return await findPostInfosByCategory(
    requestEvent.params.category,
    (page - 1) * POSTS_PER_PAGE,
    POSTS_PER_PAGE,
  );
});

export const head: DocumentHead = ({ params }) => ({
  title: params.category,
});

export default component$(() => {
  const { params } = useLocation();
  const currentPage = Number.parseInt(params.page);

  const postInfoPage = usePostInfoPage().value;
  const totalPages = Math.ceil(postInfoPage.totalCount / POSTS_PER_PAGE);

  const nav = useNavigate();

  return (
    <PostList
      totalPages={totalPages}
      currentPage={currentPage}
      posts={postInfoPage.items}
      onPageChange$={(page) => nav(`/tags/${params.category}/page/${page}`)}
    />
  );
});

export const onStaticGenerate: StaticGenerateHandler = async () => {
  const postInfos = await getPostInfos();
  const postCountByCategory = postInfos.reduce((acc, postInfo) => {
    for (const category of postInfo.categories) {
      acc.set(category, (acc.get(category) ?? 0) + 1);
    }
    return acc;
  }, new Map<string, number>());
  return {
    params: Array.from(postCountByCategory.entries()).flatMap(
      ([category, count]) => {
        const totalPages = Math.ceil(count / POSTS_PER_PAGE);
        return Array.from({ length: totalPages }, (_, i) => ({
          category,
          page: `${i + 1}`,
        }));
      },
    ),
  };
};
