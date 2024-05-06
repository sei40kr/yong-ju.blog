import type { RequestEvent } from "@builder.io/qwik-city";

export const onGet = async ({ params, redirect }: RequestEvent) => {
  throw redirect(302, `/tags/${encodeURIComponent(params.tag)}/page/1`);
};
