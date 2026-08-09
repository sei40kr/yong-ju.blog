import { Box, Heading, Text } from "@chakra-ui/react";
import type { ReactNode } from "react";
import { PostList } from "~/components/post-list/post-list";
import { TagCloud } from "~/components/tag/tag-cloud";
import type { PostInfo } from "~/models/post-info";

export const TagArchive = ({
  tags,
  currentTag,
  children,
}: {
  tags: Map<string, number>;
  currentTag?: string;
  children?: ReactNode;
}) => (
  <Box as="main" maxW="5xl" mx="auto" px="6" pt="12" pb="24">
    <Heading
      as="h1"
      fontSize="3xl"
      fontWeight="bold"
      letterSpacing="tight"
      mb="2"
    >
      タグ
    </Heading>
    <Text fontSize="md" color="fg.muted" mb="8">
      {tags.size} のタグ。選ぶと該当する記事に絞り込みます。
    </Text>
    <Box mb="11">
      <TagCloud tags={tags} currentTag={currentTag} />
    </Box>
    {children}
  </Box>
);

export const TagResults = ({
  tag,
  posts,
  totalCount,
  currentPage,
}: {
  tag: string;
  posts: PostInfo[];
  totalCount: number;
  currentPage: number;
}) => (
  <PostList
    heading={`#${tag} の記事`}
    totalCount={totalCount}
    currentPage={currentPage}
    posts={posts}
    basePath={`/tags/${encodeURIComponent(tag)}/page`}
  />
);
