import { useStore } from '../store/useStore';
import { History } from 'lucide-react';

export default function HistoryPage() {
  const { user } = useStore();

  return (
    <div className="space-y-6">
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center space-x-2 mb-6">
          <History className="w-6 h-6 text-blue-400" />
          <h1 className="text-2xl font-bold text-white">История игр</h1>
        </div>

        <div className="text-center py-16">
          <p className="text-gray-400">История игр пуста</p>
        </div>
      </div>
    </div>
  );
}
