# arxiv2line

## About
- Automatically searches for articles on arXiv, translates them at DeepL, and sends them to LINE.
- サーベイの自動化用スクリプト。特定のキーワードに関連した arXiv の論文を自動で検索し、タイトルと概要を DeepL で翻訳し LINE に自動送信する。
- arXiv API、DeepL API、IFTTT、webhook、LINE Notify を使用

## Setup
LINE に送信せず、ローカルにtsvとして結果を保存するだけの場合、以下の準備は必要なし。

- IFTTT 登録
- webhook のPOST先URL取得し```web-post-url.txt```に保存
- DeepL API の認証キーを取得し```deepl-api-key.txt```に保存

## Usage

検索し、翻訳結果等を LINE に送信
```
$ python send.py -q <検索クエリ> -d <出版日> -m <最大検索件数>

# 例）transformer に関連した、2021年1月1日の論文を最大 100 件検索しLINEに送信する場合
$ python send.py -q transformer -d 2021/1/1 -m 100
```

検索し、翻訳結果等をローカルにtsvとして保存
```
$ python search.py -q <検索クエリ> -d <出版日> -m <最大検索件数> -f <結果tsvファイル保存先>

# 例）transformer に関連した、2021年1月1日の論文を最大 100 件検索し、```result.tsv```に書き出す場合
$ python search.py -q transformer -d 2021/1/1 -m 100 -f result.tsv
```
