"use client";

import { Alert, Box, Center, Spinner } from "@chakra-ui/react";
import { useEffect, useId, useState } from "react";

// Mermaid needs a DOM (it measures text and path geometry to lay the graph
// out), so it cannot run during the static export — every diagram renders in
// the browser. The import is dynamic and module-level memoized: the chunk is
// fetched once, and only on pages that actually contain a diagram.
let mermaidPromise: Promise<typeof import("mermaid").default> | undefined;

const loadMermaid = () => {
  mermaidPromise ??= import("mermaid").then(({ default: mermaid }) => {
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
    return mermaid;
  });

  return mermaidPromise;
};

type State =
  | { status: "loading" }
  | { status: "done"; svg: string }
  | { status: "error"; message: string };

export const Mermaid = ({ code }: { code: string }) => {
  const [state, setState] = useState<State>({ status: "loading" });
  // Mermaid puts this in a DOM id and then queries it back, so it has to be a
  // plain identifier — React's useId is decorated with characters that break
  // the selector.
  const id = `mermaid-${useId().replace(/[^a-zA-Z0-9]/g, "")}`;

  useEffect(() => {
    let cancelled = false;

    setState({ status: "loading" });
    loadMermaid()
      .then((mermaid) => mermaid.render(id, code))
      .then(({ svg }) => {
        if (!cancelled) {
          setState({ status: "done", svg });
        }
      })
      .catch((error: unknown) => {
        // A failed render leaves its scratch element behind in <body>.
        document.getElementById(`d${id}`)?.remove();
        if (!cancelled) {
          setState({
            status: "error",
            message: error instanceof Error ? error.message : String(error),
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [code, id]);

  if (state.status === "loading") {
    return (
      <Center minH="32">
        <Spinner size="lg" colorPalette="blue" color="colorPalette.solid" />
      </Center>
    );
  }

  if (state.status === "error") {
    return (
      <Alert.Root status="error" variant="surface" rounded="md">
        <Alert.Indicator />
        <Alert.Content>
          <Alert.Title>図を描画できませんでした</Alert.Title>
          <Alert.Description fontSize="md" fontFamily="mono">
            {state.message}
          </Alert.Description>
        </Alert.Content>
      </Alert.Root>
    );
  }

  // Mermaid sizes the <svg> with width="100%" + an inline max-width, so it
  // scales down to whatever width it is given and never overflows.
  return (
    <Box
      css={{ "& svg": { display: "block", marginInline: "auto" } }}
      // Labels are sanitized by Mermaid itself (securityLevel: "strict").
      dangerouslySetInnerHTML={{ __html: state.svg }}
    />
  );
};
