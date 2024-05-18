import { useState } from "react";

import UploadFile from "@/components/common/UploadFile";
import { uploadMultipleFile } from "@/libs/api";
import ProcessData from "@/components/common/ProcessData";
import RenderExcelFile from "@/components/common/RenderExcelFile";
import { toast } from "react-toastify";

const HomePage = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [taskId, setTaskId] = useState("");
  const [link, setLink] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // function
  const handleUploadFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;

    if (files) {
      const newFiles = Array.from(files);
      setIsLoading(true);
      const res = await uploadMultipleFile(newFiles);
      setIsLoading(false);
      if (res && res?.task_id) {
        setTaskId(res?.task_id);
        setCurrentStep(2);
      } else {
        toast.error(res || "ERROR !", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "colored",
        });
      }
    }
  };

  const handleSetLink = (link: string) => {
    setLink(link);
    setCurrentStep(3);
  };

  return (
    <div className="mt-10 min-h-full">
      {currentStep === 1 && (
        <UploadFile loading={isLoading} handleUploadFile={handleUploadFile} />
      )}
      {currentStep === 2 && (
        <ProcessData taskId={taskId} setLink={handleSetLink} />
      )}
      {currentStep === 3 && <RenderExcelFile link={link} />}
    </div>
  );
};

export default HomePage;
