import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {

  return (
    <div>
      <Upload_button />
      <View_button />
    </div>
  )
}


function Upload_button() {

  function onuploadclick(){
    document.getElementById("fileInput").click()
  }

  function onFileChange(event){
    const file = event.target.files[0]

    if (file) {
      const reader = new FileReader()

      reader.onload = function() {
        localStorage.setItem("image", reader.result)
        window.location.href = "/view.html"
      }

      reader.readAsDataURL(file)
    }
  }

  return(
    <div>
      <input
        id="fileInput"
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={onFileChange}
      />

      <button onClick={onuploadclick}>
        Upload
      </button>
    </div>
  )
}

function View_button() {

  function onviewclick(){
    const image = localStorage.getItem("image")

    if (image) {
      window.open(image, "_blank")
    }
    else {
      alert("No image uploaded")
    }
  }

  return(
    <button onClick={onviewclick}>
      View
    </button>
  )
}

export default App
