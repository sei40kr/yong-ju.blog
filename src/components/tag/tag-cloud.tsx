import { Wrap } from "@chakra-ui/react";
import { Tag } from "~/components/tag/tag";

export const TagCloud = ({
  tags,
  currentTag,
}: {
  tags: Map<string, number>;
  currentTag?: string;
}) => (
  <Wrap gap="2">
    {[...tags.entries()].map(([tag, count]) => (
      <Tag key={tag} tag={tag} count={count} selected={tag === currentTag} />
    ))}
  </Wrap>
);
