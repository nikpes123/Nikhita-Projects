import { subtractCoordinatesOfGrid, Colour, BlockType, LevelOfDifficulty,
     FourBlocks, OneBlock, Action,State, Axis, Constants, initialState, rotationOffsets } from "./constantsAndTypes";

/**
 * Generates a random color for a game block.
 *
 * @returns A random color from the available color options.
 */
export function getRandomColor(): Colour {
    const blockColor: Colour[] = ["red", "blue", "green", "yellow", "purple", "orange"];
    const randomIndex = Math.floor(Math.random() * blockColor.length);
    return blockColor[randomIndex];
  };
/**
 * Generates a random block type for a game block.
 *
 * @returns A random block type from the available block type options.
 */
export function getRandomBlockType(): BlockType {
    const fourBlockType : BlockType[] = ["O", "I", "T", "J", "L", "S", "Z"];
    const randomIndex = Math.floor(Math.random() * fourBlockType.length);
    return fourBlockType[randomIndex];
};
/**
 * Creates a new whole block with random properties.
 *
 * @param blockCount - The current block count used for generating unique IDs.
 * @returns A FourBlocks object representing the new tetromino.
 */
  export const createTetromino = (blockCount: number): FourBlocks => {
    // Generate a random color for the four block
    const blockColour: Colour = getRandomColor();
    // Generate a random block type for the four blocks
    const blockType: BlockType = getRandomBlockType();
    let block: FourBlocks;  // The fourBlock object to be created
    
    // Create the block based on its block type and filling it with colour
    if (blockType === "O"){
      block =  {
        type: blockType,
        blocks: [
          {id: blockCount    , x: 4, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 1, x: 5, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 2, x: 4, y: 19, colour: blockColour} as OneBlock, 
          {id: blockCount + 3, x: 5, y: 19, colour: blockColour} as OneBlock],
        rotationState: 1,
        pivot: {id: blockCount, x: 4, y: 18, colour: blockColour} as OneBlock
      } as FourBlocks;
    } else if (blockType === "I"){
      block = {
      type: blockType,
      blocks: [
        {id: blockCount    , x: 4, y: 19, colour: blockColour} as OneBlock, 
        {id: blockCount + 1, x: 3, y: 19, colour: blockColour} as OneBlock, 
        {id: blockCount + 2, x: 5, y: 19, colour: blockColour} as OneBlock, 
        {id: blockCount + 3, x: 6, y: 19, colour: blockColour} as OneBlock],
      rotationState: 1,
      pivot: {id: blockCount, x: 4, y: 19, colour: blockColour} as OneBlock
    } as FourBlocks;
  } else if (blockType === "J"){
      block =  {
        type: blockType,
        blocks: [
          {id: blockCount    , x: 5, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 1, x: 4, y: 19, colour: blockColour} as OneBlock, 
          {id: blockCount + 2, x: 4, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 3, x: 6, y: 18, colour: blockColour} as OneBlock],
      rotationState: 1,
      pivot: {id: blockCount, x: 5, y: 18, colour: blockColour} as OneBlock
    } as FourBlocks;
  } else if (blockType === "L"){
    block =   {
    type: blockType,
    blocks: [
      {id: blockCount    , x: 5, y: 18, colour: blockColour} as OneBlock, 
      {id: blockCount + 1, x: 4, y: 18, colour: blockColour} as OneBlock, 
      {id: blockCount + 2, x: 6, y: 18, colour: blockColour} as OneBlock, 
      {id: blockCount + 3, x: 6, y: 19, colour: blockColour} as OneBlock],
    rotationState: 1,
    pivot: {id:  blockCount, x: 5, y: 18, colour: blockColour} as OneBlock
    } as FourBlocks;
  } else if (blockType === "S"){
      block = {
        type: blockType,
        blocks: [
          {id: blockCount    , x: 5, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 1, x: 4, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 2, x: 5, y: 19, colour: blockColour} as OneBlock, 
          {id: blockCount + 3, x: 6, y: 19, colour: blockColour} as OneBlock],
        rotationState: 1,
        pivot: {id: blockCount, x: 5, y: 18, colour: blockColour} as OneBlock
      } as FourBlocks;
  } else if (blockType === "Z"){
      block = {
        type: blockType,
        blocks: [
          {id: blockCount    , x: 5, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 1, x: 4, y: 19, colour: blockColour} as OneBlock, 
          {id: blockCount + 2, x: 5, y: 19, colour: blockColour} as OneBlock, 
          {id: blockCount + 3, x: 6, y: 18, colour: blockColour} as OneBlock],
        rotationState: 1,
        pivot: {id: blockCount, x: 5, y: 18, colour: blockColour} as OneBlock
      } as FourBlocks;
  } else {
      block = {
        type: blockType,
        blocks: [
          {id: blockCount    , x: 5, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 1, x: 4, y: 18, colour: blockColour} as OneBlock, 
          {id: blockCount + 2, x: 5, y: 19, colour: blockColour} as OneBlock, 
          {id: blockCount + 3, x: 6, y: 18, colour: blockColour} as OneBlock],
        rotationState: 1,
        pivot: {id: blockCount, x: 5, y: 18, colour: blockColour} as OneBlock
      } as FourBlocks;
    }
    return block;
};

