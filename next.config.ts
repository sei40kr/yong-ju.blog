import createMDX from "@next/mdx";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // The site is deployed as static files to S3 + CloudFront. A CloudFront
  // function rewrites extension-less URIs to `<uri>/index.html`, hence the
  // trailing-slash (directory-style) output.
  output: "export",
  trailingSlash: true,
  // Allow .mdx files to be imported as pages/components.
  pageExtensions: ["js", "jsx", "md", "mdx", "ts", "tsx"],
};

const withMDX = createMDX({
  options: {
    // Plugins are referenced by name so the config stays serializable, which
    // Turbopack requires.
    remarkPlugins: [
      "remark-frontmatter",
      "remark-mdx-frontmatter",
      "remark-gfm",
      "remark-math",
    ],
    // Syntax highlighting is no longer done here: fenced code blocks pass
    // through untouched and are highlighted by the stock Chakra CodeBlock via
    // a Shiki adapter (Night Owl) — see src/lib/shiki.ts and code-block.tsx.
    rehypePlugins: ["rehype-katex", "rehype-slug"],
  },
});

export default withMDX(nextConfig);
