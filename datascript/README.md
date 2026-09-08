# Usage
Type `just do-the-thing` and everything just runs smile, updating the parallel site/ directory.  You'll still need to rerun that build (see `site/README.md`).

# Requirements
Currently expects several command-line tools in your path.  On Windows, these can be installed by installing [Scoop](https://www.scoop.sh) and then running
```
scoop install libwebp just uv
```
Other sources for `cwebp`, `just`, etc. should work fine; this is just how they're installed on my machine currently.

You may also need
```
scoop install uutils-coreutils
```
to provide basic *nix utilities like `cp` and `mkdir`.  It probably depends on your shell.
