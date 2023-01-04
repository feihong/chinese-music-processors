# Top Playlists

Bookmarklet to generate a nicely-formatted line for Notion todo list. Assumes you're on YouTube Music album page.

```
javascript:(function(){
  const title = document.querySelector("h2").innerText;
  const artist = document.querySelector("a[dir=auto]").innerText;
  const html = `${artist}《${title}》<a href="${location.href}">youtube</a>`;
  const div = document.createElement("div");
  div.innerHTML = html;
  document.querySelector('.metadata').appendChild(div);
})();
```

