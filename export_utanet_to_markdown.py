import requests
from bs4 import BeautifulSoup

def export_utanet_to_markdown(url):
    """
    指定されたUta-Netの楽曲ページからタイトルと歌詞を抽出し、Markdown形式で保存する関数
    :param url: Uta-Netの楽曲ページのURL
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # タイトルの抽出
    title_tag = soup.select_one('h2.kashi-title')
    title = title_tag.get_text(strip=True) if title_tag else 'タイトル不明'

    # 歌詞の抽出
    kashi_area = soup.find(id="kashi_area")
    if kashi_area:
        # <br>タグをそのまま残すため、innerHTMLを取得
        # kashi_areaの子要素をすべて文字列として連結
        lyrics = ""
        for elem in kashi_area.contents:
            if isinstance(elem, str):
                lyrics += elem
            else:
                # <br>タグはそのまま文字列として追加
                if elem.name == "br":
                    lyrics += "\n"
                else:
                    # その他のタグはテキストのみ抽出
                    lyrics += elem.get_text()
        lyrics = lyrics.strip()
    else:
        lyrics = '歌詞が見つかりませんでした。'

    # Markdown形式で保存
    markdown_content = lyrics

    # ファイル名をタイトルから生成（ファイル名に使えない文字を除去）
    import re
    safe_title = re.sub(r'[\\/*?:"<>|]', '', title)
    filename = f"{safe_title}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"Markdownファイルとして保存しました: {filename}")

# 例: 関数の呼び出し
export_utanet_to_markdown("https://www.uta-net.com/song/358967/")
