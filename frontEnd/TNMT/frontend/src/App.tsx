import { BrowserRouter as UseRouter, Route, Routes } from "react-router-dom";
import { publicRoutes } from "@/routes";
import { ToastContainer } from "react-toastify";

import { ThemeProvider, createTheme } from "@mui/material/styles";

import "react-toastify/dist/ReactToastify.css";

const defaultTheme = createTheme({
  typography: {
    fontFamily: ["Fredoka", "sans-serif"].join(","),
  },
});

function App() {
  return (
    <ThemeProvider theme={defaultTheme}>
      <UseRouter>
        <div>
          <Routes>
            {publicRoutes.map((route) => {
              const Page = route.page;
              const Layout = route.layout;
              return (
                <Route
                  key={`router-${route.id}`}
                  path={route.path}
                  element={
                    <Layout>
                      <Page />
                    </Layout>
                  }
                />
              );
            })}
          </Routes>
          <ToastContainer
            style={{
              fontSize: "14px",
              fontFamily: "Fredoka, sans-serif",
            }}
          />
        </div>
      </UseRouter>
    </ThemeProvider>
  );
}

export default App;
