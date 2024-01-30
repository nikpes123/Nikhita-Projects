import { createTetromino } from "./blockState";

/** Constants */
export const Viewport = {
    CANVAS_WIDTH: 200,
    CANVAS_HEIGHT: 400,
    PREVIEW_WIDTH: 160,
    PREVIEW_HEIGHT: 80,
  } as const;
    
export const Constants = {
    TICK_RATE_MS: 40, 
    LEVEL_0_TICK: 30, // Ticks before moving a tetromino down
    GRID_WIDTH: 10,
    GRID_HEIGHT: 20,
  } as const;
  
export const Block = {
    WIDTH: Viewport.CANVAS_WIDTH / Constants.GRID_WIDTH,
    HEIGHT: Viewport.CANVAS_HEIGHT / Constants.GRID_HEIGHT,
  };
/**
 * Stores the offsets based on block type ("O"| "I"| "T"| "J"| "L"| "S"| "Z")
 */
export const rotationOffsets = (type: BlockType) : ReadonlyArray<ReadonlyArray<[number, number]>>=> {
    switch (type) {
      case "O": {
        return [[[0, 0]], [[0, -1]], [[-1, -1]], [[-1, 0]]];
      }
      case "I": {
        return [
          [[0, 0], [-1, 0], [-1, 1], [0, 1]],
          [[-1, 0], [0, 0], [1, -1], [0, 1]],
          [[2, 0], [0, 0], [-2, 1], [0, 1]],
          [[-1, 0], [0, 1], [1, 0], [0, -1]],
          [[2, 0], [0, -2], [-2, 0], [0, 2]],
        ];
      }
      default: {
        return [
          [[0, 0], [0, 0], [0, 0], [0, 0]],
          [[0, 0], [1, 0], [0, 0], [-1, 0]],
          [[0, 0], [1, -1], [0, 0], [-1, -1]],
          [[0, 0], [0, 2], [0, 0], [0, 2]],
          [[0, 0], [1, 2], [0, 0], [-1, 2]],
        ];
      }
    }
  }; 
/**
 * Initial State
 */
export const initialState: State = {
    gameEnd: false,
    fourBlocks: createTetromino(0),
    previewBlocks: createTetromino(4),
    staticBlocks: [],
    exitBlocks: [],
    blockCount: 4,
    level: 1,
    score: 0,
    highscore: 0,
  } as const;

/** Types */
export type Key = "KeyW" | "KeyA" | "KeyD" | "KeyR" | "KeyT"; // Key interactions
export type Event = "keydown" | "keyup" | "keypress";
export type Colour = "red"| "blue"| "green"| "yellow"| "purple"| "orange";
export type BlockType = "O"| "I"| "T"| "J"| "L"| "S"| "Z"; //7 block types
export type RotationType = 1 | 2 | 3 | 4; // 90 degree, 180 degree, 270 degree and 360 degree
export type LevelOfDifficulty = 1 | 2 | 3 | 4 | 5; // 5 levels in the game
export type Axis = "x" | "y" | "xy"; // xy represents both axis, used for rotation)

/**
 * one single cube
 */
export type OneBlock = Readonly<{
  x: number,
  y: number,
  colour: Colour,
  id: number
}>;
/**
 * 4 cubes together to form a block on the game
 */
export type FourBlocks = Readonly<{
  type: BlockType,
  blocks: ReadonlyArray<OneBlock>,
  rotationState: RotationType,
  pivot: OneBlock,
}>
/**
 *  State of the game
 */
export type State = Readonly<{
  gameEnd: boolean,
  fourBlocks: FourBlocks,
  previewBlocks: FourBlocks,
  staticBlocks: ReadonlyArray<OneBlock>,
  exitBlocks: ReadonlyArray<OneBlock>,
  blockCount: number,
  level: LevelOfDifficulty,
  score: number,
  highscore: number,
}>;


/**
 * an interface to represent each action on the gris
 */
export interface Action {
    apply(s: State): State;
  }

/**
 * this is a helper function used to find possible cordinates during rotation
 */
export function subtractCoordinatesOfGrid(cord1: [number, number], cord2: [number, number]): [number, number] {
    return [cord1[0] - cord2[0], cord1[1] - cord2[1]];
  }


