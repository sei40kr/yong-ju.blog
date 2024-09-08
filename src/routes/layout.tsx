import { component$, Slot } from "@builder.io/qwik";
import { routeLoader$ } from "@builder.io/qwik-city";
import type { RequestHandler } from "@builder.io/qwik-city";
import { Header } from "~/components/header";
import { Menu } from "~/components/menu";
import { getTags } from "~/repositories/tags";
import { css } from "~/styled-system/css";
import { Container, Flex } from "~/styled-system/jsx";

export const onGet: RequestHandler = async ({ cacheControl }) => {
  // Control caching for this request for best performance and to reduce hosting costs:
  // https://qwik.dev/docs/caching/
  cacheControl({
    // Always serve a cached response by default, up to a week stale
    staleWhileRevalidate: 60 * 60 * 24 * 7,
    // Max once every 5 seconds, revalidate on the server to get a fresh version of this page
    maxAge: 5,
  });
};

export const useServerTimeLoader = routeLoader$(() => {
  return {
    date: new Date().toISOString(),
  };
});

export const useTags = routeLoader$(async () => await getTags());

export default component$(() => {
  const tags = useTags().value;

  return (
    <>
      <Header />
      <Container
        class={css({
          mt: {
            base: "44px",
            sm: "50px",
            lg: "64px",
          },
        })}
      >
        <Flex direction="row" align="start">
          <div
            class={css({
              display: {
                base: "none",
                lg: "block",
              },
              flex: "0 0 19.5rem",
              w: "19.5rem",
              px: {
                base: "8",
                sm: "12",
              },
              py: "8",
            })}
          >
            <Menu tags={tags} />
          </div>
          <div
            class={css({
              overflow: "auto",
              flex: "1 1 auto",
              px: {
                base: "8",
                sm: "12",
              },
              py: "8",
            })}
          >
            <Slot />
          </div>
        </Flex>
      </Container>
    </>
  );
});
