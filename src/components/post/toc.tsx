import { Flex, Link } from "@chakra-ui/react";
import type { PostHeading } from "~/repositories/post-infos";

export const Toc = ({
  headings,
  activeHeadingId,
}: {
  headings: PostHeading[];
  activeHeadingId: string | null;
}) => (
  <Flex direction="column" gap="0.5" borderLeftWidth="1px">
    {headings.map(({ depth, text, id }) => {
      const isActive = id === activeHeadingId;
      return (
        <Link
          key={id}
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
);
