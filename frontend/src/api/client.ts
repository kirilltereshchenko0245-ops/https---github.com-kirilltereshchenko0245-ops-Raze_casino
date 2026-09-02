import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authApi = {
  init: (initData: string) => 
    apiClient.post('/auth/init', { init_data: initData }),
  
  getMe: (telegramId: number) =>
    apiClient.get(`/auth/me?telegram_id=${telegramId}`),
};

// Crash game API
export const crashApi = {
  placeBet: (betAmount: number, telegramId: number, clientSeed?: string) =>
    apiClient.post('/games/crash/bet', { 
      bet_amount: betAmount,
      client_seed: clientSeed 
    }, { 
      params: { telegram_id: telegramId } 
    }),
  
  cashout: (gameId: number, cashoutMultiplier: number, telegramId: number) =>
    apiClient.post('/games/crash/cashout', {
      game_id: gameId,
      cashout_multiplier: cashoutMultiplier
    }, {
      params: { telegram_id: telegramId }
    }),
};

// Mines game API
export const minesApi = {
  start: (betAmount: number, numMines: number, telegramId: number, clientSeed?: string) =>
    apiClient.post('/games/mines/start', {
      bet_amount: betAmount,
      num_mines: numMines,
      client_seed: clientSeed
    }, {
      params: { telegram_id: telegramId }
    }),
  
  reveal: (gameId: number, cellIndex: number, telegramId: number) =>
    apiClient.post('/games/mines/reveal', {
      game_id: gameId,
      cell_index: cellIndex
    }, {
      params: { telegram_id: telegramId }
    }),
  
  cashout: (gameId: number, telegramId: number) =>
    apiClient.post('/games/mines/cashout', {
      game_id: gameId
    }, {
      params: { telegram_id: telegramId }
    }),
};

// Game history API
export const gamesApi = {
  getHistory: (telegramId: number, limit = 20, offset = 0) =>
    apiClient.get('/games/history', {
      params: { telegram_id: telegramId, limit, offset }
    }),
};
