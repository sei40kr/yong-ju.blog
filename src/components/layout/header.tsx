import { Box, Flex, HStack, Link, Spacer, Text } from "@chakra-ui/react";
import NextLink from "next/link";

const NavLink = ({ href, label }: { href: string; label: string }) => (
  <Link
    asChild
    color="fg.muted"
    _hover={{ color: "fg", textDecoration: "none" }}
  >
    <NextLink href={href}>{label}</NextLink>
  </Link>
);

export const Header = () => (
  <Box
    as="header"
    pos="sticky"
    top="0"
    zIndex="20"
    bg="rgba(255, 255, 255, 0.86)"
    backdropFilter="blur(8px)"
    borderBottomWidth="1px"
  >
    <Flex maxW="5xl" mx="auto" px="6" h="14" align="center" gap="7">
      <Link asChild _hover={{ textDecoration: "none" }}>
        <NextLink href="/">
          <Text
            as="span"
            fontFamily="heading"
            fontSize="lg"
            fontWeight="bold"
            letterSpacing="tight"
            color="fg"
          >
            よんログ
          </Text>
        </NextLink>
      </Link>
      <Spacer />
      <HStack as="nav" gap="5" fontSize="md">
        <NavLink href="/" label="記事" />
        <NavLink href="/tags" label="タグ" />
      </HStack>
    </Flex>
  </Box>
);
