/**
 * `next dev` matches an incoming URL against `generateStaticParams` without
 * percent-decoding the path segments, so a request to `/tags/%E6%95%B0%E5%AD%A6`
 * never matches the raw param `数学` and dev responds with a 500
 * ("missing param ... required with `output: export`").
 *
 * The production export must keep the raw values, though: `next build` writes
 * param values literally as directory names, and S3 percent-decodes request
 * URIs before looking up keys, so the exported directories must be the raw
 * (unencoded) strings.
 *
 * Hence: raw params always, plus percent-encoded variants in dev only.
 */
export const withDevEncodedVariants = <T extends Record<string, string>>(
  params: T[],
): T[] => {
  if (process.env.NODE_ENV !== "development") {
    return params;
  }

  const seen = new Set(params.map((param) => JSON.stringify(param)));
  const encodedParams = params
    .map(
      (param) =>
        Object.fromEntries(
          Object.entries(param).map(([key, value]) => [
            key,
            encodeURIComponent(value),
          ]),
        ) as T,
    )
    .filter((param) => !seen.has(JSON.stringify(param)));

  return [...params, ...encodedParams];
};
