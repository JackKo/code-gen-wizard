# code-gen-wizard
When Playwright code-gen needs some magic - this is the answer 

## 🧰 Prerequisites

- Python 3.8+
- Node.js + npm
- Playwright installed globally (`npm install -g playwright`)

## 📦 Setup

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

## ▶ Usage

1. Run backend and frontend as above.
2. Open browser at `http://localhost:5173`.
3. Click **Start Codegen** – the output of `playwright codegen` will appear in the editor.
4. Edit the code in the editor.
5. Click **Save** to save the edited C# code to `backend/saved/edited_code.cs`.

## 🧪 Notes

- This is a blocking version (waits for playwright codegen to complete).
- In next steps we can add streaming or Page Object file generation.


## 🧱 Page Object Generator (Prototype)

- Use special comment markers to define page object structure:
  ```csharp
  // <# LoginPage.Login #>
  await page.FillAsync("#username", "user");
  await page.FillAsync("#password", "pass");
  await page.ClickAsync("button[type='submit']");
  // </#>
  ```

- Click **"Generate Page Objects"** in UI to generate C# classes in `backend/generated_pages/`.

