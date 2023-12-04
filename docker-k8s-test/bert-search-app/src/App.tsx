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

  const columnData: any[] = [
    { title: 'Id', columnName: 'doc_id', customStyle: 'w-1/5' },
    { title: 'Title', columnName: 'title', customStyle: 'w-2/5' },
    { title: 'Authors', columnName: 'authors' },
    { title: 'Quotes', columnName: 'quotes' },
  ];

  const sendQuery = (query: string) => {
    return fetch('http://127.0.0.1:5000/', {
       method: 'POST',
       body: query,
     }).then((response: any) => {
          console.log(response);
          if (response.status >= 200 && response.status < 300) {
            setIsResponse(true);
            return response.json();
          }
        })
        .then( (data: any) =>  { return data });
  }
  /*
  const sortObj = (obj) => {
    return Object.keys(obj).sort().reduce(function (result, key) {
      result[key] = obj[key];
      return result;
    }, {});
  }
  */
  const gettingData = (input: string) => {
    //e.preventDefault();
    //var input = e.target.elements.keyword.value;
    if (input){
      sendQuery(input).then((data: any) => {
        if (!data) {
          setIsResponse(false);
          return setTableData([]);
        }
        setResponse(data);
        console.log(data.table_data)
        console.log(data.result_docs)
        var ids:any = [];
        data.result_docs.forEach((q_info: any) => {
          if (q_info['id_from'].includes('21911362')){
            // setIdsFound([idsFound, [...q_info['doc_ids']]]);
            //return q_info['doc_ids'];
            // q_info['doc_ids'].forEach((id:any) => {return id});
            ids.push(...q_info['doc_ids']);
          }
        });
        console.log(ids);
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
  //console.log(idsFound)
  //console.log(response);
  /*
  <div className="App">
    <header className="App-header">
      <Form changeHandler={gettingData}/>
    </header>
  </div>
  */
  //console.log(tableData)
  /*<div className="flex">
    {timeQuery}
  </div>*/
  return (

    <div className="mr-5 flex w-full flex-col">
      <div className="box">
        <Title title={'Semantic search demo'} size="large" topOffset="mt-6" />
      </div>
      <div className="box">
        <Form changeHandler={gettingData}/>
      </div>
      {isResponse && (
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
    </div>
  );
}

export default App;
