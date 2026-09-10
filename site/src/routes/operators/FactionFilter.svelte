<script lang="ts">
  import { asset } from "$app/paths";
  import { nations } from "$lib/data/miscdata.json";
  import { nation_filter_set } from "./filterstate.svelte";
</script>

<h2>Nation</h2>
<div class="nations">
  {#each nations as nation}
    <button
      onclick={() => {
        if (nation_filter_set.has(nation)) {
          nation_filter_set.delete(nation);
        } else {
          nation_filter_set.add(nation);
        }
      }}
      class:selected={nation_filter_set.has(nation)}
    >
      <img src={asset(`/images/factions/${nation}.webp`)} alt={nation} />
    </button>
  {/each}
</div>

<style>
  h2 {
    font-size: 1.4em;
    border-bottom: solid 2px;
  }

  .nations {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(77px, 1fr));
  }

  .nations button {
    border: none;
    background: none;
    opacity: 0.25;
    cursor: pointer;
  }

  .nations button:hover {
    opacity: 0.75;
  }

  .nations button.selected {
    opacity: 1;
  }

  .nations img {
    max-width: 100%;
  }
</style>
