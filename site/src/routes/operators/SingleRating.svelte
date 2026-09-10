<script lang="ts">
  import StarIcon from "$lib/icons/StarIcon.svelte";

  interface Props {
    rating: number;
    onclick: () => void;
  }

  let { rating, onclick }: Props = $props();
</script>

<button class="single-rating" {onclick}>
  {#each { length: rating }}
    <StarIcon />
  {/each}
</button>

<style>
  .single-rating {
    background-color: #333737;
    display: inline-flex;
    padding: 7px 14px;
    border-radius: 20px;

    border: none;
    color: inherit;
    cursor: pointer;
  }

  .single-rating:hover {
    background-color: #8a2929;
  }

  .single-rating > :global(*) {
    opacity: 0.5;
  }
</style>
