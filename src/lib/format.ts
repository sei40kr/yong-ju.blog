const DATE_FORMATTER = new Intl.DateTimeFormat("ja-JP", {
  year: "numeric",
  month: "long",
  day: "numeric",
  // Post dates are authored in JST. Pin the time zone so the rendered date
  // doesn't depend on the time zone of the build machine.
  timeZone: "Asia/Tokyo",
});

const MS_PER_DAY = 24 * 60 * 60 * 1000;

/** Past this many days "N日前" stops being easier to place than the date. */
const RELATIVE_DAYS = 30;

/**
 * A recent post reads better as "3日前" than as a date; an older one is the
 * other way round. Rendered at build time, so "今日" means the day of the
 * build — fine for a site that is rebuilt whenever a post is added.
 */
export const humanizeDate = (date: Date, now: Date = new Date()): string => {
  const days = Math.floor((now.getTime() - date.getTime()) / MS_PER_DAY);

  if (days < 0 || days >= RELATIVE_DAYS) {
    return DATE_FORMATTER.format(date);
  }
  if (days === 0) {
    return "今日";
  }
  if (days === 1) {
    return "昨日";
  }
  return `${days}日前`;
};
