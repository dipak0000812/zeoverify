export default function ResultPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white p-4">
      <h2 className="text-2xl font-semibold mb-4">Verification Result</h2>
      <p className="text-gray-700">AI + Blockchain says: Document is Genuine ✅</p>
      <a href="/upload" className="mt-4 text-blue-600 underline">Verify another document</a>
    </div>
  );
}
