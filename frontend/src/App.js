import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { useTable } from 'react-table';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [submittedQuestion, setSubmittedQuestion] = useState('');
  const [processedData, setProcessedData] = useState([]);

  useEffect(() => {
    fetchUploads();
  }, []);

  const fetchUploads = async () => {
    try {
      const response = await axios.get('http://localhost:5000/uploads');
      console.log('Uploads:', response.data);  // Debugging: Print uploads data
      setProcessedData(response.data[0]?.processedData || []);
    } catch (error) {
      console.error('Error fetching uploads:', error);
    }
  };

  const handleChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/upload', { question });
      console.log('Processed Data:', response.data.processedData);  // Debugging: Print processed data
      setSubmittedQuestion(response.data.question);
      setProcessedData(response.data.processedData || []);
    } catch (error) {
      console.error('Error submitting question:', error);
    }
    setQuestion('');
  };

  // Helper function to remove all single and double quotes and split correctly
  const sanitizeAndSplitString = (str) => {
    // Replace single and double quotes
    const sanitizedString = str.replace(/['"]/g, '');
    // Replace "][" with a placeholder
    const placeholder = '__SPLIT__';
    const cleanedString = sanitizedString.replace(/\],\[/g, `]${placeholder}[`);
    // Split the string by the placeholder and parse each part
    return cleanedString.split(placeholder).map(part => part.replace(/^\[|\]$/g, '').split(',').map(item => item.trim()));
  };

  // Parse the sanitized string into a JSON array
  const parseData = (data) => {
    try {
      const sanitizedData = data.flatMap(item =>
        typeof item === 'string' ? sanitizeAndSplitString(item) : [item]
      );
      console.log('Parsed Data:', sanitizedData);  // Debugging: Print parsed data
      return sanitizedData;
    } catch (error) {
      console.error('Error parsing data:', data, error);
      return [];
    }
  };

  const parsedData = useMemo(() => parseData(processedData), [processedData]);

  const columns = useMemo(() => {
    if (parsedData.length > 0) {
      const headers = ["pk", "export_data",
        "export_date_raw", "itunes_release",
        "original_release", "parental_advisory_id",
        "preview_length", "preview_length_raw", "song_id",
        "track_length", "track_length_raw", "artist_display_name",
        "collection_display_name",
        "copyright", "name", "p_line", "preview_url",
        "search_terms", "title_version", "view_url", "isrc", "blank", "blank"];
      return headers.map((header, index) => ({
        Header: header,
        accessor: String(index),
      }));
    }
    return [];
  }, [parsedData]);

  const data = useMemo(
    () => parsedData.map((item, index) => {
      const row = {};
      if (Array.isArray(item)) {
        item.forEach((cell, cellIndex) => {
          row[String(cellIndex)] = cell;
        });
      }
      return row;
    }),
    [parsedData]
  );

  console.log('Table Data:', data);  // Debugging: Print table data

  const tableInstance = useTable({ columns, data });

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = tableInstance;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Music AI</h1>
        {submittedQuestion ? (
          <div>
            <h2>Your Question:</h2>
            <p>{submittedQuestion}</p>
            <h2>Answer:</h2>
            {data.length > 0 ? (
              <div className="table-container">
                <table {...getTableProps()} className="table">
                  <thead>
                    {headerGroups.map(headerGroup => (
                      <tr {...headerGroup.getHeaderGroupProps()} key={headerGroup.id}>
                        {headerGroup.headers.map(column => (
                          <th {...column.getHeaderProps()} key={column.id} className="header-cell">
                            {column.render('Header')}
                          </th>
                        ))}
                      </tr>
                    ))}
                  </thead>
                  <tbody {...getTableBodyProps()}>
                    {rows.map(row => {
                      prepareRow(row);
                      return (
                        <tr {...row.getRowProps()} key={row.id}>
                          {row.cells.map(cell => (
                            <td {...cell.getCellProps()} key={cell.column.id} className="body-cell">
                              {cell.render('Cell')}
                            </td>
                          ))}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            ) : (
              <p>No data available</p>
            )}
            <button onClick={() => setSubmittedQuestion('')}>Ask another question</button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <label>
              Enter your question:
              <input type="text" value={question} onChange={handleChange} />
            </label>
            <button type="submit">Submit</button>
          </form>
        )}
      </header>
    </div>
  );
}

export default App;






















