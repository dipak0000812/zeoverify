export default function FileCard({ file }) {
  return (
    <div className="mt-4 p-3 bg-white bg-opacity-30 backdrop-blur rounded shadow text-white text-sm">
      Selected file: <span className="font-medium">{file.name}</span>
    </div>
  );
}
