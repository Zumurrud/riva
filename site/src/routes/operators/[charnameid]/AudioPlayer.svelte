<script lang="ts">
  import AudioIcon from "$lib/icons/AudioIcon.svelte";

  export let assetloc: string;
  export let availability: string[] = [];
  export let pathOverride: {[key: string]: string};

  // Some skins have # in the name, which has to be escaped in the URL
  $: assetlocClean = assetloc.replace("#", "%23").toLowerCase()

  const sourceurl = "https://raw.githubusercontent.com/Zumurrud/riva-voices/main"

  const voiceMap = new Map([
    ["jp", "voice"],
    ["cn", "voice_cn"],
    ["en", "voice_en"],
    ["kr", "voice_kr"],
  ]);

  const oldLangs = ["old_jp", "old_en", "old_cn"]

  const regionalSuffixes = new Map([
    ["cn_topolect", "cn_topolect"],
    ["de", ""],
    ["es", ""],
    ["fr", ""],
    ["it", "ita"],
    ["ru", ""],
  ]);

  const nameMapping = new Map([
    ["cn_topolect", "CN REG"],
    ["linkage", "OG"],
    ["old_cn", "OLD CN"],
    ["old_en", "OLD EN"],
    ["old_jp", "OLD JP"],
  ]);

  function getAudioFileUrl(lang: string | null) {
    if (lang === null) {
      return null;
    }

    if (pathOverride != null && Object.hasOwn(pathOverride, lang))
    {
      // :amiyaunconcerned:
      let line_num = assetlocClean.slice(-3);
      return pathOverride[lang].replace("###", line_num);
    }
    
    // One of the standard voice languages
    if (voiceMap.has(lang)) {
      return `${sourceurl}/${voiceMap.get(lang)}/${assetlocClean}.ogg`;
    }

    if (regionalSuffixes.has(lang)) {
      let suff = regionalSuffixes.get(lang);
      let assetReal = (suff === "")
        ? assetlocClean
        : assetlocClean.replace('/', `_${suff}/`);
      return `${sourceurl}/voice_custom/${assetReal}.ogg`
    }

    if (lang === "linkage") {
      if (assetlocClean.includes("ncdeer")) {
        return `${sourceurl}/${voiceMap.get("cn")}/${assetlocClean}.ogg`
      }

      return `${sourceurl}/${voiceMap.get("jp")}/${assetlocClean}.ogg`
    }
    
    return null;
  }

  let audiofile: string | null;
  $: audiofile = getAudioFileUrl(selectedLang);

  let selectedLang: string | null = null;
  let showAudio: boolean;
  $: showAudio = selectedLang != null && audiofile != null;

  function clickLang(lang: string) {
    if (lang === selectedLang) {
      selectedLang = null;
      return;
    }

    selectedLang = lang;
  }
</script>

<div class="audio-container">
  <div class="audio-selector">
    <AudioIcon />
    {#each availability as lang}
      <button
        on:click={() => clickLang(lang)}
        class:selected={selectedLang === lang}
        class:no-width={oldLangs.includes(lang)}
      >{
        nameMapping.has(lang)
          ? nameMapping.get(lang)
          : lang.toUpperCase()
      }</button>
    {/each}
  </div>

  {#if showAudio}
  <audio controls src={audiofile} preload="auto" autoplay>
    <a href={audiofile}> Download audio </a>
  </audio>
  {/if}

</div>

<style>
  .audio-container {
    background-color: var(--color-lighterbg);
    border-radius: 0 0 20px 20px;
    padding: 0 10px 10px 10px;
    display: inline-block;
    box-sizing: border-box;
    max-width: 100%;
  }

  .audio-selector {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    column-gap: 7px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 6px;

    background-color: var(--color-background);
    border-radius: 8px;

    overflow-x: auto;
  }

  .audio-selector :global(svg) {
    margin-right: 6px;
  }

  .audio-selector button {
    width: 39px;
    height: 34px;
    font-size: 16px;
    background-color: #464646;
    color: #fff;
    box-shadow: 0px -4px 0px 0px rgba(0, 0, 0, 0.35) inset;
    border: none;
    line-height: 0.8;
  }

  .audio-selector button:active, .audio-selector button.selected {
    box-shadow: none;
    padding-top: 4px;
  }

  .audio-selector button.selected {
    background-color: #7F2936
  }

  .audio-selector button.no-width {
    width: auto;
  }

  audio {
    max-width: 100%;
    margin-top: 8px;
  }
</style>