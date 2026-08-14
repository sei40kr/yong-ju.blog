import {
  Blockquote,
  Box,
  Code,
  Heading,
  Image,
  Link as ChakraLink,
  List,
  Separator,
  Table,
  Text,
} from "@chakra-ui/react";
import type { MDXComponents } from "mdx/types";
import NextLink from "next/link";
import type { ComponentProps, ReactElement } from "react";
import { CodeBlock } from "~/components/mdx/code-block";
import { Details } from "~/components/mdx/details";
import { Hint } from "~/components/mdx/hint";
import { Mermaid } from "~/components/mdx/mermaid";
import { highlight } from "~/lib/shiki";

// Vertical rhythm of the article body.
//
// Blocks flow in a plain <Box> with symmetric margins that collapse to
// max(above, below). Three tiers: prose (5), block (7), rules (8). Headings
// reserve space above only (mb 0) and hug the content below; the next block's
// top margin fills the gap. The container zeroes the first/last block margins.

const components: MDXComponents = {
  Details,
  Hint,
  Link: (props: ComponentProps<typeof NextLink>) => (
    <ChakraLink
      asChild
      color="blue.600"
      _hover={{ color: "blue.700", textDecoration: "underline" }}
    >
      <NextLink {...props} />
    </ChakraLink>
  ),
  h2: (props) => (
    <Heading
      as="h2"
      fontSize="2xl"
      fontWeight="semibold"
      letterSpacing="tight"
      lineHeight="moderate"
      mt="11"
      mb="0"
      {...props}
    />
  ),
  h3: (props) => (
    <Heading
      as="h3"
      fontSize="lg"
      fontWeight="semibold"
      letterSpacing="tight"
      mt="8"
      mb="0"
      {...props}
    />
  ),
  h4: (props) => (
    <Heading
      as="h4"
      fontSize="lg"
      fontWeight="semibold"
      mt="7"
      mb="0"
      {...props}
    />
  ),
  h5: (props) => (
    <Heading
      as="h5"
      fontSize="lg"
      fontWeight="semibold"
      mt="7"
      mb="0"
      {...props}
    />
  ),
  h6: (props) => (
    <Heading
      as="h6"
      fontSize="lg"
      fontWeight="semibold"
      mt="7"
      mb="0"
      {...props}
    />
  ),
  p: (props) => <Text my="5" textWrap="pretty" {...props} />,
  a: (props) => (
    <ChakraLink
      color="blue.600"
      _hover={{ color: "blue.700", textDecoration: "underline" }}
      {...props}
    />
  ),
  blockquote: (props) => (
    <Blockquote.Root
      colorPalette="blue"
      color="fg.muted"
      my="7"
      css={{ "& > :last-child": { marginBottom: 0 } }}
      {...props}
    />
  ),
  code: (props: ComponentProps<"code">) =>
    // Only inline code is styled here; a fenced block carries a language class
    // and is handled by the `pre` mapper below, so leave it untouched.
    props.className?.includes("language-") ? (
      <code {...props} />
    ) : (
      <Code fontSize="1em" rounded="xs" {...props} />
    ),
  // A fenced block arrives as <pre><code class="language-xxx">…</code></pre>.
  // Highlighting happens here, on the server, so Shiki stays out of the bundle.
  pre: ({ children }) => {
    const child = children as ReactElement<{
      className?: string;
      children?: string;
    }>;
    const language = /language-([\w-]+)/.exec(
      child?.props?.className ?? "",
    )?.[1];
    // CodeBlock.Root trims its own copy, so match it or the trailing newline
    // renders as a blank line.
    const code = String(child?.props?.children ?? "").trim();
    // ```mermaid is a diagram, not source: it never reaches Shiki (which would
    // throw on the unregistered language) and renders in the browser instead.
    // The frame around it is the article's, not the component's.
    if (language === "mermaid") {
      return (
        <Box my="7" px="4" py="6" bg="bg" borderWidth="1px" rounded="md">
          <Mermaid code={code} />
        </Box>
      );
    }
    return <CodeBlock code={code} highlighted={highlight(code, language)} />;
  },
  // Stock List with native markers (variant="marker"). Marker styling goes
  // through the `_marker` style prop on the item — never a raw `::marker`
  // selector. The only css here is the nested-list reset, which has no prop
  // equivalent: a list nested under an <li> flows tightly instead of taking
  // the full block `my`.
  ul: (props) => (
    <List.Root
      my="5"
      ps="6"
      gap="2"
      variant="marker"
      listStyleType="disc"
      css={{ "li &": { marginBlock: 0, marginTop: "2" } }}
      {...props}
    />
  ),
  ol: (props) => (
    <List.Root
      as="ol"
      my="5"
      ps="6"
      gap="2"
      variant="marker"
      listStyleType="decimal"
      css={{ "li &": { marginBlock: 0, marginTop: "2" } }}
      {...props}
    />
  ),
  li: (props) => (
    <List.Item _marker={{ color: "blue.600", fontFamily: "mono" }} {...props} />
  ),
  img: (props) => <Image maxW="100%" rounded="md" {...props} />,
  hr: () => <Separator my="8" />,
  table: (props) => (
    <Table.ScrollArea my="7" borderWidth="1px" rounded="md" bg="bg">
      <Table.Root size="md" fontSize="md" color="fg" {...props} />
    </Table.ScrollArea>
  ),
  thead: (props) => <Table.Header {...props} />,
  tbody: (props) => <Table.Body {...props} />,
  tr: (props) => <Table.Row {...props} />,
  // The header background goes on the cells, not on <thead>: the "line"
  // variant paints every <tr> with `bg`, which would cover a <thead>
  // background.
  th: (props) => <Table.ColumnHeader bg="bg.subtle" {...props} />,
  td: (props) => <Table.Cell {...props} />,
};

export function useMDXComponents(): MDXComponents {
  return components;
}
