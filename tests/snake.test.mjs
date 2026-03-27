import test from "node:test";
import assert from "node:assert/strict";

import { advanceGame, createGame, placeFood, setDirection } from "../src/snake/game.mjs";

test("moves one cell in the current direction", () => {
  const state = createGame({
    columns: 8,
    rows: 8,
    random: () => 0,
  });

  const nextState = advanceGame(state, { random: () => 0 });

  assert.deepEqual(nextState.snake[0], {
    x: state.snake[0].x + 1,
    y: state.snake[0].y,
  });
  assert.equal(nextState.snake.length, state.snake.length);
});

test("ignores a direct reversal of direction", () => {
  const state = createGame({
    columns: 8,
    rows: 8,
    random: () => 0,
  });

  const reversed = setDirection(state, "left");

  assert.equal(reversed.direction, "right");
});

test("grows and increments score after eating food", () => {
  const state = {
    columns: 6,
    rows: 6,
    snake: [
      { x: 2, y: 2 },
      { x: 1, y: 2 },
      { x: 0, y: 2 },
    ],
    direction: "right",
    food: { x: 3, y: 2 },
    score: 0,
    status: "running",
    won: false,
  };

  const nextState = advanceGame(state, { random: () => 0 });

  assert.equal(nextState.score, 1);
  assert.equal(nextState.snake.length, 4);
  assert.notDeepEqual(nextState.food, { x: 3, y: 2 });
  assert.ok(nextState.food);
  assert.ok(!nextState.snake.some((segment) => segment.x === nextState.food.x && segment.y === nextState.food.y));
});

test("ends the game when the snake hits a wall", () => {
  const state = {
    columns: 4,
    rows: 4,
    snake: [
      { x: 3, y: 1 },
      { x: 2, y: 1 },
      { x: 1, y: 1 },
    ],
    direction: "right",
    food: { x: 0, y: 0 },
    score: 0,
    status: "running",
    won: false,
  };

  const nextState = advanceGame(state);

  assert.equal(nextState.status, "game_over");
  assert.equal(nextState.won, false);
});

test("ends the game when the snake hits itself", () => {
  const state = {
    columns: 5,
    rows: 5,
    snake: [
      { x: 2, y: 2 },
      { x: 2, y: 3 },
      { x: 1, y: 3 },
      { x: 1, y: 2 },
      { x: 1, y: 1 },
      { x: 2, y: 1 },
      { x: 3, y: 1 },
      { x: 3, y: 2 },
      { x: 3, y: 3 },
    ],
    direction: "right",
    food: { x: 0, y: 0 },
    score: 0,
    status: "running",
    won: false,
  };

  const nextState = advanceGame(state);

  assert.equal(nextState.status, "game_over");
});

test("places food in an open cell only", () => {
  const food = placeFood(
    [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 0, y: 1 },
    ],
    2,
    2,
    () => 0,
  );

  assert.deepEqual(food, { x: 1, y: 1 });
});
