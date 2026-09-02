import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useStore } from './store/useStore';
import { authApi } from './api/client';

// Pages
import HomePage from './pages/HomePage';
import CrashPage from './pages/CrashPage';
import MinesPage from './pages/MinesPage';
import TowerPage from './pages/TowerPage';
import RoulettePage from './pages/RoulettePage';
import ProfilePage from './pages/ProfilePage';
import HistoryPage from './pages/HistoryPage';

// Layout
import Layout from './components/Layout';
import LoadingScreen from './components/LoadingScreen';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  const { user, setUser, theme, setLoading, isLoading } = useStore();

  useEffect(() => {
    initApp();
  }, []);

  const initApp = async () => {
    try {
      setLoading(true);
      
      // Check if running in Telegram
      if (window.Telegram?.WebApp) {
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        
        // Get init data
        const initData = tg.initData;
        
        if (initData) {
          // Authenticate with backend
          const response = await authApi.init(initData);
          const { access_token, user: userData } = response.data;
          
          // Save token
          localStorage.setItem('access_token', access_token);
          
          // Set user
          setUser(userData);
        }
      } else {
        // Development mode - mock user
        console.log('Running in development mode');
        setUser({
          id: 1,
          telegram_id: 123456789,
          username: 'testuser',
          first_name: 'Test',
          is_premium: false,
          balance: 100.0,
          referral_balance: 10.0,
          wager_amount: 0,
          referral_code: 'REF123',
          is_banned: false,
          task_completed: true,
          theme: 'dark',
          chat_enabled: true,
        });
      }
    } catch (error) {
      console.error('Failed to initialize app:', error);
    } finally {
      setLoading(false);
    }
  };

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className={theme === 'dark' ? 'dark' : ''}>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/crash" element={<CrashPage />} />
              <Route path="/mines" element={<MinesPage />} />
              <Route path="/tower" element={<TowerPage />} />
              <Route path="/roulette" element={<RoulettePage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </div>
    </QueryClientProvider>
  );
}

export default App;
