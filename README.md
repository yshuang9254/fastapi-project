# FastAPI 貼文投票系統

## 專案簡介

本專案是一個以 **FastAPI** 開發的 RESTful API，模擬社群平台的貼文與投票功能。
自動產生 Swagger UI 文件。
### 相關連結
- **api.md:**[查看 API 文件](docs/api.md)
- **Swagger UI:** [https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/docs#/](https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/docs#/)  
- **ReDoc:** [https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/redoc](https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/redoc)  
- **OpenAPI JSON:** [https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/openapi.json](https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/openapi.json)  


### 專案特色

- 使用者註冊、登入 (JWT 驗證)
- 貼文 CRUD
- 投票 / 取消投票
- 整合 PostgreSQL 或 Supabase（托管 PostgreSQL）
- Alembic 資料庫遷移
- Pytest 測試
- Docker 容器化與 GitHub Actions CI/CD

---

## 技術

- **後端框架**：FastAPI  
- **資料庫**：PostgreSQL / Supabase  
- **ORM & Migration**：SQLAlchemy, Alembic  
- **認證**：JWT (OAuth2 Password Flow)  
- **測試**：Pytest  
- **容器化**：Docker, Docker Compose  
- **CI/CD**：GitHub Actions  

---

## 目錄結構

```text
app/                     # 主程式與 API 路由  
tests/                   # 測試程式  
alembic/                 # 資料庫遷移管理  
.github/                 # CI/CD 工作流程  
docker-compose-dev.yml  # 開發用 Docker Compose  
docker-compose-prod.yml # 生產用 Docker Compose  
```

---

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

建立 `.env`，可參考範例 `.env.example`：

```env
DATABASE_HOSTNAME=your_database_host
DATABASE_PORT=your_database_port
DATABASE_USERNAME=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_NAME=your_database_name

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> ⚠️ 請勿將 `.env` 推到公開 GitHub，請在 `.gitignore` 中加入 `.env`

### 3. 初始化資料庫

```bash
alembic upgrade head
```

### 4. 啟動服務

```bash
uvicorn app.main:app --reload
```

或使用 Docker：

```bash
docker-compose -f docker-compose-dev.yml up --build
```

---

## API 文件

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

---

## 主要功能

- 使用者註冊、登入（JWT 驗證）
- 貼文 CRUD（創建、查詢、修改、刪除）
- 投票 / 取消投票
- 權限控管（僅本人可編輯 / 刪除貼文）

---

## API 範例

### Users

- `POST /users/`：建立新使用者  
- `GET /users/{id}`：取得單一使用者（需授權）

### Auth

- `POST /login`：登入並取得 JWT Token

### Posts

- `GET /posts/`：取得所有貼文（支援搜尋、分頁）  
- `POST /posts/`：建立新貼文  
- `GET /posts/{id}`：取得單一貼文  
- `PUT /posts/{id}`：更新貼文（需本人）  
- `DELETE /posts/{id}`：刪除貼文（需本人）

### Vote

- `POST /vote/`：對貼文投票或取消投票

> 詳細欄位、Request/Response 請參考 API 文件

---

## Schema 總覽

### UserCreate

| 欄位     | 型別     | 描述         |
|----------|----------|--------------|
| email    | EmailStr | 使用者 Email |
| password | str      | 使用者密碼   |

### UserOut

| 欄位       | 型別     | 描述         |
|------------|----------|--------------|
| id         | int      | 使用者 ID    |
| email      | EmailStr | Email        |
| created_at | datetime | 建立時間     |

### PostBase / PostCreate

| 欄位     | 型別 | 描述         |
|----------|------|--------------|
| title    | str  | 標題         |
| content  | str  | 內容         |
| published| bool | 是否公開（預設 True）|

### PostOut

| 欄位 | 型別 | 描述     |
|------|------|----------|
| Post | Post | 文章內容 |
| votes| int  | 按讚數   |

### Token / TokenData

| 欄位         | 型別         | 描述         |
|--------------|--------------|--------------|
| access_token | str          | JWT Token    |
| token_type   | str          | Token 類型   |
| id           | Optional[int]| 使用者 ID    |

### Vote

| 欄位    | 型別 | 描述         |
|---------|------|--------------|
| post_id | int  | 文章 ID      |
| dir     | int  | 1=按讚, 0=取消 |

---

## 測試

```bash
pytest
```

---

## License

MIT License
