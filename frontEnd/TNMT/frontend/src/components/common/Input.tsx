import { FastFieldProps } from "formik";

interface InputProps extends FastFieldProps {
  type: string;
  placeHolder: string;
}

const Input = ({ type, placeHolder, field }: InputProps) => {
  const { onChange, name, value } = field;
  return (
    // <TextField
    //   id={name}
    //   value={value}
    //   label={placeHolder}
    //   type={type}
    //   autoComplete="current-password"
    //   sx={{
    //     width: "100%",
    //     fontFamily: "'Fredoka', sans-serif",
    //   }}
    //   onChange={onChange}
    // />
    <input
      type={type}
      id={name}
      value={value}
      placeholder={placeHolder}
      onChange={onChange}
      className="
        w-full
        px-4
        py-2
        mb-4
        text-base
        text-gray-700
        placeholder-gray-400
        bg-[#EFF1F9]
        border
        border-gray-300
        rounded-lg
        focus:outline-none
        focus:ring-2
        focus:ring-blue-600
        focus:border-transparent
        dark:bg-gray-700
        dark:text-gray-300
        dark:placeholder-gray-500
        dark:border-gray-600
      "
    />
  );
};

export default Input;
