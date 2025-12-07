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

// 除外対象はルート直下のみで判定する
const rootExcludeNames = ['README.md', 'index.html', 'index.md', 'script.js', '_config.yml'];

// テキストツリー格納
const treeLines = [];

async function getFiles(path = '') {
  const url = `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
  const response = await fetch(url);
  const data = await response.json();
  return data;
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

function addTreeLine(depth, name) {
  const indent = '  '.repeat(depth);
  treeLines.push(`${indent}- ${name}`);
}

/**
 * フォルダを再帰的に処理し、
 * - DOMに階層構造を追加
 * - treeLines にテキストツリーを追加
 * しつつ、「最終的に表示対象のファイル・フォルダが何も無ければ false」を返す。
 *
 * @param {HTMLElement} parentElement 追加先の <ul>
 * @param {string} path GitHub 上のパス
 * @param {number} depth テキストツリー用の深さ
 * @param {boolean} isRoot ルートかどうか
 * @returns {Promise<boolean>} 何か一つでも表示した要素があれば true
 */
async function displayFiles(parentElement, path = '', depth = 0, isRoot = false) {
  const files = await getFiles(path);

  files.sort((a, b) => {
    if (a.type === b.type) {
      return a.name.localeCompare(b.name, 'ja');
    }
    return a.type === 'dir' ? -1 : 1;
  });

  let hasVisibleChild = false;

  for (const file of files) {
    // ルート直下のみ除外対象を適用
    if (isRoot && rootExcludeNames.includes(file.name)) {
      continue;
    }

    if (file.type === 'dir') {
      // ディレクトリの場合は一旦仮の <ul> を作り、再帰結果によって表示可否を決定
      const li = document.createElement('li');
      const details = document.createElement('details');
      details.open = true;

      const summary = document.createElement('summary');
      summary.textContent = file.name;
      details.appendChild(summary);

      const ul = document.createElement('ul');
      details.appendChild(ul);
      li.appendChild(details);

      // サブフォルダ・ファイルを再帰的に処理
      const childHasVisible = await displayFiles(ul, file.path, depth + 1, false);

      if (childHasVisible) {
        // このフォルダ配下に表示対象がある場合のみ追加
        parentElement.appendChild(li);
        addTreeLine(depth, file.name + '/');
        hasVisibleChild = true;
      }

    } else if (file.type === 'file') {
      // 対象拡張子以外はスキップ
      if (!file.name.endsWith('.md') && !file.name.endsWith('.html')) {
        continue;
      }

      const li = document.createElement('li');
      li.appendChild(createFileLink(file));
      parentElement.appendChild(li);
      addTreeLine(depth, file.name);
      hasVisibleChild = true;
    }
  }

  return hasVisibleChild;
}

// 画面描画
(async () => {
  const ulRoot = document.getElementById('file-list');
  const hasAny = await displayFiles(ulRoot, '', 0, true);

  // テキストツリー出力（何か一つでもあれば）
  if (hasAny) {
    const pre = document.getElementById('file-tree-text');
    pre.textContent = treeLines.join('\n');
  }
})();
</script>
