"use client";

import createCache from "@emotion/cache";
import { CacheProvider } from "@emotion/react";
import { ChakraProvider } from "@chakra-ui/react";
import { useServerInsertedHTML } from "next/navigation";
import { type ReactNode, useState } from "react";
import { system } from "~/theme";

interface InsertedStyle {
  name: string;
  isGlobal: boolean;
}

/**
 * Emotion SSR registry for the App Router: collect the styles emitted during
 * server rendering and re-emit them in <head> via useServerInsertedHTML.
 * Without this, Emotion inlines <style> tags between sibling elements, which
 * breaks hydration (and child-indexed selectors) under React 19.
 */
const useEmotionCache = () => {
  const [registry] = useState(() => {
    const cache = createCache({ key: "css" });
    cache.compat = true;

    let inserted: InsertedStyle[] = [];
    const prevInsert = cache.insert;
    cache.insert = (...args) => {
      const [selector, serialized] = args;
      if (cache.inserted[serialized.name] === undefined) {
        inserted.push({ name: serialized.name, isGlobal: !selector });
      }
      return prevInsert(...args);
    };

    const flush = () => {
      const prevInserted = inserted;
      inserted = [];
      return prevInserted;
    };

    return { cache, flush };
  });

  useServerInsertedHTML(() => {
    const names = registry.flush();
    if (names.length === 0) {
      return null;
    }

    let styles = "";
    let dataEmotionAttribute = registry.cache.key;
    const globals: { name: string; style: string }[] = [];

    for (const { name, isGlobal } of names) {
      const style = registry.cache.inserted[name];
      if (typeof style !== "string") {
        continue;
      }
      if (isGlobal) {
        globals.push({ name, style });
      } else {
        styles += style;
        dataEmotionAttribute += ` ${name}`;
      }
    }

    return (
      <>
        {globals.map(({ name, style }) => (
          <style
            key={name}
            data-emotion={`${registry.cache.key}-global ${name}`}
            dangerouslySetInnerHTML={{ __html: style }}
          />
        ))}
        {styles !== "" && (
          <style
            data-emotion={dataEmotionAttribute}
            dangerouslySetInnerHTML={{ __html: styles }}
          />
        )}
      </>
    );
  });

  return registry.cache;
};

export const Provider = ({ children }: { children: ReactNode }) => {
  const cache = useEmotionCache();

  return (
    <CacheProvider value={cache}>
      <ChakraProvider value={system}>{children}</ChakraProvider>
    </CacheProvider>
  );
};
