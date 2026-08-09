import { Flex, HStack, Link, Text } from "@chakra-ui/react";
import NextLink from "next/link";
import { Box } from "@chakra-ui/react";

const FooterLink = ({ href, label }: { href: string; label: string }) => (
  <Link
    asChild
    color="fg.muted"
    _hover={{ color: "fg", textDecoration: "none" }}
  >
    <NextLink href={href}>{label}</NextLink>
  </Link>
);

export const Footer = ({ year }: { year: number }) => (
  <Box as="footer" borderTopWidth="1px" bg="bg.subtle">
    <Flex
      maxW="5xl"
      mx="auto"
      px="6"
      py="8"
      align="center"
      justify="space-between"
      gap="6"
      wrap="wrap"
    >
      <Text fontSize="md" color="fg.subtle">
        © {year} よんじゅ (成 英柱)
      </Text>
      <HStack gap="4.5" fontSize="md">
        <FooterLink href="/" label="記事" />
        <FooterLink href="/tags" label="タグ" />
      </HStack>
    </Flex>
  </Box>
);
