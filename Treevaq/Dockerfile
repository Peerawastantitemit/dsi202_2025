FROM python:3.10-slim

WORKDIR /app

# ติดตั้งแพ็คเกจที่จำเป็นสำหรับ build และ dependencies ของ Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดแอปพลิเคชันทั้งหมด
COPY . .

# เปิดพอร์ต 8000
EXPOSE 8000

# กำหนดคำสั่งเริ่มต้นที่จะรันเมื่อคอนเทนเนอร์เริ่มต้น
# นี่คือคำสั่งที่เคยอยู่ใน entrypoint.sh สำหรับการรัน Django server
# หากคุณต้องการรัน migrate ก่อน ให้พิจารณาใส่ใน docker-compose.yml แทน
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
