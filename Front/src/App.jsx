import { useEffect, useRef, useState } from 'react'
import './App.css'

const wasmPath = 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.1.1/wasm'
const faceModel = 'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task'

function App() {
  const [mode, setMode] = useState('interlace')
  const [lpi, setLpi] = useState(60)
  const [dpi, setDpi] = useState(600)
  const [slant, setSlant] = useState(8)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  const [image, setImage] = useState(null)
  const [tracking, setTracking] = useState(false)
  const [movement, setMovement] = useState(1)
  const [previewMessage, setPreviewMessage] = useState('')

  const preview = useRef(null)
  const camera = useRef(null)
  const view = useRef(0)
  const movementRef = useRef(movement)

  movementRef.current = movement

  function showView(amount) {
    view.current = amount
    if (!preview.current) return

    const frame = Math.max(0, Math.min(8, Math.round(4 + amount)))
    preview.current.style.backgroundPositionX = `${frame * 12.5}%`
  }

  useEffect(() => {
    if (!image) return

    let stopped = false
    let imageUrl

    async function makePreview() {
      try {
        const form = new FormData()
    
        form.append('image', image)
    
        const response = await fetch('/depth-preview', { method: 'POST', body: form })
    
        if (!response.ok) throw new Error('Image processing failed.')

        const sheet = await response.blob()
    
        imageUrl = URL.createObjectURL(sheet)
    
        const size = await createImageBitmap(sheet)

        if (!stopped && preview.current) {
          preview.current.style.backgroundImage = `url(${imageUrl})`
          preview.current.style.backgroundSize = '900% 100%'
          preview.current.style.aspectRatio = `${size.width / 9} / ${size.height}`
          showView(view.current)
          setPreviewMessage('')
        }

        size.close()
      } catch {
        if (!stopped) setPreviewMessage('Image processing failed.')
      }
    }

    makePreview()
    return () => {
      stopped = true
      if (imageUrl) URL.revokeObjectURL(imageUrl)
    }
  }, [image])

  useEffect(() => {
    if (!tracking) return

    let stopped = false
    let stream
    let tracker
    let frame

    async function startCamera() {
      try {
        const { FaceLandmarker, FilesetResolver } = await import('@mediapipe/tasks-vision')
        const files = await FilesetResolver.forVisionTasks(wasmPath)
        tracker = await FaceLandmarker.createFromOptions(files, {
          baseOptions: { modelAssetPath: faceModel },
          runningMode: 'VIDEO',
          numFaces: 1,
        })

        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user' },
          audio: false,
        })

        if (stopped) {
          stream.getTracks().forEach((track) => track.stop())
          return
        }

        camera.current.srcObject = stream
        await camera.current.play()

        let lastTime = -1
        function followFace() {
          if (stopped) return

          if (camera.current.currentTime !== lastTime && camera.current.readyState >= 2) {
            lastTime = camera.current.currentTime
            const faces = tracker.detectForVideo(camera.current, performance.now()).faceLandmarks
            if (faces.length) {
              showView((0.5 - faces[0][1].x) * movementRef.current * 4)
            }
          }

          frame = requestAnimationFrame(followFace)
        }

        followFace()
      } catch {
        if (!stopped) setPreviewMessage('Camera unavailable.')
      }
    }

    startCamera()
    return () => {
      stopped = true
      cancelAnimationFrame(frame)
      stream?.getTracks().forEach((track) => track.stop())
      tracker?.close()
    }
  }, [tracking])

  async function makeInterlace(event) {
    event.preventDefault()

    const form = new FormData(event.currentTarget)
    const images = form.getAll('images').filter((file) => file.size)
    if (images.length < 2) {
      setMessage('Choose at least two images.')
      return
    }

    setBusy(true)
    setMessage('')

    try {
      const response = await fetch('/interlace', { method: 'POST', body: form })
      if (!response.ok) throw new Error(`Request failed (${response.status}).`)

      const url = URL.createObjectURL(await response.blob())
      const link = document.createElement('a')
      link.href = url
      link.download = 'interlaced.png'
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
      setMessage('Downloaded interlaced.png')
    } catch (error) {
      if (error instanceof TypeError) {
        setMessage('Could not reach Python. Check the server.')
      } else {
        setMessage(error.message)
      }
    } finally {
      setBusy(false)
    }
  }

  function movePreview(event) {
    if (tracking) return

    const box = event.currentTarget.getBoundingClientRect()
    const across = (event.clientX - box.left) / box.width
    showView((0.5 - across) * movement * 4)
  }

  function showInterlace() {
    setTracking(false)
    setMode('interlace')
  }

  return (
    <main className="page">
      <header>
        <a className="wordmark" href="/">Parallax</a>
      </header>

      <nav className="tabs" aria-label="Tool">
        <button className={mode === 'interlace' ? 'active' : ''} onClick={showInterlace}>
          Interlace
        </button>
        <button className={mode === 'depth' ? 'active' : ''} onClick={() => setMode('depth')}>
          Depth
        </button>
      </nav>

      <form onSubmit={makeInterlace} hidden={mode !== 'interlace'}>
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

      <section className="depth-tool" hidden={mode !== 'depth'}>
        <h1>Depth preview</h1>
        <div
          className="preview"
          ref={preview}
          onPointerMove={movePreview}
          onPointerLeave={() => showView(0)}
        />
        <video ref={camera} className="camera" playsInline muted />
        {previewMessage && <p className="camera-message">{previewMessage}</p>}
        {!image && <p className="camera-message">Choose an image.</p>}

        <label className="file-field">
          <span>Image</span>
          <input
            type="file"
            accept="image/*"
            onChange={(event) => setImage(event.target.files[0] || null)}
          />
        </label>

        <label className="slider-field">
          <span>Movement <output>{movement.toFixed(1)}×</output></span>
          <input
            type="range"
            min="0.2"
            max="2"
            step="0.1"
            value={movement}
            onChange={(event) => setMovement(Number(event.target.value))}
          />
        </label>

        <button disabled={!image} onClick={() => setTracking(!tracking)}>
          {tracking ? 'Stop tracking' : 'Track my head'}
        </button>
      </section>
    </main>
  )
}

export default App
