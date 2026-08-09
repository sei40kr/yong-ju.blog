import { Box, Flex } from "@chakra-ui/react";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Footer } from "~/components/layout/footer";
import { Header } from "~/components/layout/header";
import { Provider } from "~/components/provider";

import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";
import "@fontsource/noto-sans-jp/400.css";
import "@fontsource/noto-sans-jp/500.css";
import "@fontsource/noto-sans-jp/700.css";
import "@fontsource/noto-serif-jp/400.css";
import "@fontsource/noto-serif-jp/600.css";
import "@fontsource/noto-serif-jp/700.css";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://yong-ju.blog"),
  title: {
    default: "よんログ",
    template: "%s | よんログ",
  },
  icons: {
    icon: { url: "/favicon.svg", type: "image/svg+xml" },
  },
  manifest: "/manifest.json",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja" suppressHydrationWarning>
      <body>
        <Provider>
          <Flex direction="column" minH="100vh">
            <Header />
            <Box flex="1">{children}</Box>
            <Footer year={new Date().getFullYear()} />
          </Flex>
        </Provider>
      </body>
    </html>
  );
}
