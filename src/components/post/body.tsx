import { component$, Slot } from "@builder.io/qwik";
import { css } from "~/styled-system/css";
import "@fontsource/noto-serif-jp/japanese-500.css";

export const Body = component$(() => (
  <div
    class={css({
      fontSize: "lg",
      lineHeight: "2rem",
      fontFamily: "serif",
      "& > *": {
        _first: { mt: "0" },
        _last: { mb: "0" },
      },
      "& a": {
        color: "blue.700",
        textDecoration: "underline",
        _hover: { color: "blue.500" },
      },
      "& blockquote": {
        my: "6",
        pl: "6",
        py: "2",
        borderLeft: "4px solid",
        borderColor: "gray.300",
        "& > *": {
          _last: { mb: "0" },
        },
      },
      "& code": {
        color: "rose.700",
      },
      "& dl": {
        my: "3",
      },
      "& dt": {
        fontWeight: "bold",
      },
      "& dd": {
        mb: "2",
        pl: "8",
      },
      "& h2, & h3, & h4, & h5, & h6": {
        mb: "2",
        mt: "8",
        fontFamily: "sans-serif",
      },
      "& h2": {
        mb: "4",
        fontSize: "3xl",
        fontWeight: "bold",
      },
      "& h3": {
        fontSize: "2xl",
        fontWeight: "bold",
      },
      "& h4": {
        fontSize: "xl",
        fontWeight: "bold",
      },
      "& h5": {
        fontSize: "lg",
        fontWeight: "bold",
      },
      "& h6": {
        fontSize: "lg",
        fontWeight: "bold",
      },
      "& hr": {
        h: "1px",
        my: "4",
        backgroundColor: "current",
        opacity: "0.25",
      },
      "& img": {
        w: "full",
      },
      "& ol, & ul": {
        pl: "8",
      },
      "& ol": {
        listStyleType: "decimal",
      },
      "& ul": {
        listStyleType: "disc",
      },
      "& > ol, & > ul": {
        my: "3",
      },
      "& p": {
        mb: "4",
      },
      "& table": {
        w: "full",
        my: "6",
        fontSize: "medium",
        lineHeight: "normal",
      },
      "& thead, & tbody": {
        borderBottom: "1px solid",
        borderColor: "gray.200",
      },
      "& tbody tr:not(:first-child, :last-child)": {
        borderY: "1px solid",
        borderColor: "slate.100",
      },
      "& th, & td": {
        pr: "2",
        py: "2",
      },
      "& th": {
        fontWeight: "bold",
      },
      "& .katex-display": {
        my: "2",
      },
    })}
  >
    <Slot />
  </div>
));
