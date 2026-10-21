# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
# Parallax

## Run locally

Install the Python packages in `requirements.txt`, run `npm install`, then start both servers with:

```sh
npm run dev
```

Open the Vite address it prints. Python handles image processing.

## Run as a website

Build and run the single app container from the repository root:

```sh
docker build -f Front/Dockerfile -t parallax .
docker run --rm -p 8000:8000 parallax
```

The Python server serves the built site and processes `/interlace` uploads. Deploy this container to a host that runs Docker to make it available on the web.
