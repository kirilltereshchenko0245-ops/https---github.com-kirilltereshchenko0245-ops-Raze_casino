import { useStore } from '../store/useStore';
import { Disc } from 'lucide-react';

export default function RoulettePage() {
  const { user } = useStore();

  return (
    <div className="space-y-6">
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            <Disc className="w-6 h-6 text-pink-400" />
            <h1 className="text-2xl font-bold text-white">Рулетка</h1>
          </div>
          <div className="glass px-4 py-2 rounded-lg">
            <span className="text-green-400 font-bold">${user?.balance.toFixed(2)}</span>
          </div>
        </div>

        <div className="text-center py-16">
          <div className="text-6xl mb-4">🎡</div>
          <h2 className="text-2xl font-bold text-white mb-2">Скоро</h2>
          <p className="text-gray-400">Игра в разработке</p>
        </div>
      </div>
    </div>
  );
}
