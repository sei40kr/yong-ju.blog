"use client";

import {
  Box,
  ButtonGroup,
  Flex,
  Grid,
  Heading,
  IconButton,
  Pagination,
  Text,
} from "@chakra-ui/react";
import { BsChevronLeft, BsChevronRight } from "react-icons/bs";
import { PostItem } from "~/components/post-list/post-item";
import { PostListSidebar } from "~/components/post-list/post-list-sidebar";
import { POSTS_PER_PAGE } from "~/models/paginated";
import type { PostInfo } from "~/models/post-info";

/**
 * A page of posts: section heading, result range, the items, and pagination.
 * Shared by the home page and the tag archive so both list posts identically.
 *
 * Static-site pagination: every page is pre-rendered, so Chakra renders each
 * control as a link (`type="link"` + `getPageUrl`) rather than a client-side
 * page change, filling in the hrefs and disabling the prev/next ends.
 */
export const PostList = ({
  heading,
  totalCount,
  currentPage,
  posts,
  basePath,
}: {
  heading: string;
  totalCount: number;
  currentPage: number;
  posts: PostInfo[];
  basePath: string;
}) => {
  const totalPages = Math.ceil(totalCount / POSTS_PER_PAGE);
  const from = (currentPage - 1) * POSTS_PER_PAGE + 1;
  const to = Math.min(currentPage * POSTS_PER_PAGE, totalCount);

  return (
    <>
      <Flex
        align="baseline"
        justify="space-between"
        gap="4"
        pb="3"
        borderBottomWidth="1px"
      >
        <Heading
          as="h2"
          fontFamily="body"
          fontSize="md"
          fontWeight="semibold"
          letterSpacing="wider"
          color="fg.muted"
        >
          {heading}
        </Heading>
        <Text fontSize="md" color="fg.subtle" whiteSpace="nowrap">
          {totalCount > 0 ? `${totalCount} 件中 ${from}–${to} 件` : "0 件"}
        </Text>
      </Flex>
      {posts.map((post) => (
        <PostItem key={post.slug} post={post} />
      ))}
      {totalPages > 1 && (
        <Pagination.Root
          count={totalCount}
          pageSize={POSTS_PER_PAGE}
          page={currentPage}
          type="link"
          getPageUrl={({ page }) => `${basePath}/${page}`}
          display="flex"
          justifyContent="center"
          pt="7"
        >
          <ButtonGroup variant="ghost" size="md">
            <Pagination.PrevTrigger asChild>
              <IconButton
                aria-label="前のページ"
                asChild
                _icon={{ boxSize: "4" }}
              >
                <a>
                  <BsChevronLeft />
                </a>
              </IconButton>
            </Pagination.PrevTrigger>
            <Pagination.Items
              render={(page) => (
                <IconButton
                  asChild
                  variant={page.value === currentPage ? "outline" : "ghost"}
                >
                  <a>{page.value}</a>
                </IconButton>
              )}
            />
            <Pagination.NextTrigger asChild>
              <IconButton
                aria-label="次のページ"
                asChild
                _icon={{ boxSize: "4" }}
              >
                <a>
                  <BsChevronRight />
                </a>
              </IconButton>
            </Pagination.NextTrigger>
          </ButtonGroup>
        </Pagination.Root>
      )}
    </>
  );
};

/** Home / paginated post list, matching the design's home layout. */
export const PostListPage = ({
  totalCount,
  currentPage,
  posts,
  basePath,
  tags,
}: {
  totalCount: number;
  currentPage: number;
  posts: PostInfo[];
  basePath: string;
  tags: Map<string, number>;
}) => (
  <Grid
    as="main"
    maxW="5xl"
    mx="auto"
    px="6"
    pt="12"
    pb="24"
    templateColumns={{ base: "minmax(0, 1fr)", lg: "minmax(0, 1fr) 288px" }}
    gap="14"
    alignItems="start"
  >
    <Box>
      <PostList
        heading="最新の記事"
        totalCount={totalCount}
        currentPage={currentPage}
        posts={posts}
        basePath={basePath}
      />
    </Box>
    <PostListSidebar tags={tags} />
  </Grid>
);
