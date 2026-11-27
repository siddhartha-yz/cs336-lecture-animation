// Sole production palette. Use opacity to establish hierarchy, not desaturation.
export const PALETTE = Object.freeze({
  BLACK:'#000000', PAPER:'#F2F1EC', WHITE:'#FFFFFF', AXIS:'#666666', MUTED:'#B0B8C4',
  BLUE:'#19B5FE', CYAN:'#29ABCA', SKY:'#58C4DD', GOLD:'#FFD43B', AMBER:'#F5C731',
  YELLOW:'#FFFF00', TEAL:'#2EC492', GREEN:'#3DDC84', MINT:'#5CD0B3',
  ORANGE:'#F25C3B', RED:'#E84C5C', MAGENTA:'#DF5296', PINK:'#F462C0', PURPLE:'#B87BFF',
} as const);

// The ink edge of a paper cutout, never a canvas or data color.
export const PAPER_EDGE='#C8C6BE';
