import adapter from "@sveltejs/adapter-static";

const dev = process.argv.includes("dev");

const config = {
  kit: {
    adapter: adapter({
      pages: "build",
      assets: "build",
    }),
    paths: {
      base: dev ? "" : "/asbestos-is-bestos",
    },
    prerender: {
      origin: dev ? "http://sveltekit-prerender" : "http://localhost:5173",
    },
  },
};

export default config;
