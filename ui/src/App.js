import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';


/**
 * Returns whether or not a column should be editable based on the column name.
 */
function nonEditableField(key) {
  return key == "state" || key == "date";
}


/**
 * Component that wraps an editable column.
 */
function EditableField({ key, state, date, col, val, onChange }) {
  const [innerValue, setInnerValue] = useState(val);

  return (
    <input
      type="text"
      name={key}
      value={innerValue}
      onInput={(evt) => {
        setInnerValue(evt.target.value);
        onChange(state, date, col, evt.target.value);
      }}
    />
  );
}


/**
 * Table component that displays COVID stats.
 */
function TableComponent({ rows, onColumnEdit }) {
  if (rows === undefined || rows.length == 0) {
    return <table></table>;
  }

  const firstRecord = rows[0];

  return (
    <table>
      <thead>
        <tr>
          {Object.keys(firstRecord).map((key) => <th>{key}</th>)}
        </tr>
      </thead>
      <tbody>
        {Object.values(rows).map((row) => (
          <tr>{
            Object.entries(row).map(([key, val]) =>
              nonEditableField(key)
                ? <td>{val}</td>
                : <td>
                    <EditableField
                      key={`edit-${key}-${row["date"]}-${row["state"]}`}
                      state={row["state"]}
                      date={row["date"]}
                      col={key}
                      val={val || 0}
                      onChange={onColumnEdit}
                    />
                  </td>)
          }</tr>
        ))}
      </tbody>
    </table>
  );
}


/**
 * Pagination component to iterate across COVID stat results.
 */
function PagesComponent({ currentPage, onNextPage, onPrevPage }) {
  return (
    <div className="pagination">
      <button onClick={onNextPage}>Next</button>
      <div>Page: ({currentPage})</div>
      <button onClick={onPrevPage}>Prev</button>
    </div>
  );
}


/**
 * Component that allows the number of results to be edited.
 */
function PageSizeComponent({ pageSize, onChange }) {
  return (
    <div>
      <input type="text" name="pageSize" onInput={onChange} value={pageSize} />
    </div>
  );
}


function App() {
  const [data, setData] = useState([]);
  const [page, setPage] = useState(0);
  const [numRows, setNumRows] = useState(100);

  useEffect(() => {
    console.log("Fetching COVID stats")
    fetch(`http://localhost:5001/covid-stats/state-stats?page=${page}&page_size=${numRows}`)
      .then(response => response.json())
      .then(json => setData(json))
      .catch(error => console.error(error));
  }, [page, numRows]);

  return (
    <div className="App">
      <PagesComponent 
        currentPage={page}
        onNextPage={() => setPage(Math.max(page + 1, 0))}
        onPrevPage={() => setPage(Math.max(page - 1, 0))}
      />
      <PageSizeComponent pageSize={numRows} onChange={(evt) => setNumRows(evt.target.value)} />
      <TableComponent
        rows={data}
        onColumnEdit={(state, date, column, newValue) => {
          fetch(`http://localhost:5001/covid-stats/state-stats/${state}/${date}`, {
            method: "PATCH",
            headers: {
              "Accept": "application/json",
              "Content-Type": "application/json"
            },
            body: JSON.stringify({[column]: newValue})
          });
        }}
      />
    </div>
  );
}

export default App;
