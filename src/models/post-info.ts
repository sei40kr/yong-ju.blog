export interface PostInfo {
  id: string;
  title: string;
  date: Date;
  categories: Set<string>;
  tags: Set<string>;
}
