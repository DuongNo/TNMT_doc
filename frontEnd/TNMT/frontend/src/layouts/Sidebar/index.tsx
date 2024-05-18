import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import HomeIcon from "@mui/icons-material/Home";
import InfoIcon from "@mui/icons-material/Info";
import ForumIcon from "@mui/icons-material/Forum";
import CropOriginalIcon from "@mui/icons-material/CropOriginal";
import SettingsIcon from "@mui/icons-material/Settings";

const Sidebar = () => {
  const location = useLocation();

  const [openMenu, setOpenMenu] = useState(false);
  return (
    <div className={`navigation ${openMenu ? "open" : ""}`}>
      <div
        className="menuToggle"
        onClick={() => setOpenMenu((prev) => !prev)}
      ></div>
      <ul>
        <li className={`list ${location.pathname === "/home" ? "active" : ""}`}>
          <Link to="/home">
            <span className="icon">
              <HomeIcon sx={{ color: "#ffffff" }} />
            </span>
            <span className="text">Home</span>
          </Link>
        </li>
        <li
          className={`list ${location.pathname === "/about" ? "active" : ""}`}
        >
          <Link to="/about">
            <span className="icon">
              <InfoIcon sx={{ color: "#ffffff" }} />
            </span>
            <span className="text">About</span>
          </Link>
        </li>
        <li
          className={`list ${location.pathname === "/message" ? "active" : ""}`}
        >
          <Link to="/message">
            <span className="icon">
              <ForumIcon sx={{ color: "#ffffff" }} />
            </span>
            <span className="text">Message</span>
          </Link>
        </li>
        <li
          className={`list ${location.pathname === "/photos" ? "active" : ""}`}
        >
          <Link to="/photos">
            <span className="icon">
              <CropOriginalIcon sx={{ color: "#ffffff" }} />
            </span>
            <span className="text">Photos</span>
          </Link>
        </li>
        <li
          className={`list ${location.pathname === "/setting" ? "active" : ""}`}
        >
          <Link to="/setting">
            <span className="icon">
              <SettingsIcon sx={{ color: "#ffffff" }} />
            </span>
            <span className="text">Setting</span>
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
