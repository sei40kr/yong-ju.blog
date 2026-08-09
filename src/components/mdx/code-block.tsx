"use client";

import {
  Box,
  CodeBlock as ChakraCodeBlock,
  IconButton,
} from "@chakra-ui/react";
import { useRef, useState } from "react";
import { LuCheck, LuCopy } from "react-icons/lu";
import { shikiAdapter } from "~/lib/shiki";

/**
 * Copy `text`, falling back to the legacy execCommand path when the async
 * Clipboard API is unavailable or rejects (e.g. NotAllowedError when the
 * document lacks focus or clipboard-write permission). Chakra's own
 * CopyTrigger leaves that rejection unhandled, which surfaces as a runtime
 * error, so we own the copy here instead.
 */
const copyText = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text);
    return;
  } catch {
    // fall through to the execCommand fallback below
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand("copy");
  } catch {
    // clipboard is unavailable in this context; nothing more we can do
  }
  document.body.removeChild(textarea);
};

const CopyButton = ({ code }: { code: string }) => {
  const [copied, setCopied] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  const handleCopy = async () => {
    await copyText(code);
    setCopied(true);
    clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => setCopied(false), 1000);
  };

  return (
    <IconButton
      aria-label="コードをコピー"
      size="xs"
      variant="ghost"
      color="gray.400"
      _hover={{ bg: "whiteAlpha.200", color: "gray.100" }}
      onClick={handleCopy}
    >
      {copied ? <LuCheck /> : <LuCopy />}
    </IconButton>
  );
};

export const CodeBlock = ({
  code,
  language,
}: {
  code: string;
  language?: string;
}) => (
  <ChakraCodeBlock.AdapterProvider value={shikiAdapter}>
    <ChakraCodeBlock.Root
      code={code}
      language={language}
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
