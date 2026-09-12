# Generic scripts

Every helper here is project-, domain- and language-neutral. Anything that names a language, build
tool, test framework or case belongs in the repository's own `dev/scripts/`.

- `xcalibre-dev` - validate, resume, or migrate a repository context vault; run:
  `<this-dir>/xcalibre-dev <resume|check|migrate> [--full|--apply] [repository]`.
- `comment_blocks.py` - inspect or replace source comment blocks by line range; run:
  `python3 <this-dir>/comment_blocks.py <file> [prefix]`. Also how the THREE-LINE comment rule is
  audited: any block whose range spans more than three lines is over the limit.
