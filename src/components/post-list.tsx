import { type PropFunction, component$ } from "@builder.io/qwik";
import { css } from "~/styled-system/css";
import { Pagination } from "~/components/pagination";
import { PostItem } from "~/components/post-item";
import type { PostInfo } from "~/models/post-info";

export const PostList = component$(
  ({
    totalPages,
    currentPage,
    posts,
    onPageChange$,
  }: {
    totalPages: number;
    currentPage: number;
    posts: PostInfo[];
    onPageChange$: PropFunction<(page: number) => void>;
  }) => {
    return (
      <>
        {posts.map((post) => (
          <div key={post.id} class={css({ mb: 12 })}>
            <PostItem post={post} />
          </div>
        ))}

        <Pagination
          totalPages={totalPages}
          currentPage={currentPage}
          onChange$={onPageChange$}
        />
      </>
    );
  },
);
