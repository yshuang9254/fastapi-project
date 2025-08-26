# API 文件

本專案使用 **FastAPI** 開發，自動產生 Swagger UI 文件。

- **Swagger UI:** [https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/docs#/](https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/docs#/)  
- **ReDoc:** [https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/redoc](https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/redoc)  
- **OpenAPI JSON:** [https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/openapi.json](https://yushans-fastapi-project-a3a1db9af76e.herokuapp.com/openapi.json)  

---
## 目錄
1. [Root](#root)
2. [使用者 Users](#使用者-users)
3. [認證 Auth](#認證-auth)
4. [貼文 Posts](#貼文-posts)
5. [投票 Vote](#投票-vote)
6. [Schema 總覽](#Schema-總覽)
6. [啟動方式](#啟動方式)
---

### Root

- **GET /**  
  - 功能：測試 API 是否啟動  
  - 回應：200 OK → {}

---

### 使用者 (Users)

- **POST /users/**  
  - 功能：建立新使用者  
  - Request Body: UserCreate
    ```json
    {
      "email": "user@example.com",
      "password": "string"
    }
    ```  
  - Response 201 Created (UserOut):  
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2025-08-26T10:00:00"
    }
    ```
    - Response 422 Validation Error (HTTPValidationError):  
    ```json
    {
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
    ]
    }

    ```

- **GET /users/{id}**  
  - 功能：取得單一使用者（需登入授權）  
  - Path Param: `id: int`  
  - Response 200 OK (UserOut):  
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2025-08-26T10:00:00"
    }
    ```
  - Response 422 Validation Error (HTTPValidationError):  
    ```json
    {
    "detail": [...]
    }
    ```
---

### 認證 (Auth)

- **POST /login**  
  - 功能：登入並取得 Token (OAuth2 Password Flow)  
  - Request Body (x-www-form-urlencoded):  
    ```
    username=user@example.com
    password=123456
    ```  
  - Response 200 OK (Token):  
    ```json
    {
      "access_token": "xxxxx",
      "token_type": "bearer"
    }
    ```
  - Response 422 Validation Error (HTTPValidationError):  
    ```json
    {
    "detail": [...]
    }
    ```
---

### 貼文相關 (Posts)

- **GET /posts/**  
  - 功能：取得所有貼文（需登入授權）  
  - Query Params:  
    - limit (int, 預設 100)  
    - skip (int, 預設 0)  
    - search (string, 預設空字串)  
  - Response 200 OK (PostOut[]):  
    ```json
    [
      {
        "Post": {
          "id": 1,
          "title": "My First Post",
          "content": "Hello World",
          "published": true,
          "created_at": "2025-08-26T10:00:00",
          "owner_id": 1,
          "owner": {
            "id": 1,
            "email": "user@example.com",
            "created_at": "2025-08-26T09:00:00"
          }
        },
        "votes": 5
      }
    ]
    ```
  - Response 422 Validation Error (HTTPValidationError):  


- **POST /posts/**  
  - 功能：建立新貼文（需登入授權）  
  - Request Body (PostCreate):  
    ```json
    {
      "title": "New Post",
      "content": "Post content",
      "published": true
    }
    ```  
  - Response: 201 Created (Post)
    ```json
    {
        "id": 2,
        "title": "New Post",
        "content": "Post content",
        "published": true,
        "created_at": "2025-08-26T10:10:00",
        "owner_id": 1,
        "owner": {
            "id": 1,
            "email": "user@example.com",
            "created_at": "2025-08-26T09:00:00"
        }
    }
    ```  
  - Response 422 Validation Error (HTTPValidationError): 
- **GET /posts/latest**  
  - 功能：取得最新貼文  
  - Response: 200 OK (PostOut) 

- **GET /posts/{id}**  
  - 功能：取得單一貼文（需登入授權）  
  - Path Param: `id: int`
  - Response: 200 OK (PostOut)

- **PUT /posts/{id}**  
  - 功能：更新貼文（需登入授權，且必須為發文本人）  
  - Request Body: PostCreate
  - Response: 200 OK (PostOut)
  - Response 422 Validation Error (HTTPValidationError)

- **DELETE /posts/{id}**  
  - 功能：刪除貼文（需登入授權，且必須為發文本人）  
  - Path Param: `id: int`  
  - Response: 204 No Content
  - Response 422 Validation Error (HTTPValidationError)

---

### 投票 (Vote)

- **POST /vote/**  
  - 功能：對貼文投票（需登入授權）  
  - Request Body: Vote
    ```json
    {
      "post_id": 1,
      "dir": 1   // 1 = 按讚，0 = 取消
    }
    ```  
  - Response 201 Created: 空物件 {}
  - Response 422 Validation Error (HTTPValidationError)


###  Schema 總覽

#### UserCreate  
| 欄位 | 型別 | 預設值 | 描述 |
|------|------|--------|------|
| email | EmailStr |  | 使用者 Email |
| password | str |  | 使用者密碼 |

#### UserOut
| 欄位 | 型別 | 預設值 | 描述 |
|------|------|--------|------|
| id | int |  | 使用者 ID |
| email | EmailStr |  | 使用者 Email |
| created_at | datetime |  | 建立時間 |

#### UserLogin
| 欄位 | 型別 | 描述 |
|------|------|------|
| email | EmailStr | 使用者 Email |
| password | str | 使用者密碼 |

---

#### PostBase
| 欄位 | 型別 | 預設值 | 描述 |
|------|------|--------|------|
| title | str |  | 標題 |
| content | str |  | 內容 |
| published | bool | True | 是否公開 |

#### PostCreate
- **繼承自 PostBase**

#### Post
| 欄位 | 型別 | 描述 |
|------|------|------|
| id | int | 文章 ID |
| created_at | datetime | 建立時間 |
| owner_id | int | 建立者 ID |
| owner | UserOut | 建立者資訊 |

#### PostOut
| 欄位 | 型別 | 描述 |
|------|------|------|
| Post | Post | 文章內容 |
| votes | int | 按讚數 |

---

#### Token
| 欄位 | 型別 | 描述 |
|------|------|------|
| access_token | str | JWT Token |
| token_type | str | Token 類型 |

#### TokenData
| 欄位 | 型別 | 預設值 | 描述 |
|------|------|--------|------|
| id | Optional[int] | None | 使用者 ID |

---

#### Vote
| 欄位 | 型別 | 預設值 | 描述 |
|------|------|--------|------|
| post_id | int |  | 文章 ID |
| dir | int | 0=取消讚，1=按讚 |

---

###  啟動方式
```bash
uvicorn app.main:app --reload