<script lang="ts">
  import LangButton from "./LangButton.svelte";
  import { currentLang, type textLang } from "./stores";

  function langClicked(lang: textLang) {
    $currentLang = lang;
  }
</script>

<div class="lang-buttons">
  {#each ["en", "cn", "jp", "kr"] as lang}
    <LangButton
      label={lang.toUpperCase()}
      selected={$currentLang == lang}
      onclick={() => langClicked(lang as textLang)}
    />
  {/each}
</div>

<style>
  .lang-buttons {
    display: flex;
    flex-direction: row;
    column-gap: 14px;
    justify-content: center;
    align-items: center;

    position: sticky;
    z-index: 90;
    top: 0;

    background-color: var(--color-background);
    padding: 12px;
    border-radius: 8px;
  }
</style>
