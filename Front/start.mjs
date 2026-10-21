import { spawn } from 'node:child_process'
import { get } from 'node:http'

const python = spawn(
  process.platform === 'win32' ? 'python' : 'python3',
  ['server.py'],
  { stdio: 'inherit' },
)

let vite
let stopping = false

function stop() {
  if (stopping) return
  stopping = true
  python.kill()
  vite?.kill()
}

function waitForPython() {
  return new Promise((resolve, reject) => {
    let tries = 0

    function check() {
      if (stopping) return reject(new Error('Python server stopped.'))

      const request = get('http://127.0.0.1:8000/health', response => {
        response.resume()
        if (response.statusCode === 200) {
          resolve()
        } else {
          retry()
        }
      })

      request.on('error', retry)

      function retry() {
        tries += 1
        if (tries === 100) {
          reject(new Error('Python server did not start on port 8000.'))
        } else {
          setTimeout(check, 100)
        }
      }
    }

    check()
  })
}

python.on('error', error => console.error(`Could not start Python: ${error.message}`))
python.on('exit', code => {
  if (!stopping) console.error(`Python server stopped (${code}).`)
  stop()
})

try {
  await waitForPython()
  if (!stopping) {
    vite = spawn(process.execPath, ['node_modules/vite/bin/vite.js'], { stdio: 'inherit' })
    vite.on('error', error => console.error(`Could not start Vite: ${error.message}`))
    vite.on('exit', stop)
  }
} catch (error) {
  console.error(error.message)
  stop()
}

process.on('SIGINT', stop)
process.on('SIGTERM', stop)
