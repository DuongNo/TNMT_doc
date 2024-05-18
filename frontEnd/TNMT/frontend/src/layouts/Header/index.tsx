import logo from "@/assets/VDI-logo.svg";

const Header = () => {
  return (
    <div className="h-20 px-2 lg:px-0 flex items-center border-b-gray-200 border-b">
      <img src={logo} alt="vdi" className="w-20 object-cover" />
    </div>
  );
};

export default Header;
