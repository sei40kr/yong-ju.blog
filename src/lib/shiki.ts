import { createShikiAdapter } from "@chakra-ui/react";
import { createJavaScriptRegexEngine } from "@shikijs/engine-javascript";
import bash from "@shikijs/langs/bash";
import emacsLisp from "@shikijs/langs/emacs-lisp";
import ini from "@shikijs/langs/ini";
import javascript from "@shikijs/langs/javascript";
import kotlin from "@shikijs/langs/kotlin";
import nix from "@shikijs/langs/nix";
import sql from "@shikijs/langs/sql";
import nightOwl from "@shikijs/themes/night-owl";
import { createHighlighterCoreSync } from "shiki/core";

// A synchronous highlighter so code is highlighted during the static export
// (build-time) — the same zero-flash behaviour rehype-pretty-code gave us,
// now driven through Chakra's CodeBlock. `bash` covers the sh/zsh aliases and
// `javascript` covers js; the rest map 1:1 to the fences used in content/.
const highlighter = createHighlighterCoreSync({
  engine: createJavaScriptRegexEngine(),
  themes: [nightOwl],
  langs: [bash, javascript, sql, nix, kotlin, ini, emacsLisp],
});

const shikiAdapter = createShikiAdapter({
  loadSync: () => highlighter,
  load: async () => highlighter,
  theme: "night-owl",
});

const shikiHighlight = shikiAdapter.getHighlighter(highlighter);

/** Server components only — a client import pulls ~1MB of grammars into the bundle. */
export const highlight = (code: string, language?: string) =>
  shikiHighlight({ code, language });
