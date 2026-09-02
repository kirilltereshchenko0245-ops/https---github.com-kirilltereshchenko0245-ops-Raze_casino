export default function LoadingScreen() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-purple-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <h2 className="text-white text-xl font-bold mb-2">Raze Casino</h2>
        <p className="text-gray-400">Загрузка...</p>
      </div>
    </div>
  );
}
