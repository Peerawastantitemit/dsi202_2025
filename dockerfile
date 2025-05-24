# ใช้ Alpine Linux เพื่อให้ image มีขนาดเล็ก
FROM python:3.9-alpine

# กำหนด working directory ภายใน container
WORKDIR /app

# คัดลอก requirements.txt ไปยัง working directory ก่อน
COPY requirements.txt /app/

# ติดตั้งแพ็คเกจ Python ที่จำเป็น
RUN pip install -r requirements.txt

# คัดลอกโค้ดโปรเจกต์ Django ทั้งหมดไปยัง working directory
COPY . /app/

# กำหนด port ที่ Django จะรัน (default คือ 8000)
EXPOSE 8000

# รัน Django development server เมื่อ container เริ่มต้น
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]