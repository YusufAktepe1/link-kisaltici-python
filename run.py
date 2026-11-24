"""Uygulamayı başlatır: python run.py  (VS Code'da ▶ Run ile de çalışır)"""
import uvicorn

if __name__ == "__main__":
    # reload=True: kodu değiştirip kaydettiğinde sunucu kendini yeniden başlatır
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
