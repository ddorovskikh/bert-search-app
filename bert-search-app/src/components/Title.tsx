import { ReactNode } from 'react';

interface ITitleProps {
  title: ReactNode;
  size: 'middle' | 'large';
  topOffset?: string;
  rigthOffset?: string;
  titleColor?: string;
  isClickable?: boolean;
}

export default function Title(props: ITitleProps) {
  return (
    <div
      className={`flex font-bold ${props.topOffset ? props.topOffset : ''} ${
        props.rigthOffset ? props.rigthOffset : ''
      } ${props.size === 'large' ? 'text-3xl text-genom-gray dark:text-neutral-50' : ''} ${
        props.size === 'middle'
          ? 'text-xl ' + (props.titleColor ? props.titleColor : 'text-genom-black dark:text-neutral-50')
          : ''
      } ${props.isClickable && 'cursor-pointer'} `}
    >
      {props.title}
    </div>
  );
}
