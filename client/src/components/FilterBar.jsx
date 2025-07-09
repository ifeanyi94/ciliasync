// components/FilterBar.jsx
import { useState } from 'react';

export default function FilterBar({ onFilter }) {
  const [condition, setCondition] = useState('');
  const [tag, setTag] = useState('');
  const [dateRange, setDateRange] = useState({ start: '', end: '' });

  const handleApply = () => {
    onFilter({
      condition,
      tags: tag,
      start_date: dateRange.start,
      end_date: dateRange.end,
    });
  };

  return (
    <div className="flex gap-4 p-4">
      <input
        type="text"
        placeholder="Condition"
        value={condition}
        onChange={(e) => setCondition(e.target.value)}
      />
      <input
        type="text"
        placeholder="Tag"
        value={tag}
        onChange={(e) => setTag(e.target.value)}
      />
      <input
        type="date"
        onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
      />
      <input
        type="date"
        onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
      />
      <button onClick={handleApply} className="bg-blue-500 text-white px-4 py-2 rounded">
        Apply
      </button>
    </div>
  );
}
