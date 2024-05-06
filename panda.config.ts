import { defineConfig } from "@pandacss/dev";

export default defineConfig({
  jsxFramework: "qwik",

  // Whether to use css reset
  preflight: true,

  // Where to look for your css declarations
  include: ["./src/**/*.{js,jsx,ts,tsx}"],

  // Files to exclude
  exclude: [],

  // Useful for theme customization
  theme: {
    extend: {
      tokens: {
        fonts: {
          serif: {
            value:
              "'Noto Serif JP', 'ヒラギノ明朝 ProN W6', 'HiraMinProN-W6', 'ＭＳ Ｐ明朝', 'MS PMincho', serif",
          },
        },
      },
    },
  },

  // The output directory for your css system
  outdir: "src/styled-system",
});
