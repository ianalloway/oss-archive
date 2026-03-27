import {
  GRID_COLUMNS,
  GRID_ROWS,
  TICK_MS,
  advanceGame,
  createGame,
  restartGame,
  setDirection,
  togglePause,
} from "./game.mjs";

const boardElement = document.querySelector("#board");
const scoreElement = document.querySelector("#score");
const statusElement = document.querySelector("#status");
const pauseButton = document.querySelector("#pause-button");
const restartButton = document.querySelector("#restart-button");
const controlButtons = document.querySelectorAll("[data-direction]");

const cells = [];
let state = createGame();
let timerId = null;

function buildBoard() {
  boardElement.style.setProperty("--columns", String(GRID_COLUMNS));
  boardElement.style.setProperty("--rows", String(GRID_ROWS));

  const fragment = document.createDocumentFragment();

  for (let y = 0; y < GRID_ROWS; y += 1) {
    for (let x = 0; x < GRID_COLUMNS; x += 1) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.x = String(x);
      cell.dataset.y = String(y);
      fragment.append(cell);
      cells.push(cell);
    }
  }

  boardElement.replaceChildren(fragment);
}

function getCellIndex(x, y) {
  return y * GRID_COLUMNS + x;
}

function updateStatusText() {
  if (state.status === "paused") {
    statusElement.textContent = "Paused";
    pauseButton.textContent = "Resume";
    return;
  }

  if (state.status === "game_over") {
    statusElement.textContent = state.won ? "You win" : "Game over";
    pauseButton.textContent = "Pause";
    return;
  }

  statusElement.textContent = "Running";
  pauseButton.textContent = "Pause";
}

function render() {
  for (const cell of cells) {
    cell.className = "cell";
  }

  for (let index = state.snake.length - 1; index >= 0; index -= 1) {
    const segment = state.snake[index];
    const cell = cells[getCellIndex(segment.x, segment.y)];
    if (cell) {
      cell.classList.add(index === 0 ? "snake-head" : "snake-body");
    }
  }

  if (state.food) {
    const foodCell = cells[getCellIndex(state.food.x, state.food.y)];
    foodCell?.classList.add("food");
  }

  scoreElement.textContent = String(state.score);
  updateStatusText();
}

function stopLoop() {
  if (timerId !== null) {
    window.clearInterval(timerId);
    timerId = null;
  }
}

function startLoop() {
  stopLoop();

  timerId = window.setInterval(() => {
    state = advanceGame(state);
    render();

    if (state.status === "game_over") {
      stopLoop();
    }
  }, TICK_MS);
}

function syncLoopToState() {
  if (state.status === "running") {
    startLoop();
  } else {
    stopLoop();
  }
}

function handleDirection(direction) {
  if (state.status === "game_over") {
    return;
  }

  state = setDirection(state, direction);
  render();
}

function handleKeyboard(event) {
  const directionMap = {
    ArrowUp: "up",
    ArrowDown: "down",
    ArrowLeft: "left",
    ArrowRight: "right",
    w: "up",
    a: "left",
    s: "down",
    d: "right",
    W: "up",
    A: "left",
    S: "down",
    D: "right",
  };

  if (event.code === "Space") {
    event.preventDefault();
    state = togglePause(state);
    render();
    syncLoopToState();
    return;
  }

  const nextDirection = directionMap[event.key];
  if (!nextDirection) {
    return;
  }

  event.preventDefault();
  handleDirection(nextDirection);
}

pauseButton.addEventListener("click", () => {
  state = togglePause(state);
  render();
  syncLoopToState();
});

restartButton.addEventListener("click", () => {
  state = restartGame(state);
  render();
  syncLoopToState();
});

for (const button of controlButtons) {
  button.addEventListener("click", () => {
    handleDirection(button.dataset.direction);
  });
}

window.addEventListener("keydown", handleKeyboard);

buildBoard();
render();
startLoop();
