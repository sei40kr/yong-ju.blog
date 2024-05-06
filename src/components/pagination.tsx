import { type PropFunction, component$ } from "@builder.io/qwik";
import {
  BsChevronDoubleLeft,
  BsChevronDoubleRight,
  BsChevronLeft,
  BsChevronRight,
} from "@qwikest/icons/bootstrap";
import { css, cva } from "~/styled-system/css";

const button = cva({
  base: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderTop: "1px solid",
    borderTopColor: "transparent",
    marginX: "0.5",
    marginTop: "-1px",
    w: "10",
    h: "11",
    color: "gray.500",
    fontSize: "sm",
    _hover: {
      bgColor: "slate.100",
      borderTopColor: "blue.500",
      color: "blue.500",
    },
    _disabled: {
      color: "gray.200",
      _hover: {
        borderTopColor: "unset",
        bgColor: "unset",
        color: "unset",
      },
    },
    _currentPage: {
      borderTopColor: "black",
      color: "black",
      fontWeight: "bold",
      _hover: {
        borderTopColor: "unset",
        bgColor: "unset",
        color: "unset",
      },
    },
  },
});

export const Pagination = component$(
  ({
    totalPages,
    currentPage,
    onChange$,
  }: {
    totalPages: number;
    currentPage: number;
    onChange$: PropFunction<(page: number) => void>;
  }) => {
    return (
      <nav>
        <ul
          class={css({
            display: "flex",
            alignItems: "stretch",
            justifyContent: "center",
            borderTop: "1px solid",
            borderTopColor: "gray.200",
          })}
        >
          <li>
            <button
              type="button"
              class={button()}
              disabled={currentPage === 1}
              onClick$={() => {
                if (currentPage > 1) {
                  onChange$(1);
                }
              }}
            >
              <BsChevronDoubleLeft />
            </button>
          </li>
          <li>
            <button
              type="button"
              class={button()}
              disabled={currentPage === 1}
              onClick$={() => {
                if (currentPage > 1) {
                  onChange$(currentPage - 1);
                }
              }}
            >
              <BsChevronLeft />
            </button>
          </li>
          {new Array(totalPages).fill(0).map((_, i) => {
            const isCurrent = i + 1 === currentPage;

            return (
              // biome-ignore lint/suspicious/noArrayIndexKey: <explanation>
              <li key={i}>
                <button
                  type="button"
                  class={button()}
                  aria-current={isCurrent ? "page" : undefined}
                  onClick$={() => onChange$(i + 1)}
                >
                  {i + 1}
                </button>
              </li>
            );
          })}
          <li>
            <button
              type="button"
              class={button()}
              disabled={currentPage === totalPages}
              onClick$={() => onChange$(currentPage + 1)}
            >
              <BsChevronRight />
            </button>
          </li>
          <li>
            <button
              type="button"
              class={button()}
              disabled={currentPage === totalPages}
              onClick$={() => onChange$(totalPages)}
            >
              <BsChevronDoubleRight />
            </button>
          </li>
        </ul>
      </nav>
    );
  },
);
