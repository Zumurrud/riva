<script lang="ts">
  import { createBubbler } from "svelte/legacy";

  const bubble = createBubbler();
  import Drawer from "svelte-drawer-component";
  import FilterIcon from "$lib/icons/FilterIcon.svelte";
  import CloseFilterIcon from "$lib/icons/CloseFilterIcon.svelte";
  import RatingFilter from "./RatingFilter.svelte";
  import FactionFilter from "./FactionFilter.svelte";

  let filterDrawerOpen: boolean = $state(false);
</script>

<button class="search-button" onclick={() => (filterDrawerOpen = true)}>
  <FilterIcon />
</button>

<div class="drawer-menu">
  <Drawer
    open={filterDrawerOpen}
    placement="right"
    size="80%"
    on:clickAway={() => (filterDrawerOpen = false)}
  >
    <button
      class="close-drawer-button"
      onclick={() => (filterDrawerOpen = false)}
    >
      <CloseFilterIcon />
    </button>

    <div class="mobile-search">
      <input type="text" placeholder="Search" oninput={bubble("input")} />
    </div>

    <RatingFilter />
    <FactionFilter />
  </Drawer>
</div>

<style>
  .search-button,
  .close-drawer-button {
    width: 82px;
    height: 48px;
    background-color: #e8e5dc;
    color: #070707;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    border: none;

    position: fixed;
    bottom: 16px;
    right: 0;

    cursor: pointer;
  }

  .close-drawer-button {
    position: initial;
    bottom: 16px;
  }

  .search-button :global(svg),
  .close-drawer-button :global(svg) {
    font-size: 1.5em;
  }

  .drawer-menu :global(.drawer .panel) {
    background: rgba(0, 0, 0, 0.9);
    color: var(--color-text);
    padding: 30px 20px;
    /* max-height: 100vh;
    overflow-y: auto;*/
  }

  @media (min-width: 1000px) {
    .search-button {
      display: none;
    }
  }

  .mobile-search {
    margin-top: 24px;
  }

  .mobile-search input {
    background-color: #e5e5e5;
    border-radius: 8px;
    padding: 4px 12px;
    border: none;
  }

  .mobile-search input:focus,
  input:focus-visible {
    outline: solid 2px #cc495d;
  }
</style>
