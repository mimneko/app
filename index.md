---
title: リンク集
---

<div class="folder-tree">
  <ul id="file-list"></ul>
</div>

<script>
const owner = 'mimneko';
const repo = 'app';
const branch = 'main';

async function getFiles(path = '') {
    const url = `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

function createFileLink(file) {
    const a = document.createElement('a');
    if (file.name.endsWith('.md')) {
        // .mdファイルは.html形式に変換してリンク
        const htmlName = file.name.replace(/\.md$/, '.html');
        a.href = `https://${owner}.github.io/${repo}/${file.path.replace(file.name, htmlName)}`;
    } else if (file.name.endsWith('.html')) {
        // それ以外は通常のリンク
        a.href = `https://${owner}.github.io/${repo}/${file.path}`;
    }
    a.textContent = file.name;
    a.target = '_blank';
    return a;
}

async function displayFiles(parentElement, path = '') {
    const files = await getFiles(path);
    for (const file of files) {
        if (['README.md', 'index.html', 'index.md', 'script.js', '_config.yml'].includes(file.name)) {
            continue;
        }
        const li = document.createElement('li');
        if (file.type === 'file') {
            // `.md`または`.html`で終わらない場合、次に進む
            if (!file.name.endsWith('.md') && !file.name.endsWith('.html')) {
                continue; // 次のループへ進む
            }
            li.appendChild(createFileLink(file));
        } else if (file.type === 'dir') {
            const details = document.createElement('details');
            details.open = true; // デフォルトで開いた状態にする
            const summary = document.createElement('summary');
            summary.textContent = file.name;
            details.appendChild(summary);
            const ul = document.createElement('ul');
            details.appendChild(ul);
            li.appendChild(details);
            await displayFiles(ul, file.path);
        }
        parentElement.appendChild(li);
    }
}

displayFiles(document.getElementById('file-list')).catch(console.error);

</script>
