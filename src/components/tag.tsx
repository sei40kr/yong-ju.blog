import { component$ } from "@builder.io/qwik";
import { Link } from "@builder.io/qwik-city";
import { css } from "~/styled-system/css";

export const Tag = component$(({ tag }: { tag: string }) => {
  return (
    <Link
      href={`/tags/${tag}`}
      class={css({
        px: "3",
        py: "0.5",
        rounded: "full",
        bg: "slate.200",
        fontWeight: "bold",
        _hover: {
          bg: "slate.300",
        },
      })}
    >
      #{tag}
    </Link>
  );
});
