import { spawn } from 'node:child_process'

const python = spawn(process.platform === 'win32' ? 'python' : 'python3', ['../app.py'], { stdio: 'inherit' })
const vite = spawn(process.execPath, ['node_modules/vite/bin/vite.js'], { stdio: 'inherit' })

let stopping = false

function stop() {
  if (stopping) return
  stopping = true
  python.kill()
  vite.kill()
}

python.on('error', error => console.error(`Could not start Python: ${error.message}`))
python.on('exit', stop)

vite.on('error', error => console.error(`Could not start Vite: ${error.message}`))
vite.on('exit', stop)

process.on('SIGINT', stop)
process.on('SIGTERM', stop)
