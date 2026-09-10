import { writable } from "svelte/store";
export type textLang = "en" | "cn" | "jp" | "kr";
export const currentLang = writable<textLang>("en");
