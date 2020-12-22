# MARBLE

MARBLE（MARVEL + ASSEMBLE)とは、MARVEL好きによる、MARVEL好きのための映画検索サイトです。

 
# Features
 
- MARVEL映画に特化した検索・解説が読めます
- 好きなキャラクター/楽しみ方で検索も可能
 
# Requirement

### package
```
Package                Version
---------------------- ---------
autopep8               1.5.4  →autopep8 --in-place --aggressive --aggressive ファイル名 で、コードを整型
Django                 3.1.3 →Djangoを利用
django-bootstrap4      2.3.1 →bootstrap4を利用
django-environ         0.4.5 →.envを利用
django-static-md5url   0.1 → CSSのキャッシュリロードで利用
django-http-referrer-policy 1.1.1 →リファラの設定で利用
flake8                 3.8.4 →pep8通りにコードが書けているかを確認
Pillow                 8.0.1 →画像ファイルを利用
requests               2.25.0 →requestsを利用
social-auth-app-django 4.0.0 →SNSログイン実装で利用

### command
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser

```
### design
```
Bootstrap https://getbootstrap.com/
jQuery https://jquery.com/
popper.js https://github.com/popperjs/popper-core/releases

```

### dirctory
```
marble
└── app
    └── static
        └── app
            ├── css
            │   ├── bootstrap.min.css
            │   └── bootstrap.min.css.map
            └── js
                ├── bootstrap.bundle.min.js
                ├── bootstrap.bundle.min.js.map
                ├── jquery-3.4.1.min.js
                └── jquery-3.4.1.min.map

*.map ファイルは、ブラウザーの開発者ツールで、JavaScriptのデバッグをしたり、HTMLの要素を見てCSSを検証したりする際に、元の行番号を出すためのものです。なくても動作はします。
bootstrap.bundle.min.js は、Popper.js を含む（バンドルしている）ものです。
```


# Installation
 
```bash
pip install requirements.txt
```

 
# Author
 
* MARBLE運営事務局
* contact@marble-cinema.com

