import { SvelteSet } from "svelte/reactivity";

export const nation_filter_set: SvelteSet<string> = $state(new SvelteSet());
export const rarity_filter_set: SvelteSet<number> = $state(new SvelteSet());
