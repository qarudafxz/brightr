import React, { useState } from "react";
import { IoIosImages } from "react-icons/io";

function App() {
 const [images, setImages] = useState<File[]>([]);
 const [brightenedImages, setBrightenedImages] = useState<string[]>([]);

 const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  if (e.target.files) {
   const filesArray = Array.from(e.target.files);
   setImages(filesArray);
  }
 };

 const handleSubmit = async (e: React.MouseEvent) => {
  e.preventDefault();
  try {
   const formData = new FormData();
   images.forEach((image) => {
    formData.append("images", image);
   });

   const res = await fetch("http://127.0.0.1:5000/api/adjust_brightness", {
    method: "POST",
    body: formData,
   });

   const data = await res.json();
   setBrightenedImages(data[0]);
  } catch (err) {
   console.log(err);
  }
 };

 return (
  <div className="h-full py-4 font-main grid justify-center place-content-center place-items-center items-center">
   <label className="custom-file-input bg-white border border-gray-300 rounded-lg p-14 cursor-pointer flex flex-col place-items-center">
    <input
     type="file"
     onChange={handleFileChange}
     multiple
     className="hidden"
    />
    <IoIosImages className="text-6xl text-center" />
    <span className="text-center mt-4 text-zinc-500">Upload images</span>
   </label>
   <button
    className="font-bold text-sm text-center py-2 rounded-md bg-blue-600 px-4 text-white mt-4"
    onClick={(e) => handleSubmit(e)}
   >
    Adjust Brightness
   </button>
   <div className="grid grid-cols-3 gap-4 mt-4">
    {images.map((image) => (
     <img
      key={image.name}
      src={URL.createObjectURL(image)}
      alt="preview"
      className="w-32 h-32 object-cover"
     />
    ))}
   </div>

   {brightenedImages.length !== 0 && (
    <div className="border border-zinc-400 p-4 rounded-md mt-4">
     <h1 className="font-bold text-4xl text-center my-3">Brightened Images</h1>

     <div className="grid grid-cols-3 gap-4">
      {brightenedImages.map((image, idx) => (
       <img
        key={idx}
        alt="preview"
        className="w-32 h-32 object-cover"
        src={`data:image/jpeg;base64,${image}`}
       />
      ))}
     </div>
    </div>
   )}
  </div>
 );
}

export default App;
