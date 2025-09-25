import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const LoginForm = ({ onToggleMode }) => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(formData);
    if (!result.success) {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="glass-effect rounded-lg p-8 shadow-xl">
      <h2 className="text-3xl font-bold text-white mb-6 text-center">Login to Singularity</h2>
      
      {error && (
        <div className="bg-red-500 text-white p-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:border-white"
            required
          />
        </div>
        
        <div>
          <input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:border-white"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-white text-blue-600 py-3 rounded-lg font-semibold hover:bg-blue-50 transition duration-200 disabled:opacity-50"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <p className="text-white text-center mt-4">
        Don't have an account?{' '}
        <button
          onClick={onToggleMode}
          className="text-white font-semibold hover:underline"
        >
          Register
        </button>
      </p>
    </div>
  );
};

export default LoginForm;