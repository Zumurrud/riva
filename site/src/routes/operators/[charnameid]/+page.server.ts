import type { textLang } from "$lib/stores";

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
  // TODO: this is just the keys of the actors object
  availability: [string];
  audio_path_override: {
    [key: string]: string;
  };
}

export const load = async ({ fetch, url, params }) => {
  const res = await fetch(
    `${url.origin}/data/chardata/${params.charnameid}.json`,
  );
  const item = await res.json();

  return item;
};
