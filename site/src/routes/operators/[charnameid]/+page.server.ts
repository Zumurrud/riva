import { loadJson, type LoadArgs } from "$lib/utils";
import type { textLang } from "$lib/stores";

interface CharLoadArgs extends LoadArgs {
  params: {
    charnameid: string
  }
}

export interface Chardata {
  charid: string,
  nameid: string,
  names: {
    [K in textLang]: string;
  },
  voices: [
    {
      id: string,
      title: {
        [K in textLang]: string;
      },
      text: {
        [K in textLang]: string;
      },
      asset: string,
    }
  ],
  actors: {
    [key: string]: {
      native: string,
      global: string,
    }
  }
  // TODO: this is just the keys of the actors object
  availability: [string],
  audio_path_override: {
    [key: string]: string,
  }
}

export async function load({ url, params }: CharLoadArgs): Promise<Chardata> {
  const nameid = params.charnameid; 
  const dataurl = `${url.origin}/data/chardata/${nameid}.json`;
  const chardata = await loadJson<Chardata>(dataurl);

  return chardata;
}