import { FocusEvent, forwardRef, KeyboardEvent, MouseEvent } from 'react';
import cn from 'classnames';

export interface TextInputProps {
  onChange?: (newValue: string) => void;
  placeholder?: string;
  value?: string;
  type?: 'text' | 'password';
  errorMessage?: string;
  className?: string;
  name?: string;
  disabled?: boolean;
  onBlur?: (event: FocusEvent<HTMLInputElement>) => void;
  onFocus?: (event: FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (event: KeyboardEvent<HTMLInputElement>) => void;
  onMouseDown?: (event: MouseEvent<HTMLInputElement>) => void;
}
{/*'outline-none flex w-full rounded border-2 px-20 py-3  placeholder:text-genom-gray2'*/}
const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
  ({ errorMessage, className, onChange, type = 'text', name, value, disabled, ...props }, ref) => {
    return (
      <div className="flex w-full flex-col">
        <input
          {...props}
          value={value ?? ''}
          disabled={disabled}
          className={cn(
            'outline-none flex w-full rounded border-2 px-4 py-3  placeholder:text-genom-gray2 text-indent: 20px',
            disabled ? 'bg-gray-200 dark:bg-neutral-950' : 'bg-white dark:bg-neutral-900',
            errorMessage && 'border-genom-rose',
            className,
          )}
          ref={ref}
          type={type}
          onChange={onChange ? (event) => onChange(event.target.value) : undefined}
          name={name}
        />
        {errorMessage && <p className="text-red-600">{errorMessage}</p>}
      </div>
    );
  },
);

export default TextInput;
