import fa from "./fa";
import ps from "./ps";
import en from "./en";

export type Locale = "fa" | "ps" | "en";

const dictionaries = { fa, ps, en };

export function getDictionary(locale: Locale) {
  return dictionaries[locale] ?? dictionaries.fa;
}

export function pickLang(
  obj: Record<string, any>,
  prefix: string,
  lang: Locale
): string {
  const key = `${prefix}_${lang}`;
  const fallback = `${prefix}_fa`;
  return obj[key] ?? obj[fallback] ?? "";
}
