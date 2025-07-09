import axios from 'axios';

export const fetchFilteredResults = async (params) => {
  // Use full URL to Django backend API endpoint
  const response = await axios.get('http://127.0.0.1:8000/api/results/filter/', { params });
  return response.data;
};
