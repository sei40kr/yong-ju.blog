# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Each MDX file is read **twice, by two independent paths** — keep them in sync:

1. **Rendering** — `src/app/posts/[slug]/page.tsx` does
   `import("@/content/posts/${slug}.mdx")`, compiled by `@next/mdx` with the
   plugins in `next.config.ts` and remapped through `src/mdx-components.tsx`.
2. **Metadata** — `src/repositories/post-data.ts` reads the file with
   `gray-matter` and hands the body to `src/lib/post-content.ts`, which derives
   the excerpt, read time, and TOC headings by **regex, not a remark AST pass**
   (deliberate: avoids a second full parse). Heading ids are generated with
   `github-slugger` so they match what `rehype-slug` emits at render time — use
   the same slugger if you touch either side.

Everything is prerendered (`output: "export"`), so **`"use client"` is free** —
don't treat it as an RSC-boundary trade-off or wrap client components to keep the
boundary small.

Layering, with `~/*` → `src/*` and `@/*` → repo root (the latter exists so MDX
under `content/` can be imported):

- `src/repositories/` — the only filesystem access (`post-data.ts`, `tags.ts`);
  returns `src/models/` types.
- `src/containers/` — components that own side effects or state (e.g. TOC scroll
  tracking in `post-article.tsx`). Components outside `containers/` should be pure
  functions of their props.
- `src/components/` — presentational; `components/mdx/` are the components
  authors can use inside MDX (`<Hint>`, `<Details>`) plus the code block.
- `src/lib/` — pure helpers.

`POSTS_PER_PAGE` lives in `src/models/paginated.ts` rather than in the list
component: a client module's exports become client references when imported from
a server component, so `generateStaticParams` would get a reference, not a number.

### Japanese tag routes

`generateStaticParams` for `/tags/[tag]` must emit **raw** (unencoded) tag
values — `next build` writes them literally as directory names and S3
percent-decodes request URIs. But `next dev` matches URLs without decoding, so
`src/lib/static-params.ts#withDevEncodedVariants` adds percent-encoded duplicates
in development only. Any new route with non-ASCII params needs the same wrapper.

## Content

Posts are `content/posts/<slug>.mdx`; the filename is the slug. Frontmatter:

```yaml
title: "<記事タイトル>"
date: <ISO 8601 (タイムゾーン付き)>
tags: ["<タグ1>", "<タグ2>"]
```

The site is written in Japanese; tags are Japanese and appear raw in URLs.

## Commands

Package manager is **bun** (`bun.lock`; CI pins bun 1.3.13).

```sh
bun run dev             # next dev --turbopack
bun run build           # static export → out/
bun run build.types     # tsc --noEmit — the only type check
bun run fmt             # prettier --write .  (no prettier config; defaults)
bun run fmt.check
bun run storybook       # storybook dev on :6006
bun run build.storybook # → storybook-static/
```

There is no test suite and no ESLint. Verification = `build.types` + `build`.

## Never run `next build` / `next dev` in the repo root

`next dev` and `next build` both own `.next` (and the export dir `out/`). The user
usually has `bun run dev` on **localhost:3000**; whichever of the two starts second
clobbers the other's `.next`, and the dev server then serves 500s until restarted.
A different port doesn't help, and a custom `distDir` can't isolate it either — with
`output: "export"` Next forces `distDir` back to `.next` (`hasCustomExportOutput`,
`next/dist/export/utils.js`; verified). So, in order of preference:

**1. Don't build.** `bun run build.types` (`tsc --noEmit`) catches most breakage and
touches only `tsconfig.tsbuildinfo`. For visual checks, use the running dev server —
edits hot-reload:

```sh
curl -s http://localhost:3000/posts/<slug>/ | head
```

First confirm it's up. If it's not listening or returns 500, tell the user and let
them (re)start it — never kill or restart their dev server yourself.

**2. When the static export itself must be verified** — export-only failures
(`generateStaticParams`, `dynamicParams`, non-ASCII route dirs) — build from an
isolated copy so `.next`/`out/` land in the scratchpad only (~40 s):

```sh
SRC=$PWD
DIR=<scratchpad>/build-check           # any dir outside the repo
mkdir -p "$DIR"
rsync -a --delete --exclude node_modules --exclude .next --exclude out \
      --exclude .git "$SRC/" "$DIR/"
cp -al "$SRC/node_modules" "$DIR/node_modules"   # hardlink, not symlink: Turbopack
                                                 # rejects a symlinked node_modules
(cd "$DIR" && bun run build)
```

Keep the dir between runs — `rsync --delete` re-syncs it and Next reuses its cache.
If unsure the isolation held, check `.next/required-server-files.json` — its
`appDir` must be the copy.

## Styling

Chakra UI v3 + Emotion.

- **Prefer stock Chakra components** over custom ones.
- **Markdown styling belongs in `src/mdx-components.tsx`** as element→component
  mappings, not in CSS-selector blobs. Not every tag goes through that remap,
  though: raw HTML written directly in MDX (e.g. `<dl>`) bypasses it and is styled
  in the post page's `css` prop. KaTeX is a separate story — its output comes from
  rehype-katex, not the mapping, and is styled in `src/app/globals.css`.
- `src/theme.ts` sets the fonts — a Japanese-capable serif (明朝) for headings —
  and little else.

## Storybook

`@storybook/nextjs-vite` (Vite, not the Next builder), so **Storybook never
touches `.next`/`out/`** — safe to run in the repo root while `bun run dev` is up.

Stories are colocated (`src/components/**/*.stories.tsx`, kebab-case). Page-level
compositions are deliberately not storied — components only. Sample data lives in
`.storybook/fixtures.ts`, intentionally **not** from `content/`: editing a post
must not change what stories render.

Two traps when writing stories:

- **MDX components** (`src/components/mdx/`) inherit `fontSize="lg"` /
  `lineHeight="taller"` from the article body, and their children go through
  the `mdx-components.tsx` remap (`p` → `<Text my="5">`) — a raw `<p>` in a
  story carries no margins. Use `withArticleBody` and `P` from
  `.storybook/article.tsx`.
- **CodeBlock stories** can only use languages imported in `src/lib/shiki.ts` —
  an unregistered language throws rather than rendering unhighlighted.

## Deployment

`.github/workflows/main.yml` builds every push/PR and, on `main`, syncs `out/` to
S3 and invalidates CloudFront. Infra lives in `provisioning/terraform/`.

Because the site is `output: "export"` + `trailingSlash: true`, there is no
server at runtime: no redirects, no rewrites, no dynamic params
(`dynamicParams = false` on every dynamic route). Directory-style URLs are
resolved by the CloudFront function in `provisioning/terraform/url-rewrite.js`,
which also maps `/` → `/page/1/index.html`. Routes that "should" redirect
(`/`, `/tags/[tag]`) instead render page 1 directly.
