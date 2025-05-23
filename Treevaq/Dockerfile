# ใช้ Python 3.10 slim เป็น base image
FROM python:3.10-slim

# กำหนด working directory ชั่วคราวสำหรับการคัดลอกไฟล์
WORKDIR /app

# อัปเดตแพ็คเกจและติดตั้ง build dependencies ที่จำเป็นสำหรับไลบรารี Python บางตัว
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
# การทำเช่นนี้ก่อน COPY . . จะช่วยให้ Docker ใช้ cache ได้ดีขึ้นหาก requirements.txt ไม่เปลี่ยนแปลง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดแอปพลิเคชันทั้งหมดจาก host ไปยัง /app ในคอนเทนเนอร์
# สมมติว่าโครงสร้างโปรเจกต์ของคุณบน host มีโฟลเดอร์ 'myproject' ที่มี manage.py อยู่ข้างใน
COPY . .

# เปลี่ยน working directory ไปยัง root ของโปรเจกต์ Django (ที่ manage.py อยู่)
# นี่คือส่วนสำคัญที่แก้ไขปัญหา 'No module named myproject.settings'
# เพราะ manage.py จะถูกรันจากไดเรกทอรีนี้
WORKDIR /app/myproject

# เปิดพอร์ต 8000 เพื่อให้สามารถเข้าถึงแอปพลิเคชันได้จากภายนอกคอนเทนเนอร์
EXPOSE 8000

# กำหนดคำสั่งเริ่มต้น ซึ่งจะถูก override ด้วย 'command' ใน docker-compose.yml
# แต่เป็น good practice ที่จะมี CMD ที่ใช้งานได้ใน Dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
