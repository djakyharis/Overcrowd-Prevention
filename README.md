
---

## 🚀 **System Overview**
Sistem ini mensimulasikan platform pemantauan crowd secara real-time dengan arsitektur ala edge-computing:

**1. Main Producer (`main.py`)**
- Meng-generate data crowd secara dinamis (venue → count → status).
- Update real-time state ke **Redis**.
- Insert historical log ke **PostgreSQL**.

**2. Backend Database (`backend/db.py`)**
- Manages PostgreSQL connection.
- Membuat tabel `occupancy_log`.
- Menyimpan event crowd (timestamp, venue, count, status, method, confidence).

**3. Dashboard Monitoring (`dashboard/app.py`)**
- Menampilkan status venue real-time.
- Menampilkan grafik historical crowd (time-series).
- Auto-refresh setiap 3 detik.
- Data di-load dari Redis + PostgreSQL.

**4. Docker Infra (`docker-compose.yml`)**
- Redis
- PostgreSQL 15
- Persistance via docker volumes

---

## 🧱 **Technology Stack**
| Layer | Tools |
|-------|--------|
| Realtime Cache | Redis |
| Database | PostgreSQL 15 |
| Dashboard | Streamlit |
| Simulation Engine | Python + NumPy |
| Containerization | Docker Compose |
| Programming Language | Python 3.9+ |

---

## 🛠️ **Setup & Installation**
```bash
git clone https://github.com/<username>/demo-overcrowd.git
cd demo-overcrowd