import { Box, Button, Clipboard, Flex, Heading, Text } from "@chakra-ui/react";
import { BsLink45Deg, BsTwitterX } from "react-icons/bs";
import type { PostHeading } from "~/repositories/post-infos";
import { Toc } from "./toc";

const SITE_URL = "https://yong-ju.blog";

const AsideHeading = ({ children }: { children: string }) => (
  <Heading
    as="h3"
    fontFamily="body"
    fontSize="md"
    fontWeight="semibold"
    letterSpacing="wider"
    textTransform="uppercase"
    color="fg.subtle"
    mb="2.5"
  >
    {children}
  </Heading>
);

export const PostSidebar = ({
  slug,
  title,
  headings,
  activeHeadingId,
}: {
  slug: string;
  title: string;
  headings: PostHeading[];
  activeHeadingId: string | null;
}) => {
  const url = `${SITE_URL}/posts/${slug}/`;
  const shareOnX = `https://x.com/intent/post?${new URLSearchParams({
    text: title,
    url,
  })}`;
  const shareOnHatena = `https://b.hatena.ne.jp/entry/s/${url.replace("https://", "")}`;

  return (
    <Flex
      as="aside"
      display={{ base: "none", lg: "flex" }}
      pos="sticky"
      top="20"
      direction="column"
      gap="6"
    >
      {headings.length > 0 && (
        <Box>
          <AsideHeading>目次</AsideHeading>
          <Toc headings={headings} activeHeadingId={activeHeadingId} />
        </Box>
      )}
      <Box>
        <AsideHeading>共有</AsideHeading>
        <Flex direction="column" gap="1.5" align="stretch">
          <Button
            asChild
            size="sm"
            fontSize="md"
            variant="surface"
            colorPalette="gray"
            justifyContent="flex-start"
          >
            <a href={shareOnX} target="_blank" rel="noopener noreferrer">
              <BsTwitterX />X で共有
            </a>
          </Button>
          <Button
            asChild
            size="sm"
            fontSize="md"
            variant="surface"
            colorPalette="cyan"
            justifyContent="flex-start"
          >
            <a href={shareOnHatena} target="_blank" rel="noopener noreferrer">
              <Text as="span" fontWeight="bold">
                B!
              </Text>
              はてなブックマーク
            </a>
          </Button>
          <Clipboard.Root value={url}>
            <Clipboard.Trigger asChild>
              <Button
                size="sm"
                fontSize="md"
                variant="surface"
                colorPalette="gray"
                justifyContent="flex-start"
                w="full"
              >
                <BsLink45Deg />
                <Clipboard.Indicator copied="コピーしました">
                  リンクをコピー
                </Clipboard.Indicator>
              </Button>
            </Clipboard.Trigger>
          </Clipboard.Root>
        </Flex>
      </Box>
    </Flex>
  );
};
