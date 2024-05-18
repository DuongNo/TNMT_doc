import { Header, Footer } from "@/layouts";

interface DefaultLayoutProps {
  children: React.ReactNode;
}

const DefaultLayout = ({ children }: DefaultLayoutProps) => {
  return (
    <div className="max-w-[1200px] mx-auto flex flex-col h-screen">
      <Header />
      <div className="flex-1 pt-20">{children}</div>
      <Footer />
    </div>
  );
};

export default DefaultLayout;
