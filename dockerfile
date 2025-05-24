# Use Alpine Linux for a smaller image
FROM python:3.9-alpine

# Set environment variables for Pillow (optional, but good practice for Alpine)
ENV CFLAGS="-fPIC" \
    LDFLAGS="-Wl,--strip-all"

# Define system build dependencies for Pillow AND psycopg2-binary
# postgresql-dev is crucial for psycopg2-binary to build correctly on Alpine
RUN apk add --no-cache jpeg-dev zlib-dev libwebp-dev tiff-dev openjpeg-dev freetype-dev lcms2-dev \
    postgresql-dev \
    build-base && \
    rm -rf /var/lib/apk/lists/*

# กำหนด working directory ภายใน container
WORKDIR /app

# คัดลอก requirements.txt ไปยัง working directory ก่อน
COPY requirements.txt /app/

# ติดตั้งแพ็คเกจ Python ที่จำเป็น
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to keep the final image small
RUN apk del build-base \
    jpeg-dev \
    zlib-dev \
    libwebp-dev \
    tiff-dev \
    openjpeg-dev \
    freetype-dev \
    lcms2-dev \
    postgresql-dev

# คัดลอกโค้ดโปรเจกต์ Django ทั้งหมดไปยัง working directory
COPY . /app/

# กำหนด port ที่ Django จะรัน (default คือ 8000)
EXPOSE 8000

# รัน Django development server เมื่อ container เริ่มต้น
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]