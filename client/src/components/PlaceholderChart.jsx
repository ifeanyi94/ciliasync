import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const dummyChartData = [
  { name: 'Sample 1', ciliaCount: 20, colocScore: 0.4 },
  { name: 'Sample 2', ciliaCount: 45, colocScore: 0.82 },
  { name: 'Sample 3', ciliaCount: 32, colocScore: 0.6 },
  { name: 'Sample 4', ciliaCount: 50, colocScore: 0.9 },
];

export default function PlaceholderChart() {
  return (
    <div className="bg-white shadow-md rounded-xl p-4 mt-6 w-full max-w-md mx-auto">
      <h2 className="text-lg font-semibold text-gray-700 mb-2">Sample Analysis Chart</h2>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={dummyChartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis yAxisId="left" label={{ value: 'Cilia Count', angle: -90, position: 'insideLeft' }} />
          <YAxis yAxisId="right" orientation="right" label={{ value: 'Coloc Score', angle: -90, position: 'insideRight' }} />
          <Tooltip />
          <Line yAxisId="left" type="monotone" dataKey="ciliaCount" stroke="#8884d8" />
          <Line yAxisId="right" type="monotone" dataKey="colocScore" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
