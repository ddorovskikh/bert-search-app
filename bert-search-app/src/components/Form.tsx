import { forwardRef } from "react";
import type { ChangeEventHandler, ChangeEvent } from 'react';
import { useState, useEffect } from 'react';

import Button from './Button';
import { SearchIcon } from './icons';
import TextInput from './TextInput';

interface ITextInputProps {
  changeHandler?: any;
}
//sendQuery(event.target)
const Form = (props: ITextInputProps) => {
  const [inputValue, setInputValue] = useState('');

  const changeHandler = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.currentTarget.value);
    /*
    if (props.changeHandler) {
      props.changeHandler(e);
    }
    */
  };

  const buttonHandler = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    if (props.changeHandler) {
      props.changeHandler(inputValue);
    }
    //const button: HTMLButtonElement = event.currentTarget;
    //setClickedButton(button.name);
  };
  const searchAction = (input: string | unknown) => {
    if (typeof input !== 'string' || input.length === 0) {
      return;
    }
    setInputValue(input);
    props.changeHandler && props.changeHandler(input);
  }

  /*
  <button onClick={buttonHandler} >
    Найти
  </button>
  */
  /*
  <div className="my-2 flex h-8 w-1/4">
    <div className="flex w-full">
      <textarea onChange={changeHandler}/>
      <div className="mr-6">
        <Button mode="normal" text={'Найти'} clickHandler={buttonHandler} />
      </div>
    </div>
  </div>
  */
  /*
  <TextInput
    placeholder={'Поиск'}
    onChange={(newValue) => setInputValue(newValue)}
    value={inputValue}
  />
  */
  return (
        <div className="mt-6 flex flex-wrap justify-between">
          <div className="flex">
            <div className="mr-6 flex">
              <TextInput
                placeholder={'Поиск'}
                onChange={(newValue) => setInputValue(newValue)}
                value={inputValue}
              />
              <Button
                type="button"
                icon={<SearchIcon />}
                onClick={() => searchAction(inputValue)}
              />
            </div>
          </div>
        </div>

  );
}

export default Form;
