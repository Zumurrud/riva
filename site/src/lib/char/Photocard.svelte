<script lang="ts">
  interface Props {
    imgsrc: string;
    text: string;
  }

  let { imgsrc, text }: Props = $props();
</script>

<div class="photocard">
  <img loading="lazy" src={imgsrc} alt="Portrait of {text}" />
  <span>{text}</span>
</div>

<style>
  .photocard {
    --width: 76px;

    background-color: #e8e5dc;
    padding: 4px 5px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    color: var(--color-background);
    font-weight: 600;
    font-size: 0.75em;

    /* This width does not include padding!
       So it should be the same as image */
    width: var(--width);
    min-height: 98px;
  }

  span {
    text-align: center;
    line-height: 1em;
    margin-top: 7px;
    /* Sizing eyeballing bc font size autosizing in flexbox is whack */
  }

  img {
    background-color: #3a3a3a;
    width: var(--width);
    height: var(--width);
  }

  @media (min-width: 800px) {
    .photocard {
      --width: 120px;
      padding: 8px 10px;
      font-size: 1.1em;
    }
  }
</style>
