import { useState } from 'react';
import { useStore } from '../store/useStore';
import { Grid3X3 } from 'lucide-react';

export default function MinesPage() {
  const { user } = useStore();
  const [numMines, setNumMines] = useState(5);
  const [betAmount, setBetAmount] = useState('1.00');
  const [gameStarted, setGameStarted] = useState(false);
  const [field, setField] = useState<number[]>(Array(25).fill(-1));
  const [revealedCells, setRevealedCells] = useState<number[]>([]);

  const handleStartGame = () => {
    setGameStarted(true);
    setField(Array(25).fill(-1));
    setRevealedCells([]);
  };

  const handleCellClick = (index: number) => {
    if (!gameStarted || revealedCells.includes(index)) return;
    
    // TODO: Call API to reveal cell
    setRevealedCells([...revealedCells, index]);
  };

  return (
    <div className="space-y-6">
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            <Grid3X3 className="w-6 h-6 text-blue-400" />
            <h1 className="text-2xl font-bold text-white">Мины</h1>
          </div>
          <div className="glass px-4 py-2 rounded-lg">
            <span className="text-green-400 font-bold">${user?.balance.toFixed(2)}</span>
          </div>
        </div>

        {!gameStarted ? (
          <div className="space-y-4">
            <div>
              <label className="text-gray-400 text-sm mb-2 block">Количество мин</label>
              <select
                value={numMines}
                onChange={(e) => setNumMines(Number(e.target.value))}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg"
              >
                {[...Array(23)].map((_, i) => (
                  <option key={i} value={i + 2}>{i + 2} мин</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-gray-400 text-sm mb-2 block">Ставка</label>
              <input
                type="number"
                value={betAmount}
                onChange={(e) => setBetAmount(e.target.value)}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg"
                step="0.1"
                min="0.3"
              />
            </div>

            <button onClick={handleStartGame} className="w-full btn-primary">
              Начать игру
            </button>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-5 gap-2 mb-4">
              {field.map((cell, index) => (
                <button
                  key={index}
                  onClick={() => handleCellClick(index)}
                  className={`aspect-square rounded-lg text-xl font-bold transition-all ${
                    revealedCells.includes(index)
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-800 hover:bg-gray-700 text-gray-600'
                  }`}
                >
                  {revealedCells.includes(index) ? '💎' : '?'}
                </button>
              ))}
            </div>

            <div className="flex gap-2">
              <button className="flex-1 bg-green-600 text-white py-3 rounded-lg font-bold">
                Вывести x1.00
              </button>
              <button 
                onClick={() => setGameStarted(false)}
                className="flex-1 bg-red-600 text-white py-3 rounded-lg font-bold"
              >
                Закончить
              </button>
            </div>
          </>
        )}
      </div>

      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-white font-bold mb-4">Как играть?</h2>
        <ul className="space-y-2 text-gray-400 text-sm">
          <li>• Выберите количество мин (2-24)</li>
          <li>• Открывайте безопасные клетки</li>
          <li>• Множитель растёт с каждой клеткой</li>
          <li>• Выведите до того как попадете на мину</li>
        </ul>
      </div>
    </div>
  );
}