/**
 * Checks if a block (tetromino) collides with the bottom or top boundary of the game grid.
 *
 * @param block - The block (tetromino) to check for collision.
 * @param axis - The axis to check collision on ("x", "y", or "xy").
 * @param amount - The amount to adjust the position before collision checking.
 * @returns True if collision with the bottom/top boundary occurs, otherwise false.
 */
const checkBottomCollusion = (block: FourBlocks, axis: Axis, amount: number = 0) => {
    if (axis === "y" || axis === "xy") {
      return block.blocks.some((b) =>
        b.y + amount < 0 || b.y + amount > Constants.GRID_HEIGHT - 1);
    }
    return false;
  };
/**
 * Checks if a block (tetromino) collides with the left or right boundary of the game grid.
 *
 * @param block - The block (tetromino) to check for collision.
 * @param axis - The axis to check collision on ("x", "y", or "xy").
 * @param amount - The amount to adjust the position before collision checking.
 * @returns True if collision with the left/right boundary occurs, otherwise false.
 */  
const checkSidesCollusion = (block: FourBlocks, axis: Axis, amount: number = 0) => {
    if (axis === "x" || axis === "xy") {
      return block.blocks.some((b) =>
        b.x + amount < 0 || b.x + amount > Constants.GRID_WIDTH - 1);
    }
    return false;
  };
/**
 * Checks if a block (tetromino) collides with static blocks in the game grid.
 *
 * @param block - The block (tetromino) to check for collision.
 * @param staticBlocks - The array of static blocks in the game grid.
 * @param axis - The axis to check collision on ("x" or "y").
 * @param amount - The amount to adjust the position before collision checking.
 * @returns True if collision with static blocks occurs, otherwise false.
 */
const checkCollusionWithStaticBLocks = (block: FourBlocks, staticBlocks: ReadonlyArray<OneBlock>, axis: Axis, amount: number = 0) => {
    if (axis === "y") {
      return block.blocks.some((eachBlock) =>
        staticBlocks.some((eachSBlock) =>
          eachBlock.x === eachSBlock.x && eachBlock.y + amount === eachSBlock.y
        )
      );
    } else {
      return block.blocks.some((eachBlock) =>
        staticBlocks.some((eachSBlock) =>
          eachBlock.x + amount === eachSBlock.x && eachBlock.y === eachSBlock.y));
    }
  };
/**
 * Checks for collisions of a block (tetromino) in the game grid.
 *
 * @param block - The block (tetromino) to check for collisions.
 * @param staticBlocks - The array of static blocks in the game grid.
 * @param axis - The axis to check collisions on ("x" or "y").
 * @param amount - The amount to adjust the position before collision checking.
 * @returns True if any collisions occur, otherwise false.
 */
export const checkCollusion = (block: FourBlocks, staticBlocks: ReadonlyArray<OneBlock>, axis: Axis, amount: number = 0) => {
      return checkBottomCollusion(block , axis, amount) ||
      checkSidesCollusion(block , axis, amount) ||
      checkCollusionWithStaticBLocks(block, staticBlocks, axis, amount);
    }

/**
 * Moves a block (tetromino) in the game grid by a specified amount along a specified axis.
 *
 * @param fourBlocks - The block (tetromino) to move.
 * @param axis - The axis along which to move the block ("x" or "y").
 * @param amount - The amount by which to move the block.
 * @returns A new block (tetromino) with updated positions after the move.
 */
