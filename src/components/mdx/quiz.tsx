"use client";

import {
  Badge,
  Box,
  Carousel,
  Flex,
  HStack,
  IconButton,
  Spacer,
  Text,
} from "@chakra-ui/react";
import { Children, type ReactNode, isValidElement, useState } from "react";
import {
  LuChevronLeft,
  LuChevronRight,
  LuLayers,
  LuRotateCcw,
} from "react-icons/lu";

const ToggleHint = ({ children }: { children: ReactNode }) => (
  <HStack gap="1" fontSize="sm" color="fg.subtle">
    <LuRotateCcw />
    {children}
  </HStack>
);

const Face = ({
  side,
  hidden,
  children,
}: {
  side: "question" | "answer";
  hidden: boolean;
  children: ReactNode;
}) => {
  const isAnswer = side === "answer";
  return (
    <Flex
      visibility={hidden ? "hidden" : undefined}
      gridArea="1 / 1"
      direction="column"
      gap="2"
      px="4"
      py="3"
      bg="bg.panel"
      borderWidth="1px"
      borderColor={isAnswer ? "green.200" : "border"}
      rounded="md"
    >
      {children}
    </Flex>
  );
};

const FaceBadge = ({ side }: { side: "question" | "answer" }) => (
  <Badge
    colorPalette={side === "answer" ? "green" : "blue"}
    size="md"
    fontWeight="semibold"
    flex="none"
    alignSelf="flex-start"
  >
    {side === "answer" ? "A" : "Q"}
  </Badge>
);

export const QuizItem = ({
  question,
  children,
}: {
  question: string;
  children: ReactNode;
}) => {
  const [revealed, setRevealed] = useState(false);
  const toggle = () => setRevealed((r) => !r);

  return (
    <Box
      role="button"
      tabIndex={0}
      aria-pressed={revealed}
      cursor="pointer"
      rounded="md"
      focusVisibleRing="inside"
      onClick={toggle}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggle();
        }
      }}
    >
      <Box display="grid">
        <Face side="question" hidden={revealed}>
          <FaceBadge side="question" />
          <Flex flex="1" align="center">
            <Text fontSize="md" textWrap="pretty">
              {question}
            </Text>
          </Flex>
          <ToggleHint>クリックで答え</ToggleHint>
        </Face>
        <Face side="answer" hidden={!revealed}>
          <HStack gap="2.5">
            <FaceBadge side="answer" />
            <Text fontSize="sm" color="fg.subtle">
              {question}
            </Text>
          </HStack>
          <Flex flex="1" align="center">
            <Box
              fontSize="md"
              lineHeight="taller"
              color="gray.800"
              textWrap="pretty"
              css={{
                "& > :first-child": { marginTop: 0 },
                "& > :last-child": { marginBottom: 0 },
              }}
            >
              {children}
            </Box>
          </Flex>
          <ToggleHint>クリックで問題に戻る</ToggleHint>
        </Face>
      </Box>
    </Box>
  );
};
const TRANSLATIONS = {
  nextTrigger: "次の問題",
  prevTrigger: "前の問題",
  indicator: (index: number) => `${index + 1} 問目へ`,
  item: (index: number, count: number) => `${count} 問中 ${index + 1} 問目`,
  autoplayStart: "自動再生を開始",
  autoplayStop: "自動再生を停止",
};

export const Quiz = ({
  title = "この記事のクイズ",
  children,
}: {
  title?: string;
  children: ReactNode;
}) => {
  const items = Children.toArray(children).filter(isValidElement);

  return (
    <Carousel.Root
      as="section"
      slideCount={items.length}
      translations={TRANSLATIONS}
      my="7"
      p="3"
      pt="2"
      bg="bg.subtle"
      borderWidth="1px"
      rounded="md"
    >
      <HStack gap="2">
        <Box color="blue.600" flex="none">
          <LuLayers size="16" />
        </Box>
        <Text fontFamily="heading" fontSize="md" fontWeight="semibold">
          {title}
        </Text>
        <Spacer />
        <Carousel.ProgressText fontSize="sm" color="fg.subtle" />
      </HStack>
      <Carousel.ItemGroup>
        {items.map((item, i) => (
          <Carousel.Item key={item.key} index={i}>
            {item}
          </Carousel.Item>
        ))}
      </Carousel.ItemGroup>
      <Carousel.Control justifyContent="space-between">
        <Carousel.PrevTrigger asChild>
          <IconButton size="xs" variant="outline">
            <LuChevronLeft />
          </IconButton>
        </Carousel.PrevTrigger>
        <Carousel.IndicatorGroup gap="1.5">
          {items.map((item, i) => (
            <Carousel.Indicator
              key={item.key}
              index={i}
              colorPalette="blue"
              boxSize="1.5"
              bg="border.emphasized"
              transitionProperty="width"
              transitionDuration="moderate"
              _current={{ w: "4.5", bg: "colorPalette.solid" }}
            />
          ))}
        </Carousel.IndicatorGroup>
        <Carousel.NextTrigger asChild>
          <IconButton size="xs" variant="outline">
            <LuChevronRight />
          </IconButton>
        </Carousel.NextTrigger>
      </Carousel.Control>
    </Carousel.Root>
  );
};
