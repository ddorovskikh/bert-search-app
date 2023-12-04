interface ILineProps {
  offsetTop?: string;
}
export default function Line(props: ILineProps) {
  return (
    <hr
      className={`flex ${
        props.offsetTop ? props.offsetTop : 'mt-5'
      } h-px border-0 bg-genom-light-gray dark:bg-neutral-600`}
    />
  );
}
