<script lang="ts">
  import { base } from "$app/paths"
  import { currentLang } from "$lib/stores";
  import { getAvatarUrl } from "$lib/utils"
  import LangButtonBar from "$lib/LangButtonBar.svelte";
  import Photocard from "$lib/char/Photocard.svelte";
  import RatingFilter from "./RatingFilter.svelte";
  import FactionFilter from "./FactionFilter.svelte";
  import MobileFilterMenu from "./MobileFilterMenu.svelte";
  import charlist from "$lib/data/charlist.json";
  import miscdata from "$lib/data/miscdata.json";

  interface SingleChar {
    fullid: string,
    nameid: string,
    numberid: string,
    name: {
      en: string,
      cn: string,
      jp: string,
      kr: string,
    },
    nation: string | null,
    rating: number,
  }

  let filteredCharlist: SingleChar[];

  charlist.sort((a, b) => {
    // TODO: sort lexicographically by selected language
    if (a.name.en < b.name.en) {
      return -1;
    } else {
      return 1;
    }
  })

  $: filteredCharlist = filterCharlist(charlist, appliedFilters)
  $: nations = miscdata.nations.filter(n => !!n);

  type Filters = {
    name: string,
    rating: number[],
    nation: string[],
  }

  let appliedFilters: Filters = {
    name: "",
    rating: [],
    nation: [],
  }

  function filterCharlist(list: SingleChar[], filter: Filters) {
    return list.filter(char => {
      let include: boolean = true;

      if (filter.name != "") {
        const nameToSearch = filter.name.toLowerCase();
        const names = Object.values(char.name);
        include = names.some(name =>
          name.toLowerCase().includes(nameToSearch)
        );
      }

      if (include && filter.rating.length > 0) {
        include = filter.rating.includes(char.rating);
      }

      if (include && filter.nation.length > 0) {
        include = char.nation != null && filter.nation.includes(char.nation);
      }

      return include;
    })
  }

  // I can see Svelte wants this to be a FormEventHandler<HTMLInputElement>
  // but I can't figure out what type that makes e
  function handleSearchName(e: any) {
    const value = e.currentTarget.value;
    appliedFilters = { ...appliedFilters, name: value };
  }

  function handleFilterRatings(e: CustomEvent<number[]>) {
    const rating = e.detail;
    appliedFilters = { ...appliedFilters, rating };
  }

  function handleFilterNations(e: CustomEvent<string[]>) {
    const nation = e.detail;
    appliedFilters = { ...appliedFilters, nation };
  }
</script>

<svelte:head>
  <title>Operators - RIVA</title>
</svelte:head>

<main>
  <LangButtonBar />

  <article class="charpage">
    <h1>Operator List</h1>
    <section class="filter-options">

      <label for="name-search">Search</label>
      <input type="text" placeholder="Search"
        on:input={handleSearchName}
      />

      <RatingFilter on:onRatingsChange={handleFilterRatings} />

      <FactionFilter
        nations={nations}
        on:nationsChange={handleFilterNations}
      />
    </section>

    <ol class="charlist">
      {#each filteredCharlist as char}
      <li>
        <a data-sveltekit-preload-data="tap" href="{base}/operators/{char.nameid}">
          <Photocard
            imgsrc={getAvatarUrl(char.nameid, base)}
            text={char.name[$currentLang]}
          />
        </a>
      </li>
      {/each}
    </ol>
  </article>
</main>

<MobileFilterMenu
  on:input={handleSearchName}
  on:onRatingsChange={handleFilterRatings}
  on:nationsChange={handleFilterNations}
  nations={nations}
/>

<style>
  main {
    margin-top: 12px;
  }

  h1 {
    font-size: 2em;
    font-weight: 900;
    line-height: 1em;
    margin-bottom: 0.5em;
    margin-top: 0.5em;
  }

  ol {
    padding: 0;
  }

  li {
    display: block;
  }

  .charlist {
    display: grid;
    grid-template-columns: repeat(auto-fill, 86px);
    gap: 12px;
    justify-content: center;
    align-self: start;
  }

  .charlist > * {
    align-self: center;
  }

  .charlist a {
    text-decoration: none;
    color: inherit;
  }

  .charlist a > :global(*:hover) {
    transform: translateY(-5px);
  }

  .filter-options {
    margin-left: 4px;
    display: none;
  }

  .filter-options label {
    display: none;
  }

  input {
    background-color: #E5E5E5;
    border-radius: 8px;
    padding: 4px 12px;
    border: none;
  }

  input:focus, input:focus-visible {
    outline: solid 2px #CC495D;
  }

  @media (min-width: 800px) {
    .charlist {
      grid-template-columns: repeat(auto-fill, 110px);
    }

    .charlist :global(.photocard) {
      --width: 90px;
      font-size: 0.8em;
    }
  }

  @media (min-width: 1000px) {
    main {
      max-width: 1100px;
    }

    .charpage {
      display: grid;
      grid-template-columns: 300px 1fr;
      column-gap: 6%;
    }

    h1 {
      font-size: 2.2em;
      grid-column: 1 / -1;
    }

    .filter-options {
      display: initial;
      position: sticky;
      top: 60px;
      z-index: 89;
      align-self: start;
      max-height: calc(100vh - 60px);
      overflow-y: auto;
      overflow-x: clip;
      padding-right: 30px;
    }
  }
</style>
