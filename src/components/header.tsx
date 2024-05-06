import { component$ } from "@builder.io/qwik";
import { Link } from "@builder.io/qwik-city";
import { css } from "~/styled-system/css";
import { flex } from "~/styled-system/patterns";
import "@fontsource/noto-serif-jp/japanese-700.css";

export const Header = component$(() => (
  <header
    class={[
      flex({
        align: "center",
        justify: "center",
      }),
      css({
        pos: "fixed",
        zIndex: 30,
        top: 0,
        w: "full",
        h: {
          base: "44px",
          sm: "50px",
          lg: "64px",
        },
        bgColor: "white",
        borderBottom: "1px solid",
        borderColor: "gray.200",
        fontSize: {
          base: "xl",
          sm: "2xl",
          lg: "3xl",
        },
        fontFamily: "serif",
        fontWeight: "bold",
        letterSpacing: "tighter",
      }),
    ]}
  >
    <Link href="/">よんログ</Link>
  </header>
));
