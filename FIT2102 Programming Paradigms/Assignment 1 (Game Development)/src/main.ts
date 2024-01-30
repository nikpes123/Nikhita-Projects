/**
 * Inside this file you will use the classes and functions from rx.js
 * to add visuals to the svg element in index.html, animate them, and make them interactive.
 *
 * Study and complete the tasks in observable exercises first to get ideas.
 *
 * Course Notes showing Asteroids in FRP: https://tgdwyer.github.io/asteroids/
 *
 * You will be marked on your functional programming style
 * as well as the functionality that you implement.
 *
 * Document your code!
 */

import "./style.css";

import { fromEvent, interval, merge } from "rxjs";
import { map, filter, scan, mergeWith } from "rxjs/operators";
import { State, Key, Constants,  Action, initialState  } from "./constantsAndTypes";
import { MoveBlock, Restart, Tick, Rotate } from "./blockState"; 
import { render } from "./display";


/**
 * Updates the state by proceeding with one time step.
 *
 * @param s Current state
 * @returns Updated state
 */
const tick = (s: State, action: Action): State =>
     action.apply(s);

/**
 * The main function that sets up the game and handles user input.
 */
export function main() {
  // Observing keyboard events (keypress)
  const key$ = fromEvent<KeyboardEvent>(document, "keypress");
  /**
   * Create an observable for a specific key press event.
   *
   * @param keyCode - The key code to listen for.
   * @param result - A function that returns the corresponding action when the key is pressed.
   */
  const fromKey = <T>(keyCode: Key, result: () => T) =>
    key$.pipe(
      filter(({ code }) => code === keyCode),
      map(result)
    )

  // Observables for specific key presses
  const left$ = fromKey("KeyA", () => new MoveBlock(-1, 0));
  const right$ = fromKey("KeyD", () => new MoveBlock(1, 0));
  const down$ = fromKey("KeyW", () => new MoveBlock(0,-1, 100));
  const rotate$ = fromKey("KeyR", () => new Rotate());
  const restart$ = fromKey("KeyT", () => new Restart());
  

  /**
   * The main game loop, combining key presses and ticks to control game state.
   */
  const tick$ = interval(Constants.TICK_RATE_MS)
  .pipe(
    map(elapsed => new Tick(elapsed)),
    mergeWith(left$, right$, down$, rotate$, restart$),
    scan(tick, initialState))
  .subscribe(render) // Subscribe to updates and render the game state
}

// The following simply runs your main function on window load.  Make sure to leave it in place.
if (typeof window !== "undefined") {
  window.onload = () => {
    main();
  };
}
