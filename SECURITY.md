# Security

Please report security problems privately via GitHub: **Security → Report a vulnerability** on this repository, not as a public issue. You get an answer within 7 days.

What the skill does with your data:
- It runs inside your AI assistant. The skill itself sends nothing anywhere.
- Researcher roles may search the web through your assistant's search tool. Web content is treated as data to evaluate, never as instructions.
- HTML protocols are saved as local files and can contain what you submitted (CV, contract, business numbers). Check before you share them.
- `scripts/make_demo_gifs.py` and `scripts/make_flow_gifs.py` start Chrome with `--no-sandbox` to screenshot local demo pages. Use them only on your own local files.
