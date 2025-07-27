import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between">
      <Link to="/" className="font-bold">ZeoVerify</Link>
      <div className="space-x-4">
        <Link to="/upload">Upload</Link>
        <Link to="/result">Result</Link>
      </div>
    </nav>
  );
}
