import { Viewport, Block, OneBlock, State } from "./constantsAndTypes";

/**
 * Displays a SVG element on the canvas. Brings to foreground.
 *
 * @param elem - SVG element to display
 */
const show = (elem: SVGGraphicsElement) => {
    elem.setAttribute("visibility", "visible");
    elem.parentNode!.appendChild(elem);
  };


/**
 * Hides a SVG element on the canvas.
 *
 * @param elem - SVG element to hide
 */
const hide = (elem: SVGGraphicsElement) => {
    elem.setAttribute("visibility", "hidden");
  };
/**
 * Creates an SVG element with the given properties.
 * See https://developer.mozilla.org/en-US/docs/Web/SVG/Element for valid
 * element names and properties.
 * @param namespace Namespace of the SVG element
 * @param name SVGElement name
 * @param props Properties to set on the SVG element
 * @returns SVG element
 */
const createSvgElement = (
    namespace: string | null,
    name: string,
    props: Record<string, string> = {}
  ) => {
    const elem = document.createElementNS(namespace, name) as SVGElement;
    Object.entries(props).forEach(([k, v]) => elem.setAttribute(k, v));
    return elem;
  };
/** Canvas Elements */
const svg = document.querySelector("#svgCanvas") as SVGGraphicsElement &
HTMLElement;
const preview = document.querySelector("#svgPreview") as SVGGraphicsElement &
HTMLElement;
const gameover = document.querySelector("#gameOver") as SVGGraphicsElement &
HTMLElement;

// Set canvas dimensions based on Viewport constants
svg.setAttribute("height", `${Viewport.CANVAS_HEIGHT}`);
svg.setAttribute("width", `${Viewport.CANVAS_WIDTH}`);
preview.setAttribute("height", `${Viewport.PREVIEW_HEIGHT}`);
preview.setAttribute("width", `${Viewport.PREVIEW_WIDTH}`);

const levelText = document.querySelector("#levelText") as HTMLElement;
const scoreText = document.querySelector("#scoreText") as HTMLElement;
const highScoreText = document.querySelector("#highScoreText") as HTMLElement;


  /**
   * Renders the current state to the canvas.
   *
   * In MVC terms, this updates the View using the Model.
   *
   * @param s Current state
   */
export const render = (s: State) => {
    // Combine new blocks with existing static blocks for display
    const displayCubes = [...s.fourBlocks.blocks, ...s.staticBlocks];
    // Clear preview area
    if (preview) {
        preview.innerHTML = '';
    }
 /**
     * Renders multiple blocks to a selected container (svg canvas / preview canvas).
     *
     * @param blocks - Array of SingleBlocks
     * @param container - SVG element to render to
     */
  const renderBlocks = (blocks: ReadonlyArray<OneBlock>, container: SVGGraphicsElement & HTMLElement) => {
    blocks.forEach(eachBlock => {
      const blockView = () => {
        const block = createSvgElement(svg.namespaceURI, "rect", {
          height: `${Block.HEIGHT}`,
          width: `${Block.WIDTH}`,
          x: "0",
          y: "0",
          style: `fill: ${eachBlock.colour}`,
          id: `${eachBlock.id}`
        });
        container.appendChild(block);
        return block;
      }
      let block = document.getElementById(`${eachBlock.id}`) || blockView();
      block.setAttribute('transform', `translate(${Block.WIDTH * eachBlock.x }, ${(Viewport.CANVAS_HEIGHT - Block.HEIGHT) - (Block.HEIGHT * eachBlock.y)})`)
    })
  }
// Render the display cubes on the svg canvas
renderBlocks(displayCubes, svg)
// Render the preview blocks
renderBlocks(s.previewBlocks.blocks, preview)

levelText.textContent = `${s.level}`;
scoreText.textContent = `${s.score}`;
highScoreText.textContent = `${s.highscore}`;

// Remove exit blocks from the canvas
s.exitBlocks.forEach((eachBlock) => {
    const block = document.getElementById(`${eachBlock.id}`);
    if (block) {
        svg.removeChild(block);
    }
});

if (s.gameEnd) {
    // Display the game over message
    show(gameover);
    // Remove all rectangles from the svg canvas and preview
    svg.querySelectorAll('rect').forEach(node => node.remove());
    preview.innerHTML = '';
} else {
    // Hide the game over message
    hide(gameover);
}
};