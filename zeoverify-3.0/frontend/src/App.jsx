import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import UploadPage from "./pages/UploadPage";
import ResultPage from "./pages/ResultPage";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/result" element={<ResultPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
