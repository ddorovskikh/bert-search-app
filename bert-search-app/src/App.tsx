import React from 'react';
import Form from "./components/Form";
import { useState, useEffect } from 'react';
import Table from './components/Table';
import Title from './components/Title';

function App() {
  const [isResponse, setIsResponse] = useState(false);
  const [response, setResponse] = useState({});
  const [tableData, setTableData] = useState<any>([]);
  const [timeQuery, setTimeQuery] = useState<number>();
  const [idsFound, setIdsFound] = useState<any>([]);
  const [error, setError] = useState<string>('');

  const columnData: any[] = [
    { title: 'Id', columnName: 'doc_id', customStyle: 'w-1/5' },
    { title: 'Title', columnName: 'title', customStyle: 'w-2/5' },
    { title: 'Authors', columnName: 'authors' },
    { title: 'Quotes', columnName: 'quotes' },
  ];

  const sendQuery = (query: string) => {
    var query_json = { "query": query }
    return fetch('http://127.0.0.1:5000/', {
       method: 'POST',
       body: JSON.stringify(query_json),
     }).then((response: any) => {
          console.log(response);
          if (response.status >= 200 && response.status < 300) {
            setIsResponse(true);
            return response.json();
          }
        })
        .then( (data: any) =>  { return data });
  }

  const gettingData = (input: string) => {
    if (input){
      sendQuery(input).then((data: any) => {
        if (!data) {
          setIsResponse(false);
          return setTableData([]);
        }
        setResponse(data);
        if (data.error) {
          setError(data.error);
          return setTableData([]);
        } else {
          setError('');
        }
        var ids:any = [];
        data.result_docs.forEach((q_info: any) => {
          if (q_info['id_from'].includes('21911362')){
            ids.push(...q_info['doc_ids']);
          }
        });
        setTableData(Object.values(data.table_data).map((item: any) => {
          if ('authors' in item && item.authors.length) {
            var authors: string = item.authors.join(", ")
          }
          else {
            var authors: string = ''
          }
          return {
            doc_id: item.doc_id,
            title: item.title,
            authors: authors,
            quotes: item.quotes.join(", ")
          }
        }));
        setTimeQuery(data.time * 60);
      });
    }
  }

  return (

    <div className="mr-5 flex w-full flex-col">
      <div className="box">
        <Title title={'Semantic search demo'} size="large" topOffset="mt-6" />
      </div>
      <div className="box">
        <Form changeHandler={gettingData}/>
      </div>
      {isResponse && !error && (
        <>
          <div
            className={`mt-6 mb-6 flex flex-1 flex-col rounded bg-white px-7 pt-7 pb-8 shadow-card dark:border dark:border-neutral-600 dark:bg-neutral-900`}
          >
            <Table
              columnData={columnData}
              tableData={tableData}
            />
          </div>
        </>
      )}
      {error && (
        <div
          className={`text-center mt-10 mb-10`}
        >
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
