module.exports = {
  run: [{
    method: "shell.run",
    params: {
      message: "git pull"
    }
  }, {
    // Re-fetch the latest tiny-voca and dizione from GitHub, then the latest weights.
    method: "shell.run",
    params: {
      venv: "env",
      path: "app",
      message: [
        "uv pip install --refresh --reinstall-package tiny-voca --reinstall-package dizione -r requirements.txt",
        "hf download n4ze3m/tiny-voca --include tiny-voca.pt --include \"phonemizer/*\" --local-dir weights"
      ]
    }
  }]
}
