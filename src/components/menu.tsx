import { component$ } from "@builder.io/qwik";
import { Link } from "@builder.io/qwik-city";
import { css } from "~/styled-system/css";

export const Menu = component$(
  ({ categories }: { categories: Set<string> }) => {
    return (
      <>
        <h3
          class={css({
            mb: "2",
            fontSize: "md",
            fontWeight: "bold",
          })}
        >
          カテゴリ
        </h3>
        <ul class={css()}>
          {[...categories].sort().map((category) => (
            <li key={category} class={css({ py: "1" })}>
              <Link
                href={`/categories/${encodeURIComponent(category)}/page/1`}
                class={css({
                  color: "gray.500",
                  _hover: { color: "slate.700" },
                })}
              >
                {category}
              </Link>
            </li>
          ))}
        </ul>
      </>
    );
  },
);
