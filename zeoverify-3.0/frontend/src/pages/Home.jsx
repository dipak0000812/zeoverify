export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-100 to-blue-50 p-4">
      <h1 className="text-3xl font-bold mb-4">Welcome to ZeoVerify</h1>
      <p className="text-gray-700 mb-6 text-center max-w-md">
        Verify legal & rental documents instantly using Blockchain + AI.
      </p>
      <a
        href="/upload"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Start Verification
      </a>
    </div>
  );
}
