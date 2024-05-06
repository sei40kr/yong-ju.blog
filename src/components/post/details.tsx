import { Slot, component$ } from "@builder.io/qwik";
import { BsChevronRight } from "@qwikest/icons/bootstrap";
import { css } from "~/styled-system/css";
import { HStack } from "~/styled-system/jsx";

export const Details = component$(({ title }: { title: string }) => (
  <details
    class={css({
      my: "6",
      border: "1px solid",
      borderColor: "gray.200",
      rounded: "lg",
      shadow: "sm",
    })}
  >
    <summary
      class={css({
        listStyleType: "none",
      })}
    >
      <HStack class={css({ pl: "4", pr: "6", py: "3" })}>
        <div>
          <BsChevronRight />
        </div>
        <div class={css({ flexGrow: "1", lineHeight: "normal" })}>{title}</div>
      </HStack>
    </summary>

    <div class={css({ px: "6", py: "3", "& > *": { _last: { mb: "0" } } })}>
      <Slot />
    </div>
  </details>
));
