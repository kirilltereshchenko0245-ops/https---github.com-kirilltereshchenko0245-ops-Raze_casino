import { create } from 'zustand';
import { User, CrashGameState, MinesGameState, TowerGameState, RouletteGameState } from '../types';

interface AppState {
  // User
  user: User | null;
  setUser: (user: User | null) => void;
  updateBalance: (balance: number) => void;
  
  // Theme
  theme: 'dark' | 'light';
  setTheme: (theme: 'dark' | 'light') => void;
  
  // Crash game
  crashGame: CrashGameState;
  setCrashGame: (game: Partial<CrashGameState>) => void;
  resetCrashGame: () => void;
  
  // Mines game
  minesGame: MinesGameState;
  setMinesGame: (game: Partial<MinesGameState>) => void;
  resetMinesGame: () => void;
  
  // Tower game
  towerGame: TowerGameState;
  setTowerGame: (game: Partial<TowerGameState>) => void;
  resetTowerGame: () => void;
  
  // Roulette game
  rouletteGame: RouletteGameState;
  setRouletteGame: (game: Partial<RouletteGameState>) => void;
  resetRouletteGame: () => void;
  
  // UI
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
}

const initialCrashGame: CrashGameState = {
  current_multiplier: 1.0,
  is_playing: false,
  has_cashed_out: false,
  bet_amount: 0,
};

const initialMinesGame: MinesGameState = {
  num_mines: 5,
  revealed_cells: [],
  current_multiplier: 1.0,
  is_playing: false,
  bet_amount: 0,
};

const initialTowerGame: TowerGameState = {
  current_level: 0,
  current_multiplier: 1.0,
  is_playing: false,
  bet_amount: 0,
  chosen_doors: [],
};

const initialRouletteGame: RouletteGameState = {
  is_playing: false,
  bet_amount: 0,
};

export const useStore = create<AppState>((set) => ({
  // User
  user: null,
  setUser: (user) => set({ user }),
  updateBalance: (balance) => 
    set((state) => ({
      user: state.user ? { ...state.user, balance } : null
    })),
  
  // Theme
  theme: 'dark',
  setTheme: (theme) => set({ theme }),
  
  // Crash game
  crashGame: initialCrashGame,
  setCrashGame: (game) =>
    set((state) => ({
      crashGame: { ...state.crashGame, ...game }
    })),
  resetCrashGame: () => set({ crashGame: initialCrashGame }),
  
  // Mines game
  minesGame: initialMinesGame,
  setMinesGame: (game) =>
    set((state) => ({
      minesGame: { ...state.minesGame, ...game }
    })),
  resetMinesGame: () => set({ minesGame: initialMinesGame }),
  
  // Tower game
  towerGame: initialTowerGame,
  setTowerGame: (game) =>
    set((state) => ({
      towerGame: { ...state.towerGame, ...game }
    })),
  resetTowerGame: () => set({ towerGame: initialTowerGame }),
  
  // Roulette game
  rouletteGame: initialRouletteGame,
  setRouletteGame: (game) =>
    set((state) => ({
      rouletteGame: { ...state.rouletteGame, ...game }
    })),
  resetRouletteGame: () => set({ rouletteGame: initialRouletteGame }),
  
  // UI
  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),
}));
