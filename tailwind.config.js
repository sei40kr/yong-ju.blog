const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./layouts/**/*.html",
    "./{assets,static}/**/*.js",
    "./themes/hugo-book/layouts/**/*.html",
    "./themes/hugo-book/{assets,static}/**/*.js",
    { raw: '<div class="markdown"><blockquote>', extension: "html" },
    { raw: '<div class="markdown"><code>', extension: "html" },
    { raw: '<div class="markdown"><dl><dt>', extension: "html" },
    { raw: '<div class="markdown"><dl><dd>', extension: "html" },
    { raw: '<div class="markdown"><hr>', extension: "html" },
    { raw: '<div class="markdown"><img>', extension: "html" },
    { raw: '<div class="markdown"><ol><li>', extension: "html" },
    { raw: '<div class="markdown"><p>', extension: "html" },
    { raw: '<div class="markdown"><table><thead><tr><th>', extension: "html" },
    { raw: '<div class="markdown"><table><tbody><tr><td>', extension: "html" },
    { raw: '<div class="markdown"><ul><li>', extension: "html" },
    {
      raw: '<div class="markdown"><div class="highlight"><pre>',
      extension: "html",
    },
    { raw: '<div class="markdown"><span class="katex">', extension: "html" },
    {
      raw: '<div class="markdown"><span class="katex-display">',
      extension: "html",
    },
  ],
  theme: {
    fontFamily: {
      serif: [
        "Noto Serif JP",
        "ヒラギノ明朝 ProN W6",
        "HiraMinProN-W6",
        "ＭＳ Ｐ明朝",
        "MS PMincho",
        "serif",
      ],
    },
    extend: {
      colors: {
        link: colors.blue["500"],
        "link-hover": colors.blue["700"],
        muted: colors.gray["500"],
      },
    },
  },
  plugins: [],
};