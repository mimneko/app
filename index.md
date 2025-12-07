---
title: リンク集
---

<div class="folder-tree">
  <ul id="file-list"></ul>
</div>

<script>
const owner  = 'mimneko';
const repo   = 'app';
const branch = 'main';

// ルート直下のみ除外
const rootExcludeNames = [
  'README.md',
  'index.html',
  'index.md',
  'script.js',
  '_config.yml'
];

async function getFiles(path = '') {
  const url = `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
  const response = await fetch(url);
  return await response.json();
}

function createFileLink(file) {
  const a = document.createElement('a');
  if (file.name.endsWith('.md')) {
    const htmlName = file.name.replace(/\.md$/, '.html');
    a.href = `https://${owner}.github.io/${repo}/${file.path.replace(file.name, htmlName)}`;
  } else if (file.name.endsWith('.html')) {
    a.href = `https://${owner}.github.io/${repo}/${file.path}`;
  }
  a.textContent = file.name;
  a.target = '_blank';
  return a;
}

/**
 * 再帰的にフォルダを処理し、
 * 表示可能な子要素がある場合のみ DOM に追加する。
 */
async function displayFiles(parentElement, path = '', isRoot = false) {
  const files = await getFiles(path);

  files.sort((a, b) => {
    if (a.type === b.type) return a.name.localeCompare(b.name, 'ja');
    return a.type === 'dir' ? -1 : 1;
  });

  let hasVisibleChild = false;

  for (const file of files) {
    if (isRoot && rootExcludeNames.includes(file.name)) continue;

    if (file.type === 'dir') {
      const li = document.createElement('li');
      const details = document.createElement('details');
      details.open = true;

      const summary = document.createElement('summary');
      summary.textContent = file.name;

      const ul = document.createElement('ul');

      details.appendChild(summary);
      details.appendChild(ul);
      li.appendChild(details);

      const childVisible = await displayFiles(ul, file.path, false);

      if (childVisible) {
        parentElement.appendChild(li);
        hasVisibleChild = true;
      }

    } else if (file.type === 'file') {
      if (!file.name.endsWith('.md') && !file.name.endsWith('.html')) continue;

      const li = document.createElement('li');
      li.appendChild(createFileLink(file));
      parentElement.appendChild(li);

      hasVisibleChild = true;
    }
  }

  return hasVisibleChild;
}

(async () => {
  const rootUL = document.getElementById('file-list');
  await displayFiles(rootUL, '', true);
})();
</script>