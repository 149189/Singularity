import React from 'react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white">Singularity</h1>
            <p className="text-white/80">Level up your real life</p>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-white">Welcome, {user.username}</span>
            <button
              onClick={logout}
              className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="glass-effect rounded-lg p-6 text-center">
            <div className="text-2xl font-bold text-white">Level {user.level}</div>
            <div className="text-white/80">Operator</div>
          </div>
          
          <div className="glass-effect rounded-lg p-6">
            <div className="text-white font-semibold mb-2">Strength</div>
            <div className="text-2xl font-bold text-white">{user.attributes?.strength || 1}</div>
          </div>
          
          <div className="glass-effect rounded-lg p-6">
            <div className="text-white font-semibold mb-2">Agility</div>
            <div className="text-2xl font-bold text-white">{user.attributes?.agility || 1}</div>
          </div>
          
          <div className="glass-effect rounded-lg p-6">
            <div className="text-white font-semibold mb-2">Vitality</div>
            <div className="text-2xl font-bold text-white">{user.attributes?.vitality || 1}</div>
          </div>
        </div>

        {/* Main Content */}
        <div className="glass-effect rounded-lg p-6">
          <h2 className="text-2xl font-bold text-white mb-4">Your Journey Awaits</h2>
          <p className="text-white/80">
            Welcome to Singularity, {user.username} the {user.user_class}! 
            Your path to becoming your ultimate self begins now.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;