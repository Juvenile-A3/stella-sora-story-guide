// Pages serves HTML with a ten-minute freshness window. Revalidate site files
// on normal visits, using the browser's ETag cache for unchanged responses.
self.addEventListener("install", event => event.waitUntil(self.skipWaiting()));
self.addEventListener("activate", event => event.waitUntil(self.clients.claim()));
self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET" || !request.url.startsWith(self.registration.scope)) return;
  // Media has a content-versioned URL. Leave native byte-range streaming alone.
  if (request.headers.has("Range") || request.destination === "video" || request.destination === "audio") return;
  if (request.cache === "only-if-cached") return;
  event.respondWith(fetch(request, { cache: "no-cache" }).catch(() =>
    fetch(request, { cache: "force-cache" })
  ));
});
