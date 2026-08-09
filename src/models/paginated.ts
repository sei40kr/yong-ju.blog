export interface Paginated<T> {
  totalCount: number;
  items: T[];
}

/**
 * Posts shown per list page. Lives here rather than in the post list component:
 * that component is a client module, and a client module's exports become
 * client references when imported by a server component — reading it from
 * `generateStaticParams` would yield a reference instead of the number.
 */
export const POSTS_PER_PAGE = 10;
