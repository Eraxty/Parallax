import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {

  return (
    <div>
      <Upload_button/>
      <View_button/>
    </div>
  )}


function Upload_button() {

  function onuploadclick(){
    document.getElementById("fileInput").click()
    alert("uploaded")
}

  return(
    <div>
      <input 
      id = "fileInput"
      type = "file" 
      style = {{ display: "none" }}
      />

      <button onClick = {onuploadclick}>
        Upload
      </button>
    </div>
  )
}

function View_button() {

  function onviewclick(){
  alert("view")
}

  return(
    <button onClick = {onviewclick}>
      View
    </button>
  )
}

export default App
