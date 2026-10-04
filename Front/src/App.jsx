import './App.css'

function App() {
  return (
    <main className = "landing-page">
      <section className = "hero-section" aria-labelledby = "page-title">
        <div className = "hero-copy">
          <p className = "eyebrow">PARALLAX</p>
          <h1 id = "page-title">Your images,<br /><em>in motion.</em></h1>
          <p className = "intro">Upload an image to get started.</p>
        </div>
        <div className = "action-panel">
          <UploadButton />
          <ViewButton />
        </div>
      </section>
    </main>
  )
}

function UploadButton() {
  function onUploadClick() {
    document.getElementById('fileInput').click()
  }

  function onFileChange(event) {
    const file = event.target.files[0]

    if (file) {
      const reader = new FileReader()

      reader.onload = function () {
        localStorage.setItem('image', reader.result)
        window.location.href = '/view.html'
      }

      reader.readAsDataURL(file)
    }
  }

  return (
    <>
      <input id = "fileInput" type = "file" accept = "image/*" hidden onChange = { onFileChange } />
      <button className = "action-button primary-action" onClick = { onUploadClick }>
        <span>Upload image</span>
      </button>
    </>
  )
}

function ViewButton() {
  function onViewClick() {
    const image = localStorage.getItem('image')

    if (image) {
      window.open(image, '_blank')
    }
    else {
      alert('No image uploaded')
    }
  }

  return (
    <button className = "action-button secondary-action" onClick = { onViewClick }>
      <span>View current image</span>
    </button>
  )
}

export default App
