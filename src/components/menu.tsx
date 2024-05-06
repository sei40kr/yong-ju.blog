import { component$ } from "@builder.io/qwik";
import { Link } from "@builder.io/qwik-city";
import { css } from "~/styled-system/css";

export const Menu = component$(({ tags }: { tags: Set<string> }) => {
  return (
    <>
      <h3
        class={css({
          mb: "2",
          fontSize: "md",
          fontWeight: "bold",
        })}
      >
        タグ
      </h3>
      <ul class={css()}>
        {[...tags].sort().map((tag) => (
          <li key={tag} class={css({ py: "1" })}>
            <Link
              href={`/tags/${encodeURIComponent(tag)}/page/1`}
              class={css({
                color: "gray.500",
                _hover: { color: "slate.700" },
              })}
            >
              {tag}
            </Link>
          </li>
        ))}
      </ul>
    </>
  );
});
