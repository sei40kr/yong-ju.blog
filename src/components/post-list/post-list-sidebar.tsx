import {
  Avatar,
  Box,
  Card,
  Flex,
  HStack,
  Heading,
  Link,
  Text,
  Wrap,
} from "@chakra-ui/react";
import NextLink from "next/link";
import { BsGithub, BsLinkedin } from "react-icons/bs";
import { Tag } from "~/components/tag/tag";

const SOCIAL_LINKS = [
  { icon: BsGithub, label: "GitHub", href: "https://github.com/sei40kr" },
  {
    icon: BsLinkedin,
    label: "LinkedIn",
    href: "https://www.linkedin.com/in/sei40kr",
  },
];

const SIDEBAR_TAG_LIMIT = 14;

// Gravatar for sei40kr@gmail.com (SHA-256 of the lower-cased address).
// Requested at 2x the 40px avatar so it stays sharp on retina displays.
const AVATAR_URL =
  "https://www.gravatar.com/avatar/d239621fe0243510aba6c1bb0aaf63eb92c1c4e784b9c77c36aa472387f4fcf1?s=80";

export const PostListSidebar = ({ tags }: { tags: Map<string, number> }) => (
  <Flex as="aside" pos={{ lg: "sticky" }} top="20" direction="column" gap="7">
    <Card.Root size="sm" rounded="md">
      <Card.Body gap="3">
        <HStack gap="3">
          <Avatar.Root bg="gray.900" color="white">
            <Avatar.Fallback fontSize="md" fontWeight="semibold">
              四
            </Avatar.Fallback>
            <Avatar.Image src={AVATAR_URL} alt="よんじゅ" />
          </Avatar.Root>
          <Box>
            <Text fontSize="md" fontWeight="semibold">
              よんじゅ
            </Text>
            <Text fontSize="md" color="fg.subtle">
              ソフトウェアエンジニア
            </Text>
          </Box>
        </HStack>
        <HStack gap="4" fontSize="md">
          {SOCIAL_LINKS.map(({ icon: Icon, label, href }) => (
            <Link
              key={label}
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              display="inline-flex"
              alignItems="center"
              gap="1.5"
              color="fg.muted"
              _hover={{ color: "fg", textDecoration: "none" }}
            >
              <Icon />
              {label}
            </Link>
          ))}
        </HStack>
      </Card.Body>
    </Card.Root>
    <Box>
      <Heading
        as="h3"
        fontFamily="body"
        fontSize="md"
        fontWeight="semibold"
        letterSpacing="wider"
        textTransform="uppercase"
        color="fg.muted"
        mb="3"
      >
        タグ
      </Heading>
      <Wrap gap="1.5">
        {[...tags.entries()].slice(0, SIDEBAR_TAG_LIMIT).map(([tag, count]) => (
          <Tag key={tag} tag={tag} count={count} />
        ))}
      </Wrap>
      <Link
        asChild
        display="inline-block"
        mt="3"
        fontSize="md"
        color="blue.600"
        _hover={{ textDecoration: "underline" }}
      >
        <NextLink href="/tags">すべてのタグを見る →</NextLink>
      </Link>
    </Box>
  </Flex>
);
