import {
  Box,
  Card,
  Flex,
  HStack,
  Heading,
  LinkOverlay,
  Separator,
  SimpleGrid,
} from "@chakra-ui/react";
import type { Metadata } from "next";
import NextLink from "next/link";
import { LuArrowLeft, LuArrowRight } from "react-icons/lu";
import { Tag } from "~/components/tag/tag";
import { PostArticle } from "~/containers/post-article";
import { humanizeDate } from "~/lib/format";
import type { PostInfo } from "~/models/post-info";
import { getPostHeadings, getPostInfos } from "~/repositories/post-infos";

import "katex/dist/katex.min.css";

interface PostFrontmatter {
  title: string;
  tags?: string[];
}

const importPost = async (slug: string) => {
  const { default: PostContent, frontmatter } = await import(
    `@/content/posts/${slug}.mdx`
  );
  return { PostContent, frontmatter: frontmatter as PostFrontmatter };
};

export const dynamicParams = false;

export async function generateStaticParams() {
  return (await getPostInfos()).map(({ slug }) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const { frontmatter } = await importPost(slug);
  return { title: frontmatter.title };
}

const AdjacentPostCard = ({
  post,
  label,
  align = "left",
}: {
  post: PostInfo;
  label: string;
  align?: "left" | "right";
}) => (
  <Card.Root
    size="sm"
    minW="0"
    rounded="md"
    pos="relative"
    textAlign={align}
    _hover={{ bg: "bg.subtle" }}
  >
    <Card.Body gap="1.5">
      <HStack
        gap="1.5"
        justify={align === "right" ? "flex-end" : "flex-start"}
        fontSize="md"
        color="fg.subtle"
      >
        {align === "left" && <LuArrowLeft />}
        <span>{label}</span>
        {align === "right" && <LuArrowRight />}
      </HStack>
      <Card.Title
        fontSize="md"
        fontWeight="medium"
        lineHeight="tall"
        maxW="full"
        whiteSpace="nowrap"
        overflow="hidden"
        textOverflow="ellipsis"
      >
        <LinkOverlay asChild>
          <NextLink href={`/posts/${post.slug}`}>{post.title}</NextLink>
        </LinkOverlay>
      </Card.Title>
    </Card.Body>
  </Card.Root>
);

export default async function PostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const { PostContent } = await importPost(slug);

  const [allPosts, headings] = await Promise.all([
    getPostInfos(),
    getPostHeadings(slug),
  ]);
  const posts = [...allPosts].sort(
    (a, b) => b.date.getTime() - a.date.getTime(),
  );
  const index = posts.findIndex((post) => post.slug === slug);
  const post = posts[index];
  const newer = index > 0 ? posts[index - 1] : undefined;
  const older = index < posts.length - 1 ? posts[index + 1] : undefined;
  const tags = [...post.tags];

  return (
    <PostArticle slug={slug} title={post.title} headings={headings}>
      <Heading
        as="h1"
        fontSize="4xl"
        fontWeight="bold"
        lineHeight="moderate"
        letterSpacing="tight"
        mb="4"
        textWrap="pretty"
      >
        {post.title}
      </Heading>
      <Flex
        direction="column"
        align="flex-start"
        gap="3"
        pb="6"
        borderBottomWidth="1px"
      >
        {tags.length > 0 && (
          <HStack gap="1.5" wrap="wrap">
            {tags.map((tag) => (
              <Tag key={tag} tag={tag} />
            ))}
          </HStack>
        )}
        <HStack gap="3" fontSize="md" color="fg.subtle">
          <span>{humanizeDate(post.date)}</span>
          <Separator orientation="vertical" height="3.5" />
          <span>{post.readMinutes} min</span>
        </HStack>
      </Flex>

      <Box
        pt="7"
        fontSize="lg"
        lineHeight="taller"
        color="gray.800"
        css={{
          "& > :first-child": { marginTop: 0 },
          "& > :last-child": { marginBottom: 0 },
          // Definition lists are authored as raw <dl>/<dt>/<dd> HTML in MDX,
          // which bypasses the component remap, so style them here. Rendered as
          // the design's "hanging" variant: the term sits in a fixed left
          // column with its definition(s) in the right column, collapsing to a
          // stacked layout on narrow screens.
          "& dl": {
            marginBlock: "7",
            display: "grid",
            gridTemplateColumns: { base: "1fr", md: "168px minmax(0, 1fr)" },
            columnGap: "6",
            rowGap: "5",
            alignItems: "start",
          },
          "& dt": {
            gridColumn: { md: "1" },
            fontFamily: "serif",
            fontSize: "lg",
            fontWeight: "semibold",
            lineHeight: "tall",
          },
          "& dd": {
            gridColumn: { md: "2" },
            marginInlineStart: "0",
            fontSize: "md",
            lineHeight: "taller",
            color: "fg.muted",
            textWrap: "pretty",
            "& > :first-child": { marginTop: 0 },
            "& > :last-child": { marginBottom: 0 },
          },
        }}
      >
        <PostContent />
      </Box>

      {(older || newer) && (
        <SimpleGrid columns={{ base: 1, sm: 2 }} gap="3" mt="8">
          <Box minW="0">
            {older && <AdjacentPostCard post={older} label="前の記事" />}
          </Box>
          <Box minW="0">
            {newer && (
              <AdjacentPostCard post={newer} label="次の記事" align="right" />
            )}
          </Box>
        </SimpleGrid>
      )}
    </PostArticle>
  );
}
