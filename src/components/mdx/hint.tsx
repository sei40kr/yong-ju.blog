import { Alert } from "@chakra-ui/react";
import type { ReactNode } from "react";

type HintLevel = "info" | "warn" | "danger";

const HINT_META: Record<
  HintLevel,
  { status: "info" | "warning" | "error"; title: string }
> = {
  info: { status: "info", title: "補足" },
  warn: { status: "warning", title: "注意" },
  danger: { status: "error", title: "警告" },
};

export const Hint = ({
  level,
  children,
}: {
  level: HintLevel;
  children: ReactNode;
}) => {
  const { status, title } = HINT_META[level];

  return (
    <Alert.Root status={status} variant="surface" my="7" rounded="md">
      <Alert.Indicator />
      <Alert.Content>
        <Alert.Title>{title}</Alert.Title>
        <Alert.Description
          display="block"
          fontSize="md"
          lineHeight="taller"
          color="gray.800"
          css={{
            "& p": { marginBottom: "2" },
            "& p:last-of-type": { marginBottom: 0 },
          }}
        >
          {children}
        </Alert.Description>
      </Alert.Content>
    </Alert.Root>
  );
};
