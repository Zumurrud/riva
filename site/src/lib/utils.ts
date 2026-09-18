import { asset } from "$app/paths";

export async function loadJson<T>(dataurl: string): Promise<T> {
  const response = await fetch(dataurl);

  return response.json();
}

export interface LoadArgs {
  url: {
    origin: string;
  };
}

export function getAvatarUrl(file: string): string {
  return asset(`/images/avatars/${file}.webp`);
}
