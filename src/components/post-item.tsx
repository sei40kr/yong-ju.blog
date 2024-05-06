import { component$ } from "@builder.io/qwik";
import { css } from "~/styled-system/css";
import { BsCalendar } from "@qwikest/icons/bootstrap";
import { Link } from "@builder.io/qwik-city";
import { Wrap } from "~/styled-system/jsx/wrap.mjs";
import { Tag } from "~/components/tag";
import { HStack } from "~/styled-system/jsx/hstack.mjs";
import type { PostInfo } from "~/models/post-info";

const DATE_FORMATTER = new Intl.DateTimeFormat("ja-JP", {
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
});

export const PostItem = component$(
  ({ post: { id, title, date, tags } }: { post: PostInfo }) => {
    return (
      <article>
        <Link href={`/posts/${id}`}>
          <span
            class={css({
              fontSize: "1.875rem",
              lineHeight: "2.25rem",
              fontWeight: "bold",
            })}
          >
            {title}
          </span>
        </Link>

        <div class={css({ mt: "3" })}>
          <Wrap gap="3">
            <HStack gap="1.5" class={css({ color: "gray.500" })}>
              <BsCalendar />
              <span>{DATE_FORMATTER.format(date)}に公開</span>
            </HStack>
          </Wrap>
        </div>

        <div class={css({ mt: "3" })}>
          <Wrap gap="3">
            {[...tags].map((tag) => (
              <Tag key={tag} tag={tag} />
            ))}
          </Wrap>
        </div>
      </article>
    );
  },
);
