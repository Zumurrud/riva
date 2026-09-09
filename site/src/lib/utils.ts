export async function loadJson<T>(dataurl: string): Promise<T> {
  const response = await fetch(dataurl);

  return response.json();
}

export interface LoadArgs {
  url: {
    origin: string;
  };
}

export function getAvatarUrl(file: string, base: string): string {
  return `${base}/images/avatars/${file}.webp`;
}
