# Modern-App-Development

### 🔥 Flask Context Management
```plaintext
                    +---------------------+
                    |  Flask App Startup  |
                    +---------------------+
                              |
                              ↓
                 +-----------------------+
                 |  Application Context  |
                 |  (app.app_context())  |
                 +-----------------------+
                              |
                              ↓
              -------------------------
             |                         |
       Request Context           Non-Request Code
      (During API Calls)        (DB, Background Jobs)
             |                         |
             ↓                         ↓
     +----------------+        +----------------+
     | request object |        | current_app    |
     | session object |        | g (global obj) |
     | g (global obj) |        +----------------+
     +----------------+
             |
             ↓
     +------------------+
     | Request Handling |
     +------------------+
             |
             ↓
      +-------------+
      | Response     |
      +-------------+
```

---

### 🎯 How it works:
| Context                  | Description                     | Automatically Managed |
|---------------------------|--------------------------------|-----------------------|
| **Application Context**    | Binds the app instance to the current thread | ❌ No (Use `app.app_context()`) |
| **Request Context**        | Manages request-specific data like `request`, `session`, and `g` | ✅ Yes (Inside routes) |
| **Global Object (g)**      | Temporary storage for request-level data | ✅ Yes |
| **current_app**            | The currently running app instance | ✅ Inside request | ❌ Outside request |

---