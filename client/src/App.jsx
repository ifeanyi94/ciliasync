import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ImageUpload from './components/ImageUpload';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen w-full overflow-x-hidden bg-gray-100">
        <Routes>
          <Route path="/" element={<ImageUpload />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Redirect any unknown paths to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
