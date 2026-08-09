export interface PostInfo {
  slug: string;
  title: string;
  date: Date;
  tags: Set<string>;
  excerpt: string;
  readMinutes: number;
}
