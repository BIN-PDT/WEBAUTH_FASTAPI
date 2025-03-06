**1. PROJECT**

```
git clone https://github.com/BIN-PDT/WEBAUTH_FASTAPI.git && rm -rf WEBAUTH_FASTAPI/.git
```

_For privacy reasons, replace the sensitive information in `.env` with your own._

-   _Replace `MAIL_ADDRESS` & `MAIL_PASSWORD` (Application Password) with your Gmail Account_.

-   _Generate `SECRET_KEY`_.

    ```
    python
    ```

    ```python
    import secrets
    print(secrets.token_hex(32))
    exit()
    ```

**2. VIRTUAL ENVIRONMENT**

```
python -m venv .venv
```

```
.venv\Scripts\activate.bat
```

**3. DEPENDENCY**

```
python.exe -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

**4. DATABASE**

```
alembic upgrade head
```

**5. RUN TEST**

```
pytest
```

**6. RUN APPLICATION**

```
fastapi dev main.py
```
