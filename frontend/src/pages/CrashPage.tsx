import { useState, useEffect, useRef } from 'react';
import { useStore } from '../store/useStore';
import { crashApi } from '../api/client';
import { Zap, TrendingUp } from 'lucide-react';

export default function CrashPage() {
  const { user, updateBalance, crashGame, setCrashGame, resetCrashGame } = useStore();
  const [betAmount, setBetAmount] = useState('1.00');
  const [autoCashout, setAutoCashout] = useState('');
  const [history, setHistory] = useState<number[]>([]);
  const animationRef = useRef<number>();

  useEffect(() => {
    if (crashGame.is_playing && !crashGame.has_cashed_out) {
      startMultiplierAnimation();
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [crashGame.is_playing]);

  const startMultiplierAnimation = () => {
    const startTime = Date.now();
    const animate = () => {
      const elapsed = (Date.now() - startTime) / 1000;
      const multiplier = 1 + elapsed * 0.1; // Grows 0.1x per second
      
      setCrashGame({ current_multiplier: Number(multiplier.toFixed(2)) });
      
      // Check if crashed
      if (crashGame.crash_point && multiplier >= crashGame.crash_point) {
        handleCrash();
        return;
      }
      
      // Check auto cashout
      if (autoCashout && multiplier >= parseFloat(autoCashout)) {
        handleCashout();
        return;
      }
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animationRef.current = requestAnimationFrame(animate);
  };

  const handlePlaceBet = async () => {
    if (!user) return;
    
    const amount = parseFloat(betAmount);
    if (amount < 0.3 || amount > user.balance) {
      alert('Неверная сумма ставки');
      return;
    }

    try {
      const response = await crashApi.placeBet(amount, user.telegram_id);
      const { game_id, crash_point, hash } = response.data;
      
      setCrashGame({
        game_id,
        crash_point,
        bet_amount: amount,
        is_playing: true,
        has_cashed_out: false,
        current_multiplier: 1.0,
      });
      
      // Update balance
      updateBalance(user.balance - amount);
      
    } catch (error) {
      console.error('Failed to place bet:', error);
      alert('Ошибка при размещении ставки');
    }
  };

  const handleCashout = async () => {
    if (!crashGame.game_id || !user || crashGame.has_cashed_out) return;

    try {
      const response = await crashApi.cashout(
        crashGame.game_id,
        crashGame.current_multiplier,
        user.telegram_id
      );
      
      const { success, profit, new_balance } = response.data;
      
      if (success) {
        setCrashGame({ has_cashed_out: true });
        updateBalance(new_balance);
        setHistory([crashGame.current_multiplier, ...history.slice(0, 9)]);
        
        setTimeout(() => {
          resetCrashGame();
        }, 3000);
      } else {
        handleCrash();
      }
    } catch (error) {
      console.error('Failed to cashout:', error);
    }
  };

  const handleCrash = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    
    setCrashGame({ is_playing: false });
    setHistory([crashGame.crash_point || 0, ...history.slice(0, 9)]);
    
    setTimeout(() => {
      resetCrashGame();
    }, 3000);
  };

  const getMultiplierColor = () => {
    const mult = crashGame.current_multiplier;
    if (mult < 1.5) return 'text-gray-400';
    if (mult < 2.0) return 'text-blue-400';
    if (mult < 5.0) return 'text-green-400';
    if (mult < 10.0) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="space-y-6">
      {/* Game Display */}
      <div className="glass-card rounded-2xl p-8 relative overflow-hidden">
        {/* Background Animation */}
        <div className="absolute inset-0 opacity-20">
          <div className={`absolute top-0 left-0 w-full h-full ${
            crashGame.is_playing ? 'bg-gradient-to-t from-purple-600 to-transparent' : ''
          }`}></div>
        </div>

        <div className="relative z-10">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <Zap className="w-6 h-6 text-orange-400" />
              <h1 className="text-2xl font-bold text-white">Краш</h1>
            </div>
            <div className="glass px-4 py-2 rounded-lg">
              <span className="text-green-400 font-bold">${user?.balance.toFixed(2)}</span>
            </div>
          </div>

          {/* Multiplier Display */}
          <div className="text-center py-16">
            {crashGame.is_playing ? (
              <div className="space-y-4">
                <div className={`text-8xl font-bold ${getMultiplierColor()} animate-pulse`}>
                  {crashGame.current_multiplier.toFixed(2)}x
                </div>
                {crashGame.has_cashed_out ? (
                  <div className="text-green-400 text-2xl font-bold">
                    Выведено! 🎉
                  </div>
                ) : (
                  <div className="text-gray-400">
                    <TrendingUp className="w-8 h-8 mx-auto animate-bounce" />
                  </div>
                )}
              </div>
            ) : crashGame.crash_point ? (
              <div className="space-y-4">
                <div className="text-8xl font-bold text-red-500">
                  {crashGame.crash_point.toFixed(2)}x
                </div>
                <div className="text-red-400 text-2xl font-bold">
                  Краш! 💥
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="text-6xl font-bold text-gray-500">
                  1.00x
                </div>
                <div className="text-gray-400">
                  Ждём ставок...
                </div>
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="space-y-4">
            {!crashGame.is_playing ? (
              <>
                <div>
                  <label className="text-gray-400 text-sm mb-2 block">Сумма ставки</label>
                  <input
                    type="number"
                    value={betAmount}
                    onChange={(e) => setBetAmount(e.target.value)}
                    className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                    placeholder="0.00"
                    step="0.1"
                    min="0.3"
                  />
                </div>

                <div>
                  <label className="text-gray-400 text-sm mb-2 block">Авто-вывод (опционально)</label>
                  <input
                    type="number"
                    value={autoCashout}
                    onChange={(e) => setAutoCashout(e.target.value)}
                    className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
                    placeholder="2.00x"
                    step="0.1"
                    min="1.1"
                  />
                </div>

                <button
                  onClick={handlePlaceBet}
                  disabled={!betAmount || parseFloat(betAmount) < 0.3}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Сделать ставку ${betAmount || '0.00'}
                </button>
              </>
            ) : (
              <button
                onClick={handleCashout}
                disabled={crashGame.has_cashed_out}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed text-lg"
              >
                {crashGame.has_cashed_out ? 'Выведено ✓' : `Вывести ${crashGame.current_multiplier.toFixed(2)}x`}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* History */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-white font-bold mb-4">История</h2>
        <div className="flex flex-wrap gap-2">
          {history.length === 0 ? (
            <p className="text-gray-400 text-sm">Нет истории</p>
          ) : (
            history.map((mult, idx) => (
              <div
                key={idx}
                className={`px-4 py-2 rounded-lg font-bold ${
                  mult < 2 ? 'bg-red-900/30 text-red-400' :
                  mult < 5 ? 'bg-green-900/30 text-green-400' :
                  'bg-purple-900/30 text-purple-400'
                }`}
              >
                {mult.toFixed(2)}x
              </div>
            ))
          )}
        </div>
      </div>

      {/* How to Play */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-white font-bold mb-4">Как играть?</h2>
        <ul className="space-y-2 text-gray-400 text-sm">
          <li>• Сделайте ставку до начала раунда</li>
          <li>• Следите за растущим множителем</li>
          <li>• Выведите до того как произойдёт краш</li>
          <li>• Можно установить авто-вывод</li>
        </ul>
      </div>
    </div>
  );
}
