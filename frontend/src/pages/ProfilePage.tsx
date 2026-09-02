import { useStore } from '../store/useStore';
import { User, Copy, Gift, Moon, Sun } from 'lucide-react';

export default function ProfilePage() {
  const { user, theme, setTheme } = useStore();

  const copyReferralLink = () => {
    if (user) {
      const link = `https://t.me/RazeCasino_bot?start=${user.referral_code}`;
      navigator.clipboard.writeText(link);
      alert('Ссылка скопирована!');
    }
  };

  return (
    <div className="space-y-6">
      {/* Profile Card */}
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center space-x-4 mb-6">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
            <User className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{user?.first_name}</h1>
            <p className="text-gray-400">@{user?.username || 'user'}</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center py-3 border-b border-gray-700">
            <span className="text-gray-400">Баланс</span>
            <span className="text-white font-bold">${user?.balance.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-gray-700">
            <span className="text-gray-400">Реферальный</span>
            <span className="text-green-400 font-bold">${user?.referral_balance.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center py-3">
            <span className="text-gray-400">Premium</span>
            <span className="text-purple-400 font-bold">
              {user?.is_premium ? '✓' : '✗'}
            </span>
          </div>
        </div>
      </div>

      {/* Referral */}
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Gift className="w-5 h-5 text-purple-400" />
          <h2 className="text-white font-bold">Реферальная программа</h2>
        </div>

        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <p className="text-gray-400 text-sm mb-2">Ваш реферальный код:</p>
            <div className="flex items-center justify-between">
              <code className="text-white font-mono">{user?.referral_code}</code>
              <button
                onClick={copyReferralLink}
                className="p-2 bg-purple-600 rounded-lg hover:bg-purple-700"
              >
                <Copy className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Обычный</p>
              <p className="text-white font-bold text-xl">$0.15</p>
            </div>
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4">
              <p className="text-gray-300 text-sm">Premium</p>
              <p className="text-white font-bold text-xl">$0.20</p>
            </div>
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-white font-bold mb-4">Настройки</h2>
        
        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="w-full flex items-center justify-between py-3 px-4 bg-gray-800 rounded-lg hover:bg-gray-700"
        >
          <span className="text-white">Тема</span>
          <div className="flex items-center space-x-2">
            <span className="text-gray-400">{theme === 'dark' ? 'Тёмная' : 'Светлая'}</span>
            {theme === 'dark' ? (
              <Moon className="w-5 h-5 text-purple-400" />
            ) : (
              <Sun className="w-5 h-5 text-yellow-400" />
            )}
          </div>
        </button>
      </div>
    </div>
  );
}
