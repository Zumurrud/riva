import type { textLang } from "$lib/stores";
import type { PageServerLoad } from "./$types";
import { asset } from "$app/paths";

export interface Chardata {
  charid: string;
  nameid: string;
  names: {
    [K in textLang]: string;
  };
  voices: [
    {
      id: string;
      title: {
        [K in textLang]: string;
      };
      text: {
        [K in textLang]: string;
      };
      asset: string;
    },
  ];
  actors: {
    [key: string]: {
      native: string;
      global: string;
    };
  };
  availability: [string];
  audio_path_override: {
    [key: string]: string;
  };
}

export const load: PageServerLoad = async ({ fetch, url, params }) => {
  const res = await fetch(asset(`/data/chardata/${params.charnameid}.json`));
  const item = await res.json();

  return item as Chardata;
};
