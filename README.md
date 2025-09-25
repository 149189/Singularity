# Singularity - Personal Evolution Platform 🚀

> **Level Up Your Real Life** - Transform your physical and mental fitness into an epic RPG adventure!



## 🌟 Overview

Singularity is a gamified personal development platform that turns real-world exercises and activities into an immersive RPG experience. Track your fitness, learning, and wellness journey while leveling up your character across four core attributes: **Strength**, **Agility**, **Vitality**, and **Intelligence**.

## 🎮 Key Features

### 🏋️‍♂️ Gamified Fitness Tracking
- **Real-World Exercise Logging**: Convert workouts into in-game experience
- **Attribute Progression**: Level up Strength, Agility, Vitality, and Intelligence
- **Skill Trees**: Unlock specialized paths within each attribute
- **Experience Points**: Earn XP for completed exercises and activities

### 🏆 Quest System
- **Daily & Weekly Quests**: Regular challenges to keep you engaged
- **Story Campaign**: Epic narrative guiding your personal growth journey
- **PvE Challenges**: Battle virtual enemies through physical exercises
- **Community Quests**: Collaborate with other players on massive goals

### 👥 Social & Competitive
- **Clans & Guilds**: Team up with friends for group challenges
- **Leaderboards**: Compete globally and within your class
- **PvP Duels**: Challenge friends to head-to-head workout battles
- **Achievement System**: Unlock badges and rewards for milestones

### 🎯 Personalization
- **Character Classes**: Choose from Warrior, Mage, Rogue, or Cleric
- **Custom Avatars**: Visual representation of your progress
- **Item System**: Equip gear that provides stat bonuses
- **Progress Analytics**: Detailed insights into your growth journey

## 🛠 Technology Stack

### Backend
- **Python** with **FastAPI** - High-performance API framework
- **MongoDB** - Flexible NoSQL database for player data
- **Motor** - Async MongoDB driver
- **JWT** - Secure authentication
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB 5.0+
- Git

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/singularity.git
cd singularity

Backend Setup - 
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB credentials

Frontend Setup -
cd ../frontend

# Install dependencies
npm install

4. Database Setup
Ensure MongoDB is running on your system.

5. Run the Application
Terminal 1 - Backend:

bash
cd backend
uvicorn app.main:app --reload --port 8000
Terminal 2 - Frontend:

bash
cd frontend
npm run dev
6. Access the Application
Frontend: http://localhost:3000

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs
```

.env.example

MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=singularity
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
