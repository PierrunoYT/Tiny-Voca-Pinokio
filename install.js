module.exports = {
  requires: {
    bundle: "ai"
  },
  run: [
    // tiny-voca is a 4.5M-parameter model that runs ~70x real time on CPU,
    // so the CPU build of torch is installed instead of a multi-GB CUDA build.
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "{{platform === 'darwin' ? 'uv pip install torch' : 'uv pip install torch --index-url https://download.pytorch.org/whl/cpu'}}",
          "uv pip install -r requirements.txt"
        ]
      }
    },
    // Only the PyTorch checkpoint and the phonemizer data are needed (skips the ONNX/GGUF/sample files).
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "hf download n4ze3m/tiny-voca --include tiny-voca.pt --include \"phonemizer/*\" --local-dir weights"
        ]
      }
    }
  ]
}
