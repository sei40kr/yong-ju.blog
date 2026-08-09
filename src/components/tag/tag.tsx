import { Tag as ChakraTag, Text } from "@chakra-ui/react";
import NextLink from "next/link";

export const Tag = ({
  tag,
  count,
  selected = false,
}: {
  tag: string;
  count?: number;
  selected?: boolean;
}) => (
  <ChakraTag.Root
    asChild
    rounded="full"
    px="2.5"
    py="1"
    variant={selected ? "solid" : "outline"}
    colorPalette={selected ? "blue" : undefined}
    {...(selected
      ? {}
      : {
          color: "fg.muted",
          _hover: {
            color: "blue.600",
            shadow: "inset 0 0 0px 1px var(--chakra-colors-blue-400)",
          },
        })}
  >
    <NextLink href={`/tags/${encodeURIComponent(tag)}`}>
      {/* recipe が label スロットに textStyle: xs を当てるため、サイズはここで上書きする */}
      <ChakraTag.Label textStyle="md">
        #{tag}
        {count !== undefined && (
          <Text as="span" opacity="0.55" ml="1">
            {count}
          </Text>
        )}
      </ChakraTag.Label>
    </NextLink>
  </ChakraTag.Root>
);
