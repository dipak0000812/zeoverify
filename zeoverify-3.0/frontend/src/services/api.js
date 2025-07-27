import axios from "axios";

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post("http://localhost:5000/upload", formData); // Flask/Node backend
};
