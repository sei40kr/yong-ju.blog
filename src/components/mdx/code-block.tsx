"use client";

import {
  Box,
  CodeBlock as ChakraCodeBlock,
  Clipboard,
  IconButton,
} from "@chakra-ui/react";
import { useMemo } from "react";
import { LuCheck, LuCopy } from "react-icons/lu";

/** Chakra's adapter shape; `code` is markup, not source. */
export interface HighlightedCode {
  code: string;
  highlighted: boolean;
}

const CopyButton = ({ code }: { code: string }) => (
  <Clipboard.Root value={code} timeout={1000}>
    <Clipboard.Trigger asChild>
      <IconButton
        aria-label="コードをコピー"
        size="xs"
        variant="ghost"
        color="gray.400"
        _hover={{ bg: "whiteAlpha.200", color: "gray.100" }}
      >
        <Clipboard.Indicator copied={<LuCheck />}>
          <LuCopy />
        </Clipboard.Indicator>
      </IconButton>
    </Clipboard.Trigger>
  </Clipboard.Root>
);

// Chakra resolves code text through an adapter at render time — that is how
// Shiki reached the client bundle. This one just returns the server's result.
export const CodeBlock = ({
  code,
  highlighted,
}: {
  code: string;
  highlighted: HighlightedCode;
}) => {
  const adapter = useMemo(
    () => ({ getHighlighter: () => () => highlighted }),
    [highlighted],
  );

  return (
    <ChakraCodeBlock.AdapterProvider value={adapter}>
      <ChakraCodeBlock.Root
        code={code}
        size="md"
        my="7"
        bg="gray.900"
        borderColor="gray.800"
      >
        <ChakraCodeBlock.Content>
          <Box pos="absolute" top="2" insetEnd="2" zIndex="1">
            <CopyButton code={code} />
          </Box>
          <ChakraCodeBlock.Code fontSize="md">
            <ChakraCodeBlock.CodeText />
          </ChakraCodeBlock.Code>
        </ChakraCodeBlock.Content>
      </ChakraCodeBlock.Root>
    </ChakraCodeBlock.AdapterProvider>
  );
};
