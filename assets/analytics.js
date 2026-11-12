// Public site token from the site's Cloudflare Web Analytics snippet.
(() => {
  const siteToken = "ca2c5af99ac949498dd7b1e7527c4d5f";
  if (!siteToken || location.origin !== "https://juvenile-a3.github.io") return;

  const tracker = document.createElement("script");
  tracker.type = "module";
  tracker.src = "https://static.cloudflareinsights.com/beacon.min.js";
  // Route, story and filter changes all update the hash within a single guide page.
  tracker.dataset.cfBeacon = JSON.stringify({ token: siteToken, spa: false });
  document.head.appendChild(tracker);
})();
