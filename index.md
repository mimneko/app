---
title: リンク集
---

<div class="folder-tree">
  <ul id="file-list"></ul>
</div>

<pre id="file-tree-text"></pre>

<script>
const owner  = 'mimneko';
const repo   = 'app';
const branch = 'main';

// 再帰的取得用のテキストツリー格納配列
const treeLines = [];

// GitHub API から、指定パス直下のファイル／フォルダ一覧を取得
async function getFiles(path = '') {
    const url = `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

// .md / .html 用リンク生成
function createFileLink(file) {
    const a = document.createElement('a');

    if (file.name.endsWith('.md')) {
        // .md は .html に変換してリンク
        const htmlName = file.name.replace(/\.md$/, '.html');
        a.href = `https://${owner}.github.io/${repo}/${file.path.replace(file.name, htmlName)}`;
    } else if (file.name.endsWith('.html')) {
        // .html はそのままリンク
        a.href = `https://${owner}.github.io/${repo}/${file.path}`;
    }

    a.textContent = file.name;
    a.target = '_blank';
    return a;
}

// テキスト用ツリー行追加
function addTreeLine(depth, name) {
    const indent = '  '.repeat(depth);
    treeLines.push(`${indent}- ${name}`);
}

// 再帰的に GitHub 上のフォルダをたどり、
// 1) DOM に階層構造 (details/summary + ul/li)
// 2) treeLines にテキストの階層構造
// を構築する
async function displayFiles(parentElement, path = '', depth = 0) {
    const files = await getFiles(path);

    // ディレクトリを先、ファイルを後に並べる（任意）
    files.sort((a, b) => {
        if (a.type === b.type) {
            return a.name.localeCompare(b.name, 'ja');
        }
        return a.type === 'dir' ? -1 : 1;
    });

    for (const file of files) {
        // 特定ファイルは除外
        if (['README.md', 'index.html', 'index.md', 'script.js', '_config.yml'].includes(file.name)) {
            continue;
        }

        const li = document.createElement('li');

        if (file.type === 'dir') {
            // ディレクトリ: details/summary で折りたたみ可能にし、再帰呼び出し
            const details = document.createElement('details');
            details.open = true; // デフォルトで開いた状態

            const summary = document.createElement('summary');
            summary.textContent = file.name;
            details.appendChild(summary);

            const ul = document.createElement('ul');
            details.appendChild(ul);

            li.appendChild(details);
            parentElement.appendChild(li);

            // テキストツリーにもディレクトリを追加
            addTreeLine(depth, file.name + '/');

            // 再帰的にサブフォルダを処理
            await displayFiles(ul, file.path, depth + 1);

        } else if (file.type === 'file') {
            // 対象拡張子以外はスキップ
            if (!file.name.endsWith('.md') && !file.name.endsWith('.html')) {
                continue;
            }

            // リンクを作成してツリーに追加
            li.appendChild(createFileLink(file));
            parentElement.appendChild(li);

            // テキストツリーにもファイルを追加
            addTreeLine(depth, file.name);
        }
    }
}

// 画面描画＋テキストツリー出力
displayFiles(document.getElementById('file-list'))
    .then(() => {
        const pre = document.getElementById('file-tree-text');
        pre.textContent = treeLines.join('\n');
    })
    .catch(console.error);

</script>
