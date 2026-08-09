import { Accordion, Text } from "@chakra-ui/react";
import type { ReactNode } from "react";
import { BsChevronRight } from "react-icons/bs";

export const Details = ({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) => (
  <Accordion.Root collapsible my="7" variant="enclosed">
    <Accordion.Item value="details">
      <Accordion.ItemTrigger fontWeight="semibold" _hover={{ bg: "bg.subtle" }}>
        <Accordion.ItemIndicator _open={{ rotate: "90deg" }}>
          <BsChevronRight />
        </Accordion.ItemIndicator>
        <Text>{title}</Text>
      </Accordion.ItemTrigger>
      <Accordion.ItemContent
        fontSize="md"
        lineHeight="taller"
        color="fg.muted"
        css={{ "& > * > :last-child": { marginBottom: 0 } }}
      >
        <Accordion.ItemBody>{children}</Accordion.ItemBody>
      </Accordion.ItemContent>
    </Accordion.Item>
  </Accordion.Root>
);
