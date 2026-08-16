/**
 * An h2/h3 heading of a post, as listed in the table of contents. `id`
 * matches what rehype-slug emits at render time.
 */
export interface PostHeading {
  depth: 2 | 3;
  text: string;
  id: string;
}
