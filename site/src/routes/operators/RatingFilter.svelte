<script lang="ts">
  import StarIcon from "$lib/icons/StarIcon.svelte";
  import SingleRating from "./SingleRating.svelte";
  import { rarity_filter_set } from "./filterstate.svelte";

  const ratings: number[] = [1, 2, 3, 4, 5, 6];

  let selectedStatus: boolean[] = $state(ratings.map((_) => false));

  function onSelect(idx: number) {
    if (!rarity_filter_set.has(ratings[idx])) {
      rarity_filter_set.add(ratings[idx]);
    }

    // Reset selected display
    selectedStatus = ratings.map((_) => false);
  }

  function onHover(selectedIdx: number) {
    selectedStatus = selectedStatus.map((_, idx) => {
      return idx <= selectedIdx;
    });
  }

  function onUnhover() {
    // Reset selected display
    selectedStatus = ratings.map((_) => false);
  }

  function removeRating(ratingToRemove: number) {
    rarity_filter_set.delete(ratingToRemove);
  }
</script>

<h2>Rarity</h2>
<div class="selector">
  {#each ratings as _, index}
    <button
      onclick={() => onSelect(index)}
      onpointerover={() => onHover(index)}
      onpointerleave={onUnhover}
      class:selected={selectedStatus[index]}
    >
      <StarIcon />
    </button>
  {/each}
</div>

<ol>
  {#each rarity_filter_set as rating}
    <li><SingleRating onclick={() => removeRating(rating)} {rating} /></li>
  {/each}
</ol>

<style>
  h2 {
    font-size: 1.4em;
    border-bottom: solid 2px;
  }

  button {
    color: var(--color-text);

    background: none;
    border: none;
    cursor: pointer;
    opacity: 0.25;

    padding: 0;
    margin-right: -2px;
  }

  button:hover,
  button.selected {
    opacity: 1;
  }

  .selector {
    display: flex;
  }

  ol {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
</style>
