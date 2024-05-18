import React from "react";

interface LoginLayoutProps {
  children: React.ReactNode;
}

const LoginLayout = ({ children }: LoginLayoutProps) => {
  return <div>{children}</div>;
};

export default LoginLayout;
