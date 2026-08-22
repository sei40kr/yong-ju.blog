import {
  Flex,
  HStack,
  LinkBox,
  LinkOverlay,
  Separator,
  Text,
} from "@chakra-ui/react";
import NextLink from "next/link";
import { humanizeDate } from "~/lib/format";
import { Tag } from "~/components/tag/tag";
import type { PostData } from "~/models/post-data";

export const PostItem = ({
  post: { slug, title, date, tags, excerpt, readMinutes },
}: {
  post: PostData;
}) => (
  <LinkBox
    as="article"
    className="group"
    mx="-4.5"
    py="5"
    pr="4.5"
    pl="4"
    borderBottomWidth="1px"
    borderBottomColor="border.muted"
    borderLeftWidth="2px"
    borderLeftColor="transparent"
    _hover={{ borderLeftColor: "blue.500", bg: "bg.subtle" }}
  >
    <Flex align="center" gap="2.5" mb="2" wrap="wrap">
      {/* Rendered conditionally: an empty tag list would still consume the
          Flex gap and shift the metadata to the right. */}
      {tags.size > 0 && (
        // Lift above the card-wide LinkOverlay so the tag links stay clickable.
        <HStack gap="1.5" pos="relative" zIndex="1">
          {[...tags].slice(0, 2).map((tag) => (
            <Tag key={tag} tag={tag} />
          ))}
        </HStack>
      )}
      <HStack gap="2" fontSize="md" color="fg.subtle">
        <span>{humanizeDate(date)}</span>
        <Separator orientation="vertical" height="3.5" />
        <span>{readMinutes} min</span>
      </HStack>
    </Flex>
    <Text
      as="h3"
      fontFamily="heading"
      fontSize="xl"
      fontWeight="semibold"
      lineHeight="moderate"
      letterSpacing="tight"
      mb="1.5"
      _groupHover={{ color: "blue.700" }}
    >
      <LinkOverlay asChild>
        <NextLink href={`/posts/${slug}`}>{title}</NextLink>
      </LinkOverlay>
    </Text>
    <Text
      fontSize="md"
      lineHeight="taller"
      color="fg.muted"
      textWrap="pretty"
      lineClamp="2"
    >
      {excerpt}
    </Text>
  </LinkBox>
);