const moveBlock = (fourBlocks: FourBlocks, axis: Axis, amount: number): FourBlocks => {
        // Map through tetromino blocks and increase / decrease x or y value by amount, same for pivot
        const updateBlocks = fourBlocks.blocks.map(eachBlock => {
          const [newX, newY] = updateBlockMovement(axis, eachBlock, amount);
          return {
            ...eachBlock,
            x: newX,
            y: newY
          } as OneBlock;
        });
      
        const [newX, newY] = updateBlockMovement(axis, fourBlocks.pivot, amount);
        const updateCentre = {...fourBlocks.pivot, 
          x: newX,
          y: newY
        } as OneBlock
      
        return {...fourBlocks,
          blocks: updateBlocks,
          pivot: updateCentre 
        } as FourBlocks
      }
/**
 * Updates the position of a block (tetromino) along a specified axis by a specified amount.
 *
 * @param axis - The axis along which to update the position ("x" or "y").
 * @param block - The block (tetromino) to update.
 * @param amount - The amount by which to update the position.
 * @returns An array containing the new X and Y coordinates of the block.
 */      
const updateBlockMovement = (axis: Axis, block: OneBlock, amount:number ) => {
        const newX = axis === "x" ? Math.min(Math.max(block.x + amount, 0), Constants.GRID_WIDTH - 1) : block.x;
        const newY = axis === "y" ? Math.max(block.y + amount, 0) : block.y;
        return [newX, newY];
      }


/**
 * Represents an action to move a block (tetromino) in the game grid.
 */
export class MoveBlock implements Action {
    constructor(
      public readonly deltaX: number,
      public readonly deltaY: number,
      public readonly speedFactor: number = 1
    ) {}
    apply(s: State): State {
      // Check if a block will collide
      const isMoveX = !checkCollusion(s.fourBlocks, s.staticBlocks, "x", this.deltaX);
      const isMoveY = !checkCollusion(s.fourBlocks, s.staticBlocks, "y", this.deltaY * this.speedFactor);
  
      const updatedFourBlocks = moveBlock(s.fourBlocks, "x", this.deltaX);
      const updatedState = {
        ...s,
        fourBlocks: isMoveX ? updatedFourBlocks : s.fourBlocks,
      };
      return isMoveY ? updatedState : moveDownwards(updatedState);
    }
  }
/**
 * Represents an action to restart the game.
 *
 * This action is instantiated when the "T" key is pressed.
 */
export class Restart implements Action {constructor() {}
apply(s: State): State {
  // If the game over, reset to the initial state while keeping the high score
    // return the current state unchanged 
  if (s.gameEnd) {
    return {
      ...initialState,
      highscore: s.highscore,
    };
  } else {
    return s;
  }
}
}
/**
 * Handles moving a block (tetromino) downwards in the game grid.
 *
 * Checks for valid moves, collision, and game end conditions.
 *
 * @param s - The current game state.
 * @returns The updated game state after moving the block down.
 */
export const moveDownwards = (s: State): State => {
    const isMove = !(checkCollusion(s.fourBlocks, s.staticBlocks, "y", -1))
    const IsGameEnd = s.fourBlocks.blocks.some((eachBlock) =>
    s.staticBlocks.some((eachSBlock) => eachBlock.x === eachSBlock.x && eachBlock.y === eachSBlock.y)
  );
    let state: State;
    if (IsGameEnd){
      state = {...s,
        gameEnd: IsGameEnd,
        highscore: s.score > s.highscore ? s.score : s.highscore 
      } as State
    } else {
      state = {...s,
        fourBlocks: isMove ? moveBlock(s.fourBlocks, "y", -1) : s.previewBlocks,
        previewBlocks: isMove ? s.previewBlocks : createTetromino(s.blockCount + 4),
        staticBlocks: isMove ? s.staticBlocks : s.staticBlocks.concat(s.fourBlocks.blocks), 
        blockCount: isMove ? s.blockCount : s.blockCount + 4,
      } as State
    }  
    return clearBlocks(state);
  }

/**
 * Clears filled rows and updates the game state.
 *
 * @param s - The current game state.
 * @returns The updated game state after clearing rows and updating the score.
 */ 
const clearBlocks = (s: State): State => { 
    const filledRows = [...new Set(s.staticBlocks.map(block => block.y))];
    const findRowsToErase = filledRows.filter(row =>
      s.staticBlocks.reduce((count, block) => count + Number(block.y === row), 0) === Constants.GRID_WIDTH
    );
    const blocksToBeErased = s.staticBlocks.filter(eachBlock => findRowsToErase.includes(eachBlock.y));
    const newScore = s.score + findRowsToErase.length * 50;
    
    const updatedState = {
      ...s,
      staticBlocks: s.staticBlocks.filter(block => !blocksToBeErased.includes(block)),
      exitBlocks: s.exitBlocks.concat(blocksToBeErased),
      level: findDifficultyLevel(newScore),
      score: newScore,
    };
    return findRowsToErase.length > 0 ? updateRows(updatedState, findRowsToErase) : updatedState;
  }
