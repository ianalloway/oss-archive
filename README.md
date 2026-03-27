# Snake

A minimal classic Snake game built with plain HTML, CSS, and JavaScript.

The project focuses on the original gameplay loop only:

- grid-based movement
- food spawning
- snake growth
- score tracking
- game over on wall or self collision
- restart support

## Stack

- HTML
- CSS
- JavaScript ES modules
- Node.js built-in test runner

## Run locally

```bash
npm start
```

Then open `http://localhost:3000`.

## Run tests

```bash
npm test
```

## Project structure

- `index.html` — app shell
- `src/snake/game.mjs` — deterministic core game logic
- `src/snake/app.mjs` — browser rendering and controls
- `src/snake/styles.css` — minimal presentation
- `scripts/serve.mjs` — zero-dependency local static server
- `tests/snake.test.mjs` — core logic tests

## Controls

- Arrow keys or `WASD` to move
- `Space` to pause or resume
- `Restart` button to reset the run
- On smaller screens, on-screen directional buttons are available

## Deploy options

### GitHub Pages / static hosting

This project is static and can be deployed anywhere that serves plain files.

### Hugging Face Spaces

Create a **Static** Space and upload:

- `index.html`
- `src/`
- `package.json`
- `README.md`

### Website embed

If you host it separately, it can be embedded with a standard `iframe`.
