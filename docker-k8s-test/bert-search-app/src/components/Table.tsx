import type { ReactElement } from 'react';
import { useState } from 'react';

import Line from './Line';


export interface IColumnData {
  title: string;
  columnName: string;
  customStyle?: string;
  widthStyle?: string;
  stateData?: any;
}

interface ITableProps {
  columnData: IColumnData[];
  tableData: any;
}

const itemsOnPage = [
  { name: '5', value: 5 },
  { name: '10', value: 10 },
  { name: '25', value: 25 },
  { name: '50', value: 50 },
];

export default function Table(props: ITableProps) {
  /*
  const [currentLimit, setCurrentLimit] = useState<number>(
    props.hidePagination ? -1 : props.currentLimit ? props.currentLimit : 25,
  );
  const [currentPage, setCurrentPage] = useState<number>(1);

  const updateLimit = (index: number) => {
    const newLimit = itemsOnPage[index].value;
    setCurrentLimit(newLimit);
    setCurrentPage(1);
    props.limitChange?.(newLimit);
  };

  const paginationHandler = (item: any) => {
    setCurrentPage(item.value);
    props.pageChange && props.pageChange(item.value, currentLimit);
  };
  */
  return (
    <>
      <table className={`divide-primary table w-force-full divide-y`}>
        <thead className="text-left text-sm font-bold leading-5 text-genom-black dark:text-neutral-50">
          <tr>
            {props.columnData.map((item, index) => (
              <th className={`mr-8 whitespace-nowrap p-3 ${item.widthStyle ? item.widthStyle : ''}`} key={index}>
                {item.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-primary divide-y">
          {props.tableData.map(
            (item: any, index: number) =>
               (
                <tr
                  className="text-sm leading-5 text-genom-black hover:bg-genom-bg-gray dark:text-neutral-50 dark:hover:bg-neutral-700"
                  key={index}
                >
                  {props.columnData.map((item1, index1) => (
                    <td className={`mr-8 p-3 ${item1.customStyle ? item1.customStyle : ''}`} key={index1}>
                      {item[item1.columnName]}
                    </td>
                  ))}
                </tr>
              ),
          )}
        </tbody>
      </table>
      <Line offsetTop="mt-0" />
    </>
  );
}