/**
 * Determines the difficulty level based on the player's score.
 *
 * @param score - The player's score.
 * @returns The difficulty level.
 */
const findDifficultyLevel = (score: number): LevelOfDifficulty => {
    if (score < 100){
      return 1;
    } else if (score >= 100 && score < 500){
      return 2;
    } else if (score >= 500 && score < 1000){
      return 3;
    } else if (score >= 1000 && score < 1500){
      return 4;
    } else {
      return 5;
    }
  }

/**
 * Updates the game state by shifting blocks downwards.
 *
 * @param s - The current game state.
 * @param clearedRows - An array of row numbers that have been cleared.
 * @returns The updated game state after shifting the blocks downwards.
 */
const updateRows = (s: State, clearedRows: ReadonlyArray<number>): State => {
    const blocksToUpdate = s.staticBlocks.filter(block => block.y > Math.min(...clearedRows));
    const updatedBlocksRows = blocksToUpdate.map(block => ({
      ...block,
      y: block.y - clearedRows.filter(rowNum => rowNum < block.y).length
    }) as OneBlock);
    return {...s,
      staticBlocks: s.staticBlocks.filter(eachBlock => !blocksToUpdate.includes(eachBlock)).concat(updatedBlocksRows)
    } as State
  } 
/**
 * Represents an action to advance the game by one tick.
 */
export class Tick implements Action {
    constructor(public readonly ticks: number) {}
    apply(s: State): State {
      return this.ticks % (Constants.LEVEL_0_TICK - (s.level * 4)) === 0 ? moveDownwards(s) : s;
    }
  }
/**
 * Represents an action to rotate the current block (tetromino) in the game grid.
 */
export class Rotate implements Action {constructor() {}
  apply(s: State): State {
    if (s.fourBlocks.type === "O") {
        // If it's an "O" block, return the original state without rotation
        return s;
      }
    const positions = rotateBlocks(s.fourBlocks, s.fourBlocks.pivot)
    .filter(eachSet => !checkCollusion(eachSet, s.staticBlocks, "xy"));
    
    let rotatedBlock: FourBlocks; 
    if (positions.length > 0){
      rotatedBlock = {...s.fourBlocks, 
        blocks:  positions[0].blocks ,
        rotationState: (s.fourBlocks.rotationState + 1) % 4 ,
        pivot:  positions[0].blocks[0] 
      } as FourBlocks   
    } else{
      rotatedBlock = {...s.fourBlocks, 
        blocks:  s.fourBlocks.blocks,
        rotationState:  s.fourBlocks.rotationState,
        pivot:  s.fourBlocks.pivot
      } as FourBlocks 
    }
    return {...s,
      fourBlocks: rotatedBlock
    } as State
  }
}
/**
 * Rotates the blocks of a tetromino around its pivot point and returns the possible positions.
 *
 * @param tetromino - The tetromino to rotate.
 * @param pivot - The pivot point of the tetromino.
 * @returns An array of possible tetromino positions after rotation.
 */
const rotateBlocks = (tetromino: FourBlocks, pivot: OneBlock): ReadonlyArray<FourBlocks> => {
    const rotatedBlocks = tetromino.blocks.map(eachBlock => {
      const xPivot = eachBlock.x - pivot.x
      const yPivot = eachBlock.y - pivot.y
      const xPos = (xPivot * 0 + yPivot * 1) + pivot.x
      const yPos = (xPivot * -1 + yPivot * 0) + pivot.y
      return {...eachBlock,
        x: xPos,
        y: yPos,
      } as OneBlock
    })
    const offset: ReadonlyArray<ReadonlyArray<[number, number]>> = rotationOffsets(tetromino.type);
    const positions =  offset.map(eachOffset => {
      const updatedBlocks =  rotatedBlocks.map(eachBlock => ({...eachBlock,
        x: eachBlock.x + (subtractCoordinatesOfGrid(
          eachOffset[tetromino.rotationState], eachOffset[(tetromino.rotationState + 1) % 4])[0]),
        y: eachBlock.y + (subtractCoordinatesOfGrid(
          eachOffset[tetromino.rotationState], eachOffset[(tetromino.rotationState + 1) % 4])[1])} as OneBlock))
      return {...tetromino, 
        blocks: updatedBlocks
      } as FourBlocks
    })
    return positions;
  }