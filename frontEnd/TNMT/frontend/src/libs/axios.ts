import axios from "axios";

export const base = `http://${window.location.hostname}:${import.meta.env.VITE_SERVER_PORT
  }`;
console.log("base url : ", base);
const axiosClient = axios

export default axiosClient;
