import { BenchmarkTable } from './components/BenchmarkTable';

function App() {
  return (
    <div style={{ padding: '2rem' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 'bold',
          color: '#333'
        }}>
          Zia Compression Benchmark Results
        </h1>
        <p style={{
          color: '#666',
          marginTop: '0.5rem'
        }}>
          Comparing different compression algorithms and their performance
        </p>
      </header>
      <main>
        <BenchmarkTable />
      </main>
    </div>
  );
}

export default App;
