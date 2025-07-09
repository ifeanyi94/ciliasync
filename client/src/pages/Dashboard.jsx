// C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\client\src\pages\Dashboard.jsx

import { useEffect, useState } from 'react';
import { fetchFilteredResults } from '../api/analysis';
import FilterBar from '../components/FilterBar';
import { CiliaCountChart, ColocalizationLineChart, ColocScatterPlot } from '../components/Charts';

export default function Dashboard() {
  const [data, setData] = useState([]);

const handleFilter = async (filters) => {
  try {
    const results = await fetchFilteredResults(filters);
    console.log("DEBUG: API returned", results);

    // Validate that the result is an array
    if (Array.isArray(results)) {
      setData(results);
    } else if (Array.isArray(results.data)) {
      // If it's inside a `data` property
      setData(results.data);
    } else {
      console.error("Expected array but got:", results);
      setData([]); // Fallback to empty array to prevent chart crash
    }
  } catch (err) {
    console.error("Fetch failed", err);
    setData([]); // Fallback in case of error
  }
};



  useEffect(() => {
    handleFilter({});
  }, []);

  return (
    <div className="p-8">
      <h2 className="text-xl font-semibold mb-4">CiliaSync Dashboard</h2>
      <FilterBar onFilter={handleFilter} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <CiliaCountChart data={data} />
        <ColocalizationLineChart data={data} />
        <ColocScatterPlot data={data} />
      </div>
    </div>
  );
}
