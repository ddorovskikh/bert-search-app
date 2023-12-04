import cn from 'classnames';
import { forwardRef, MouseEventHandler, ReactElement, PropsWithChildren } from 'react';

interface ButtonProps {
  variation?: 'primary' | 'secondary';
  type?: 'submit' | 'button';
  icon?: ReactElement;
  onClick?: MouseEventHandler;
  className?: string;
  disabled?: boolean;
}

const Button = forwardRef<HTMLButtonElement, PropsWithChildren<ButtonProps>>(
  ({ children, icon, variation = 'primary', disabled, type = 'button', ...props }, ref) => {
    return (
      <button
        {...props}
        ref={ref}
        className={cn(
          'border-blue-primary flex flex-1 cursor-pointer justify-center rounded border px-5 py-genom-11 align-baseline text-base leading-6 transition-colors',
          disabled && 'cursor-not-allowed bg-button-active dark:bg-neutral-900-60',
          {
            'bg-blue-primary text-white hover:bg-blue-800 active:bg-blue-900': variation === 'primary',
            'text-blue-primary hover:text-blue-800 active:text-blue-900': variation === 'secondary',
          },
          props.className,
        )}
        type={type}
        disabled={disabled}
      >
        {children}
        {icon}
      </button>
    );
  },
);

export default Button;
