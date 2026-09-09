# RIVA Site

The site is built using SvelteKit and TypeScript. I'm using `bun`. `npm`, `yarn`, etc. should be similar or the same.

For development, run

```bash
bun run dev
```

To build, run

```bash
bun run build
```

This will build a static site in the `build` folder. For a preview, run

```bash
bun run preview
```

If you want to deploy somewhere that's not a bare sub/domain (e.g. `www.xyz.com/not-a-domain`) see `config.kit.paths.base` in `svelte.config.js`.
