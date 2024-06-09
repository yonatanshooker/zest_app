import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';

const App = () => {
  const [repositories, setRepositories] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [userId] = useState('user1'); // For simplicity, assuming a single user

  useEffect(() => {
    const fetchRepositories = async () => {
      const response = await axios.get('http://localhost:8000/top-repositories/');
      setRepositories(response.data);
    };

    const fetchFavorites = async () => {
      const response = await axios.get(`http://localhost:8001/favorites/${userId}`);
      setFavorites(response.data);
    };

    fetchRepositories();
    fetchFavorites();
  }, [userId]);

  const addFavorite = async (repo) => {
    await axios.post('http://localhost:8001/favorites/', {
      user_id: userId,
      repo_id: repo.id,
      repo_name: repo.name,
    });
    setFavorites([...favorites, repo]);
  };

  const removeFavorite = async (repo) => {
    // Assuming there's an endpoint for removing a favorite
    await axios.delete(`http://localhost:8001/favorites/${userId}/${repo.name}`);
    setFavorites(favorites.filter(fav => fav.id !== repo.id));
  };

  return (
    <div>
      <h1>GitHub Top Repositories</h1>
      <Dashboard
        repositories={repositories}
        favorites={favorites}
        addFavorite={addFavorite}
        removeFavorite={removeFavorite}
      />
    </div>
  );
};

export default App;
