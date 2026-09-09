import { writable } from "svelte/store";
export type textLang = "cn" | "en" | "kr" | "jp";
export const currentLang = writable<textLang>("en");
