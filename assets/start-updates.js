if ((location.protocol === "https:" || location.protocol === "http:") && "serviceWorker" in navigator) {
  navigator.serviceWorker.register("./refresh-worker.js", { updateViaCache: "none" }).catch(() => {
    // Offline file copies and browsers with worker restrictions can use the static guide.
  });
}
