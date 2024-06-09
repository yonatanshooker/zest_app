import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';

const Dashboard = ({ repositories, favorites, addFavorite, removeFavorite }) => {
  const [sortOption, setSortOption] = useState('stars');

  const sortedRepositories = [...repositories].sort((a, b) => {
    if (sortOption === 'stars') {
      return b.stargazers_count - a.stargazers_count;
    } else if (sortOption === 'name') {
      return a.name.localeCompare(b.name);
    } else {
      return 0;
    }
  });

  const data = {
    labels: sortedRepositories.map(repo => repo.name),
    datasets: [
      {
        label: 'Stars',
        data: sortedRepositories.map(repo => repo.stargazers_count),
        backgroundColor: 'rgba(75,192,192,0.4)',
      },
    ],
  };

  return (
    <div>
      <div>
        <label>Sort by: </label>
        <select value={sortOption} onChange={(e) => setSortOption(e.target.value)}>
          <option value="stars">Stars</option>
          <option value="name">Name</option>
        </select>
      </div>
      <Bar data={data} />
      <ul>
        {sortedRepositories.map(repo => (
          <li key={repo.id}>
            {repo.name} ({repo.stargazers_count} stars)
            {favorites.some(fav => fav.id === repo.id) ? (
              <button onClick={() => removeFavorite(repo)}>Remove from Favorites</button>
            ) : (
              <button onClick={() => addFavorite(repo)}>Add to Favorites</button>
            )}
          </li>
        ))}
      </ul>
      <h2>Favorite Repositories</h2>
      <ul>
        {favorites.map(fav => (
          <li key={fav.id}>{fav.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
