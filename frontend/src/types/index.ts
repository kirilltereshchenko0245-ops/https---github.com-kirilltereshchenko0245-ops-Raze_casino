// User types
export interface User {
  id: number;
  telegram_id: number;
  username?: string;
  first_name: string;
  last_name?: string;
  is_premium: boolean;
  balance: number;
  referral_balance: number;
  wager_amount: number;
  referral_code: string;
  is_banned: boolean;
  task_completed: boolean;
  theme: 'dark' | 'light';
  chat_enabled: boolean;
}

// Game types
export type GameType = 'crash' | 'mines' | 'tower' | 'roulette';

export interface Game {
  id: number;
  user_id: number;
  game_type: GameType;
  status: 'active' | 'won' | 'lost' | 'cashed_out';
  bet_amount: number;
  potential_win: number;
  profit: number;
  commission: number;
  created_at: string;
  finished_at?: string;
}

// Crash game
export interface CrashGameState {
  game_id?: number;
  crash_point?: number;
  current_multiplier: number;
  is_playing: boolean;
  has_cashed_out: boolean;
  bet_amount: number;
}

// Mines game
export interface MinesGameState {
  game_id?: number;
  num_mines: number;
  revealed_cells: number[];
  current_multiplier: number;
  is_playing: boolean;
  bet_amount: number;
}

// Tower game
export interface TowerGameState {
  game_id?: number;
  current_level: number;
  current_multiplier: number;
  is_playing: boolean;
  bet_amount: number;
  chosen_doors: number[];
}

// Roulette game
export interface RouletteGameState {
  is_playing: boolean;
  bet_amount: number;
  bet_on?: 'x2' | 'x3' | 'x5' | 'x30';
  result?: {
    sector: number;
    result: string;
    multiplier: number;
    color: string;
  };
}

// Transaction
export interface Transaction {
  id: number;
  type: string;
  amount: number;
  balance_before: number;
  balance_after: number;
  description?: string;
  created_at: string;
}

// Chat message
export interface ChatMessage {
  id: number;
  user_id: number;
  username: string;
  message: string;
  created_at: string;
}
