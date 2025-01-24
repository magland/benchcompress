import { useEffect, useState } from 'react';
import axios from 'axios';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
} from '@tanstack/react-table';
import { BenchmarkResult } from '../types';

const columnHelper = createColumnHelper<BenchmarkResult>();

const formatNumber = (num: number, decimals = 2) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num);
};

const formatSize = (bytes: number) => {
  const mb = bytes / (1024 * 1024);
  return `${formatNumber(mb)} MB`;
};

const columns = [
  columnHelper.accessor('dataset', {
    header: 'Dataset',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('algorithm', {
    header: 'Algorithm',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('compression_ratio', {
    header: 'Compression Ratio',
    cell: info => `${formatNumber(info.getValue())}x`,
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.compression_ratio;
      const b = rowB.original.compression_ratio;
      return a - b;
    },
  }),
  columnHelper.accessor('encode_time', {
    header: 'Encode Time (s)',
    cell: info => formatNumber(info.getValue(), 4),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.encode_time;
      const b = rowB.original.encode_time;
      return a - b;
    },
  }),
  columnHelper.accessor('decode_time', {
    header: 'Decode Time (s)',
    cell: info => formatNumber(info.getValue(), 4),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.decode_time;
      const b = rowB.original.decode_time;
      return a - b;
    },
  }),
  columnHelper.accessor('encode_mb_per_sec', {
    header: 'Encode Speed (MB/s)',
    cell: info => formatNumber(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.encode_mb_per_sec;
      const b = rowB.original.encode_mb_per_sec;
      return a - b;
    },
  }),
  columnHelper.accessor('decode_mb_per_sec', {
    header: 'Decode Speed (MB/s)',
    cell: info => formatNumber(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.decode_mb_per_sec;
      const b = rowB.original.decode_mb_per_sec;
      return a - b;
    },
  }),
  columnHelper.accessor('original_size', {
    header: 'Original Size',
    cell: info => formatSize(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.original_size;
      const b = rowB.original.original_size;
      return a - b;
    },
  }),
  columnHelper.accessor('compressed_size', {
    header: 'Compressed Size',
    cell: info => formatSize(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.compressed_size;
      const b = rowB.original.compressed_size;
      return a - b;
    },
  }),
];

export function BenchmarkTable() {
  const [data, setData] = useState<BenchmarkResult[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          'https://raw.githubusercontent.com/magland/zia/benchmark-results/benchmark_results/results.json'
        );
        setData(response.data.results);
      } catch (error) {
        console.error('Error fetching benchmark data:', error);
      }
    };

    fetchData();
  }, []);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="table-container">
      <table>
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  style={{ cursor: 'pointer' }}
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                  {header.column.getIsSorted() && (
                    <span style={{ marginLeft: '4px' }}>
                      {header.column.getIsSorted() === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
