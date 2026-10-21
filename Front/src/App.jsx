import { useState } from 'react'
import './App.css'

function App() {
  const [lpi, setLpi] = useState(60)
  const [dpi, setDpi] = useState(600)
  const [slant, setSlant] = useState(8)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  async function createImage(event) {
    event.preventDefault()

    const form = new FormData(event.currentTarget)
    const images = form.getAll('images').filter((image) => image.size > 0)

    if (images.length < 2) {
      setMessage('Choose at least two images.')
      return
    }

    setBusy(true)
    setMessage('')

    try {
      const response = await fetch('/interlace', {
        method: 'POST',
        body: form,
      })

      if (!response.ok) {
        const reason = (await response.text()).trim()
        throw new Error(reason || `Request failed (${response.status}).`)
      }

      const image = await response.blob()
      const url = URL.createObjectURL(image)
      const link = document.createElement('a')
      link.href = url
      link.download = 'interlaced.png'
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
      setMessage('Downloaded interlaced.png')
    } catch (error) {
      if (error instanceof TypeError) {
        setMessage('Could not reach Python. Check the terminal running the app.')
      } else {
        setMessage(error.message)
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="page">
      <header>
        <a className="wordmark" href="/">Parallax</a>
      </header>

      <form onSubmit={createImage}>
        <h1>Interlace images</h1>

        <label className="file-field">
          <span>Images</span>
          <input name="images" type="file" accept="image/*" multiple />
          <small>Choose two or more images</small>
        </label>

        <label className="slider-field">
          <span>LPI <output>{lpi}</output></span>
          <input
            name="lpi"
            type="range"
            min="20"
            max="160"
            value={lpi}
            onChange={(event) => setLpi(Number(event.target.value))}
          />
        </label>

        <label className="slider-field">
          <span>DPI <output>{dpi}</output></span>
          <input
            name="dpi"
            type="range"
            min="150"
            max="1200"
            step="10"
            value={dpi}
            onChange={(event) => setDpi(Number(event.target.value))}
          />
        </label>

        <label className="slider-field">
          <span>Slant <output>{slant}°</output></span>
          <input
            name="slant"
            type="range"
            min="-20"
            max="20"
            value={slant}
            onChange={(event) => setSlant(Number(event.target.value))}
          />
        </label>

        <button type="submit" disabled={busy}>
          {busy ? 'Working…' : 'Create image'}
        </button>
        <p className="message" role="status">{message}</p>
      </form>
    </main>
  )
}

export default App
