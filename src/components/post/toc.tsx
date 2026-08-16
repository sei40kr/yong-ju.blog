"use client";

import { Box, Flex, Link } from "@chakra-ui/react";
import { useEffect, useRef } from "react";
import type { PostHeading } from "~/repositories/post-infos";

export const Toc = ({
  headings,
  activeHeadingId,
}: {
  headings: PostHeading[];
  activeHeadingId: string | null;
}) => {
  const rootRef = useRef<HTMLDivElement>(null);
  const activeLinkRef = useRef<HTMLAnchorElement>(null);

  // Center the active item. scrollIntoView would also scroll the page.
  useEffect(() => {
    const root = rootRef.current;
    const link = activeLinkRef.current;
    if (!root || !link) return;
    const rootRect = root.getBoundingClientRect();
    const linkRect = link.getBoundingClientRect();
    root.scrollTo({
      top:
        root.scrollTop +
        (linkRect.top + linkRect.height / 2) -
        (rootRect.top + rootRect.height / 2),
      behavior: "smooth",
    });
  }, [activeHeadingId]);

  // Border on the scrollbox itself would clip the active link's ml="-1px" overlay.
  return (
    <Box ref={rootRef} overflowY="auto" minH="0">
      <Flex direction="column" gap="0.5" borderLeftWidth="1px">
        {headings.map(({ depth, text, id }) => {
          const isActive = id === activeHeadingId;
          return (
            <Link
              key={id}
              ref={isActive ? activeLinkRef : undefined}
              href={`#${id}`}
              py="1"
              pr="3"
              pl={depth === 3 ? "6" : "3"}
              fontSize="md"
              lineHeight="tall"
              colorPalette="blue"
              color={
                isActive
                  ? "colorPalette.600"
                  : depth === 3
                    ? "fg.subtle"
                    : "fg.muted"
              }
              borderLeftWidth={isActive ? "2px" : undefined}
              borderColor="colorPalette.600"
              ml={isActive ? "-1px" : undefined}
              _hover={{
                color: isActive ? "colorPalette.600" : "fg",
                textDecoration: "none",
              }}
            >
              {text}
            </Link>
          );
        })}
      </Flex>
    </Box>
  );
};
