import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const RegisterForm = ({ onToggleMode }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    user_class: 'warrior'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic validation
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      setLoading(false);
      return;
    }

    console.log('Submitting registration data:', {
      ...formData,
      password: '[HIDDEN]'
    });

    const result = await register(formData);
    if (!result.success) {
      console.error('Registration failed:', result.error);
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="glass-effect rounded-lg p-8 shadow-xl">
      <h2 className="text-3xl font-bold text-white mb-6 text-center">Join Singularity</h2>
      
      {error && (
        <div className="bg-red-500 text-white p-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <input
              type="text"
              placeholder="Username"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:border-white"
              required
              minLength={3}
            />
          </div>
          
          <div>
            <select
              value={formData.user_class}
              onChange={(e) => setFormData({ ...formData, user_class: e.target.value })}
              className="w-full p-3 rounded-lg bg-white/20 text-white border border-white/30 focus:outline-none focus:border-white"
            >
              <option value="warrior" className="text-black">Warrior</option>
              <option value="mage" className="text-black">Mage</option>
              <option value="rogue" className="text-black">Rogue</option>
              <option value="cleric" className="text-black">Cleric</option>
            </select>
          </div>
        </div>
        
        <div>
          <input
            type="text"
            placeholder="Full Name"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:border-white"
            required
            minLength={2}
          />
        </div>
        
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
            placeholder="Password (min 8 characters)"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="w-full p-3 rounded-lg bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:border-white"
            required
            minLength={8}
          />
          <p className="text-white/60 text-sm mt-1">
            Password must contain uppercase, lowercase, number, and be 8+ characters
          </p>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-white text-blue-600 py-3 rounded-lg font-semibold hover:bg-blue-50 transition duration-200 disabled:opacity-50"
        >
          {loading ? 'Creating Account...' : 'Start Your Journey'}
        </button>
      </form>
      
      <p className="text-white text-center mt-4">
        Already have an account?{' '}
        <button
          onClick={onToggleMode}
          className="text-white font-semibold hover:underline"
        >
          Login
        </button>
      </p>
    </div>
  );
};

export default RegisterForm;