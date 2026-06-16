// Slug consistente para tags/URLs: sem acento, minusculo, hifenizado.
const COMBINING_MARKS = new RegExp('[\\u0300-\\u036f]', 'g');

export function slugify(s: string): string {
  return s
    .normalize('NFD')
    .replace(COMBINING_MARKS, '') // remove diacriticos
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}
