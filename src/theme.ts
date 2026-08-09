import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const SERIF =
  "'Noto Serif JP', 'Hiragino Mincho ProN', 'Yu Mincho', Georgia, serif";
const SANS =
  "Inter, 'Noto Sans JP', -apple-system, 'Hiragino Kaku Gothic ProN', sans-serif";

const config = defineConfig({
  globalCss: {
    html: {
      scrollPaddingTop: "20",
    },
    body: {
      fontFeatureSettings: '"cv11"',
      textRendering: "optimizeLegibility",
    },
    "::selection": {
      bg: "blue.100",
    },
  },
  theme: {
    tokens: {
      fonts: {
        heading: { value: SERIF },
        body: { value: SANS },
        serif: { value: SERIF },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
