import { Box } from "@chakra-ui/react";
import type { Decorator } from "@storybook/nextjs-vite";
import type { ComponentProps, ComponentType } from "react";
import { useMDXComponents } from "~/mdx-components";

/**
 * The typography `src/components/mdx/` inherits from the article body (the
 * <Box> in src/app/posts/[slug]/page.tsx). Rendered outside it, those
 * components pick up the plain body font size and line height instead.
 */
export const withArticleBody: Decorator = (Story) => (
  <Box fontSize="lg" lineHeight="taller" color="gray.800">
    <Story />
  </Box>
);

/**
 * In a real post, a paragraph goes through the mdx-components.tsx remap
 * (`p` → `<Text my="5">`); a raw <p> in a story would carry no margins at all.
 */
export const P = useMDXComponents().p as ComponentType<ComponentProps<"p">>;
