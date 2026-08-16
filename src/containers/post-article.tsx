"use client";

import { Box, Grid } from "@chakra-ui/react";
import {
  type ReactNode,
  type RefObject,
  useEffect,
  useRef,
  useState,
} from "react";
import { PostSidebar } from "~/components/post/post-sidebar";
import type { PostHeading } from "~/models/post-heading";

// Track the heading in view, scoped to the body so the observer never
// reaches a sibling subtree via a global `document` lookup.
const useActiveHeading = (
  headings: PostHeading[],
  bodyRef: RefObject<HTMLElement | null>,
) => {
  const [activeHeadingId, setActiveHeadingId] = useState<string | null>(
    headings[0]?.id ?? null,
  );

  useEffect(() => {
    const body = bodyRef.current;
    if (!body) return;

    // Detection band just below the sticky header.
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.find((entry) => entry.isIntersecting);
        if (visible) setActiveHeadingId(visible.target.id);
      },
      { rootMargin: "-100px 0px -66% 0px" },
    );

    for (const { id } of headings) {
      const el = body.querySelector(`#${CSS.escape(id)}`);
      if (el) observer.observe(el);
    }
    return () => observer.disconnect();
  }, [headings, bodyRef]);

  return activeHeadingId;
};

// Two-column reading view: post body plus its table of contents, linked by
// scroll tracking. Body is passed through as server-rendered children.
export const PostArticle = ({
  slug,
  title,
  headings,
  children,
}: {
  slug: string;
  title: string;
  headings: PostHeading[];
  children: ReactNode;
}) => {
  const bodyRef = useRef<HTMLDivElement>(null);
  const activeHeadingId = useActiveHeading(headings, bodyRef);

  return (
    <Grid
      as="main"
      maxW="5xl"
      mx="auto"
      px="6"
      pt="10"
      pb="24"
      templateColumns={{ base: "minmax(0, 1fr)", lg: "minmax(0, 1fr) 220px" }}
      gap="14"
      alignItems="start"
    >
      <Box ref={bodyRef} maxW="3xl">
        {children}
      </Box>
      <PostSidebar
        slug={slug}
        title={title}
        headings={headings}
        activeHeadingId={activeHeadingId}
      />
    </Grid>
  );
};
