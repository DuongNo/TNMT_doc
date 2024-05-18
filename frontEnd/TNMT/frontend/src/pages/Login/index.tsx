// import { Formik, Form, FastField } from "formik";
// import Button from "@mui/material/Button";

// import { Input } from "@/components";

const LoginPage = () => {
  return (
    <div className="flex justify-center items-center min-h-screen bg-[#edf1f4]">
      {/* <Formik
        enableReinitialize
        initialValues={{ username: "", password: "" }}
        onSubmit={() => {
          console.log("form");
        }}
      >
        {(formikProps) => {
          return (
            <div className="login">
              <Form>
                <h2>
                  Hello! <br />
                  <span>Welcome back!</span>
                </h2>
                <div className="inputBox mb-9">
                  <FastField
                    name="username"
                    component={Input}
                    type="text"
                    placeHolder="Username *"
                  />
                </div>
                <div className="inputBox mb-5">
                  <FastField
                    name="password"
                    component={Input}
                    type="text"
                    placeHolder="Password *"
                  />
                </div>
                <label className="mb-5">
                  <input type="checkbox" />
                  Keep me logged in
                </label>
                <div className="inputBox text-center">
                  <Button
                    type="submit"
                    variant="contained"
                    color="secondary"
                    sx={{
                      width: "100%",
                    }}
                  >
                    Login
                  </Button>
                </div>
              </Form>
              <h4 className="uppercase font-medium">or</h4>
            </div>
          );
        }}
      </Formik> */}
    </div>
  );
};

export default LoginPage;
