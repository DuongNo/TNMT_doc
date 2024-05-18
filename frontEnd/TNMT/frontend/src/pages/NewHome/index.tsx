import { useState, useRef } from "react";
import { Formik, FastField, Form } from "formik";

import { Input, UploadLabel } from "@/components";
import axios from "axios";
import LoadingOverlay from "./LoadingOverlay";
import { toast } from "react-toastify";

// const SERVER_PORT = import.meta.env.VITE_SERVER_PORT || 18556;

type ResponseType = {
  donvichucchi: string;
  macongviec: string;
  noidungcongviec: string;
  phoihop: string;
  phutrach: string;
  sanpham: string;
  thuchien: string;
  content?: string;
  tomtat?: string;
  download_url?: string;
  message?: string;
};

const NewHome = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ResponseType | null>(null);
  const [mode, setMode] = useState("plvb");

  const fileInputRef = useRef<any>(null);

  // state
  const [files, setFiles] = useState<File[]>([]);
  const hostname = window.location.hostname;
  console.log("-----------hostname : ", hostname);

  const serverUrl =
    hostname.includes("127.0.0.1") ||
    hostname.includes("localhost") ||
    hostname.includes("172.16.50.201")
      ? `http://172.16.50.201:18556`
      : `http://113.20.109.148:2602`;

  // functions
  const handChangeFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      for (let i = 0; i < e.target.files.length; i++) {
        const file = e.target.files[i];
        setFiles((prevFiles: File[]) => [...prevFiles, file]);
      }
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (trick_yeu: string, so_ki_hieu: string) => {
    setLoading(true);
    setResponse(null);

    const formData = new FormData();
    formData.append("trichyeu", trick_yeu);
    formData.append("sokyhieu", so_ki_hieu);
    formData.append("OCR", mode === "ocr" ? "1" : "0");
    formData.append("PLVB", mode === "plvb" ? "1" : "0");
    formData.append("SUMMARY", mode === "summary" ? "1" : "0");
    if (files) {
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }
    }
    const headers = {
      accept: "application/json",
      "Content-Type": "multipart/form-data",
    };

    try {
      const res = await axios.post(`${serverUrl}/process`, formData, {
        headers: {
          ...headers,
        },
      });

      if (res.status === 200) {
        if (res.data.result === "0") {
          setResponse(res.data);
          setFiles([]);
        }
      }
    } catch (error: any) {
      console.log(error);
      toast.error(error.toString());
    } finally {
      setLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };
  // function downloadPdfFromBase64(base64: string, filename = "file.pdf") {
  //   // Decode base64 string
  //   const binaryString = window.atob(base64);

  //   // Create binary array
  //   const len = binaryString.length;
  //   const binaryArray = new Uint8Array(len);
  //   for (let i = 0; i < len; i++) {
  //     binaryArray[i] = binaryString.charCodeAt(i);
  //   }

  //   // Create blob object
  //   const blob = new Blob([binaryArray], { type: "application/pdf" });

  //   // Create link element and click it to download the file
  //   const link = document.createElement("a");
  //   link.href = window.URL.createObjectURL(blob);
  //   link.download = filename;
  //   link.click();
  // }
  function openPdfInNewTabFromBase64(base64: string) {
    // Decode base64 string
    const binaryString = window.atob(base64);

    // Create binary array
    const len = binaryString.length;
    const binaryArray = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      binaryArray[i] = binaryString.charCodeAt(i);
    }

    // Create blob object
    const blob = new Blob([binaryArray], { type: "application/pdf" });

    // Create link element and click it to open the file in a new tab
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.target = "_blank"; // Open in a new tab
    const width = 1024;
    const height = 768;
    // link.params = `width=${width},height=${height},right=0,top=0`;
    // link.click();
    // Open a new window and set its dimensions
    const newWindow = window.open(
      link.href,
      "_blank",
      `width=${width},height=${height},right=0,top=0`
    );

    // Check if the new window is opened
    if (newWindow) {
      // Focus the new window
      newWindow.focus();
    } else {
      // Handle the case where the new window couldn't be opened
      console.error("Failed to open a new window");
    }
  }

  return (
    <div className="flex flex-wrap">
      <div
        className={`mt-2 my-2 w-1/4 relative items-center ${
          loading ? "bg-white opacity-50" : ""
        }`}
      >
        <h1 className="text-xl font-medium">Điền thông tin và upload file</h1>
        <div className=" mx-auto mt-2">
          <Formik
            initialValues={{
              trick_yeu: "",
              so_ki_hieu: "",
            }}
            onSubmit={(values: any) => {
              handleSubmit(values?.trick_yeu, values?.so_ki_hieu);
            }}
            enableReinitialize
          >
            {() => (
              <Form>
                <label htmlFor="trick_yeu">Trích yếu</label>
                <FastField
                  name="trick_yeu"
                  component={Input}
                  type="text"
                  placeHolder="Trích yếu"
                />
                <label htmlFor="so_ki_hieu">Số ký hiệu</label>
                <FastField
                  name="so_ki_hieu"
                  component={Input}
                  type="text"
                  placeHolder="Số kí hiệu"
                />
                {files && files.length > 0 ? (
                  <div className="my-2 ">
                    {Array.from(files).map((file, i) => (
                      <div
                        className="flex justify-between my-2"
                        key={`file-${i}`}
                      >
                        <div
                          onClick={() => {
                            const file = files[i];
                            const url = URL.createObjectURL(file);
                            const link = document.createElement("a");
                            link.href = url;
                            link.download = file.name;
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                          }}
                          className="text-blue-400 cursor-pointer "
                        >
                          {file.name}
                        </div>
                        <div
                          onClick={() => {
                            setFiles(files.filter((_, id) => id !== i));
                          }}
                          className="cursor-pointer hover:text-red-400"
                        >
                          xóa
                        </div>
                      </div>
                    ))}
                  </div>
                ) : null}

                <UploadLabel onChange={handChangeFiles} ref={fileInputRef} />

                <div className="flex items-center justify-between">
                  <div className="flex items-center cursor-pointer">
                    <input
                      id="ocr-radio"
                      type="radio"
                      value="ocr"
                      name="list-radio"
                      className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2 focus:border-none focus:outline-none"
                      checked={mode === "ocr"}
                      onChange={(e) => {
                        setMode(e.target.value);
                      }}
                    />
                    <label
                      htmlFor="ocr-radio"
                      className="w-full py-3 ms-2 text-sm font-medium text-gray-900"
                    >
                      OCR
                    </label>
                  </div>
                  <div className="flex items-center cursor-pointer">
                    <input
                      id="plvb-radio"
                      type="radio"
                      value="plvb"
                      checked={mode === "plvb"}
                      name="list-radio"
                      className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2 focus:border-none focus:outline-none"
                      onChange={(e) => {
                        setMode(e.target.value);
                      }}
                    />
                    <label
                      htmlFor="plvb-radio"
                      className="w-full py-3 ms-2 text-sm font-medium text-gray-900"
                    >
                      PLVB
                    </label>
                  </div>
                  <div className="flex items-center cursor-pointer">
                    <input
                      id="summary-radio"
                      type="radio"
                      value="summary"
                      name="list-radio"
                      checked={mode === "summary"}
                      className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2 focus:border-none focus:outline-none"
                      onChange={(e) => {
                        setMode(e.target.value);
                      }}
                    />
                    <label
                      htmlFor="summary-radio"
                      className="w-full py-3 ms-2 text-sm font-medium text-gray-900"
                    >
                      SUMMARY
                    </label>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="
                    border-none
                    outline-none
                    focus:outline-none
                    bg-[#143066]
                    hover:bg-[#112855]
                    rounded-lg
                    text-white
                    py-2
                    px-4
                    mt-4
                    w-full
                    transition-all
                    delay-75
                "
                >
                  {loading ? `Loading...` : `Submit`}
                </button>
              </Form>
            )}
          </Formik>
        </div>
      </div>
      <div className="mt-2 pl-5 w-3/4">
        {response?.content ? (
          <div className="mb-2">
            <label
              htmlFor="file download"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              PDF file
            </label>
            <div
              onClick={() => {
                // downloadPdfFromBase64(response?.content as string, "file.pdf");
                openPdfInNewTabFromBase64(response?.content as string);
              }}
              className="text-blue-500 cursor-pointer"
            >
              {`file_${response?.donvichucchi}.pdf`}
            </div>
          </div>
        ) : null}
        <div className="mb-2">
          <label
            htmlFor="first_name"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Đơn vị chủ trì
          </label>
          <input
            type="text"
            id="first_name"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
            value={response?.donvichucchi}
          />
        </div>
        <div className="mb-2">
          <label
            htmlFor="last_name"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Mã công việc
          </label>
          <input
            type="text"
            id="last_name"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            defaultValue={response?.macongviec}
          />
        </div>
        <div className="mb-2">
          <label
            htmlFor="company"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Nội dung công việc
          </label>
          <input
            type="text"
            id="company"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
            defaultValue={response?.noidungcongviec}
          />
        </div>
        <div className="mb-2">
          <label
            htmlFor="phone"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Phối hợp
          </label>
          <input
            type="tel"
            id="phone"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
            defaultValue={response?.phoihop}
          />
        </div>
        <div className="mb-2">
          <label
            htmlFor="phone"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Phụ trách
          </label>
          <input
            type="tel"
            id="phone"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
            defaultValue={response?.phutrach}
          />
        </div>
        <div className="mb-2">
          <label
            htmlFor="website"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Sản phẩm
          </label>
          <input
            type="url"
            id="website"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            defaultValue={response?.sanpham}
          />
        </div>
        <div className="mb-2">
          <label
            htmlFor="visitors"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Thực hiện
          </label>
          <input
            id="visitors"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            defaultValue={response?.thuchien}
            required
          />
        </div>
        <div className="">
          <label
            htmlFor="visitors"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Tóm tắt
          </label>
          <textarea
            id="tomtat_vanban"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            defaultValue={response?.tomtat}
          />
        </div>
        <div className="">
          <label
            htmlFor="visitors"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Result
          </label>
          <textarea
            id="message"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            defaultValue={response?.message}
          />
        </div>
        {response?.download_url && (
          <div className="mt-6">
            <a href={response?.download_url} className="underline">
              Down Load Summary
            </a>
          </div>
        )}
      </div>
      <LoadingOverlay isLoading={loading} />
    </div>
  );
};

export default NewHome;
