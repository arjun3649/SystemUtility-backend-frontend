# 🖥️ System Utils Platform

This project is a **full system monitoring solution** consisting of:

- **systemutils-client** → A daemon installed on machines that reports health data   
- **systemutils-backend** → FastAPI service + PostgreSQL DB for storing reports  
- **systemutils-dashboard** →  frontend dashboard to visualize system health  



---

## 🚀 Features
- Collect OS info, disk encryption, antivirus, and sleep settings  
- Backend stores machine health data in PostgreSQL  
- Frontend dashboard (React/Next.js) displays data in real-time  
- Fully Dockerized (backend + frontend + db)  

---

## 📦 Requirements
- Docker  
- Docker Compose
- **systemutils-client** -> https://github.com/arjun3649/SystemUtility

---

## 🔧 Installation & Setup

### 1. Clone repository
```bash
git clone https://github.com/arjun3649/SystemUtility-backend-frontend
cd SystemUtility`
```
### 2. clone the **systemutils-client** 
```bash
https://github.com/arjun3649/SystemUtility
```
## Start service
```bash
docker-compose up -d # it starts the postgres db
uvicorn main:app # will start the backend
# frontend is a static file that can be opened in browser
```
