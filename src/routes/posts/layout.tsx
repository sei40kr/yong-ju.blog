import { component$, Slot } from "@builder.io/qwik";
import { useDocumentHead } from "@builder.io/qwik-city";
import { css } from "~/styled-system/css";
import "katex/dist/katex.min.css";
import { Body } from "~/components/post/body";
import { Wrap } from "~/styled-system/jsx";
import { Tag } from "~/components/tag";

export default component$(() => {
  const { title, frontmatter } = useDocumentHead();

  return (
    <>
      <h1
        class={css({
          fontSize: "4xl",
          fontWeight: "bold",
        })}
      >
        {title}
      </h1>

      <div class={css({ mt: "3" })}>
        <Wrap gap="3">
          {(frontmatter.tags ?? []).map((tag: string) => (
            <Tag key={tag} tag={tag} />
          ))}
        </Wrap>
      </div>

      <div class={css({ py: "8" })}>
        <Body>
          <Slot />
        </Body>
      </div>
    </>
  );
});
