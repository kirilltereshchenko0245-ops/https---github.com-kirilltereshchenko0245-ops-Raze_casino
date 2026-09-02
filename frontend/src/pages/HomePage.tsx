import { Link } from 'react-router-dom';
import { Zap, Grid3X3, Castle, Disc } from 'lucide-react';
import { useStore } from '../store/useStore';

export default function HomePage() {
  const { user } = useStore();

  const games = [
    {
      id: 'crash',
      name: 'Краш',
      icon: Zap,
      description: 'Поймай момент до краша',
      color: 'from-orange-500 to-red-600',
      path: '/crash',
    },
    {
      id: 'mines',
      name: 'Мины',
      icon: Grid3X3,
      description: 'Открывай безопасные клетки',
      color: 'from-blue-500 to-purple-600',
      path: '/mines',
    },
    {
      id: 'tower',
      name: 'Башня',
      icon: Castle,
      description: 'Поднимайся по уровням',
      color: 'from-green-500 to-teal-600',
      path: '/tower',
    },
    {
      id: 'roulette',
      name: 'Рулетка',
      icon: Disc,
      description: 'x2, x3, x5, x30',
      color: 'from-pink-500 to-rose-600',
      path: '/roulette',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="glass-card rounded-2xl p-6">
        <h1 className="text-3xl font-bold text-white mb-2">
          Привет, {user?.first_name || 'Игрок'}! 👋
        </h1>
        <p className="text-gray-400">
          Добро пожаловать в Raze Casino
        </p>
        
        <div className="grid grid-cols-2 gap-4 mt-6">
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl p-4">
            <p className="text-gray-300 text-sm">Баланс</p>
            <p className="text-white text-2xl font-bold">
              ${user?.balance.toFixed(2) || '0.00'}
            </p>
          </div>
          
          <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-xl p-4">
            <p className="text-gray-300 text-sm">Реферальный</p>
            <p className="text-white text-2xl font-bold">
              ${user?.referral_balance.toFixed(2) || '0.00'}
            </p>
          </div>
        </div>
      </div>

      {/* Games Grid */}
      <div>
        <h2 className="text-white text-xl font-bold mb-4">🎮 Игры</h2>
        <div className="grid grid-cols-2 gap-4">
          {games.map((game) => {
            const Icon = game.icon;
            return (
              <Link key={game.id} to={game.path}>
                <div className="glass-card rounded-2xl p-6 hover:scale-105 transition-transform cursor-pointer">
                  <div className={`w-12 h-12 bg-gradient-to-r ${game.color} rounded-xl flex items-center justify-center mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-white font-bold text-lg mb-1">{game.name}</h3>
                  <p className="text-gray-400 text-sm">{game.description}</p>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Stats */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-white text-xl font-bold mb-4">📊 Статистика</h2>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Всего игр</span>
            <span className="text-white font-bold">0</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Выиграно</span>
            <span className="text-green-400 font-bold">$0.00</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Рефералов</span>
            <span className="text-purple-400 font-bold">0</span>
          </div>
        </div>
      </div>
    </div>
  );
}
