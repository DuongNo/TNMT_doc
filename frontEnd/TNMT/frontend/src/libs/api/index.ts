import axiosClient from "../axios";
import axios, { AxiosError } from "axios";

type ResponseErrorAxios = {
  detail: string;
};
function isAxiosError<ResponseType>(
  error: unknown
): error is AxiosError<ResponseType> {
  return axios.isAxiosError(error);
}
export const uploadMultipleFile = async (files: File[]) => {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }

  try {
    const res = await axiosClient.post(`/upload/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (error: unknown) {
    if (isAxiosError<ResponseErrorAxios>(error)) {
      // "thisIsANumber" is properly typed here:
      console.log(error.response?.data.detail);
      return error.response?.data.detail || "an error has occurred !";
    }
  }
};

export const callRunTask = async (taskId: string) => {
  try {
    const res = await axiosClient.get(`/task-status/${taskId}`);
    return res.data;
  } catch (error) {
    console.warn(error);
    return undefined;
  }
};
