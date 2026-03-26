| NRP        | Nama              |
|:-----------:|:-----------------:|
| 5025241021 | Kartika Nana Naulita |

# Penugasan 1 Netics 2026
Pada tugas ini dilakukan pembuatan REST API sederhana menggunakan Flask sebagai layanan utama. Selanjutnya, aplikasi dikemas ke dalam container menggunakan Docker. Aplikasi kemudian dideploy ke VPS publik menggunakan layanan Microsoft Azure agar dapat diakses melalui internet. Untuk mengatur akses, digunakan Nginx sebagai reverse proxy dengan port 5000. Proses konfigurasi server diotomatisasi menggunakan Ansible guna meningkatkan efisiensi dan konsistensi. Terakhir, diterapkan mekanisme CI/CD menggunakan GitHub Actions sehingga setiap perubahan kode yang dikirim ke repository dapat langsung terdeploy secara otomatis ke VPS.

# API Endpoint
### 1. Membuat Project
Langkah pertama adalah membuat folder project sebagai tempat penyimpanan seluruh file aplikasi.
```
mkdir health-api
cd health-api
```
### 2. Membuat File Python

Selanjutnya dibuat file Python untuk menuliskan kode API.
```
touch apl.py
```
### 3. Menulis Kode API
```
from flask import Flask, jsonify
import time

app = Flask(__name__)

start_time = time.time()

@app.route("/health")
def health():
   print("Endpoint /health diakses!") 
   
   return jsonify({
       "nama": "KARTIKA NANA NAULITA",
       "nrp": "5025241021",
       "status": "UP",
       "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
       "uptime": int(time.time() - start_time)
   })

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
```
- Flask digunakan untuk membuat web server sederhana
- Endpoint /health digunakan untuk mengecek status aplikasi
- timestamp menampilkan waktu saat request
- uptime menunjukkan lama aplikasi berjalan

### 4. Instalasi Dependency

Sebelum menjalankan API, dilakukan instalasi dependency yang dibutuhkan.

a. Update package
```
sudo apt-get update
```
b. Install Python dan tools pendukung
```
sudo apt install python3-full python3-venv python3-pip -y
```
c. Membuat Virtual Environment
```
python3 -m venv venv
```
d. Mengaktifkan Virtual Environment
```
source venv/bin/activate
```
e. Install Flask
```
python -m pip install flask
```
### 5. Menjalankan API
API dijalankan dengan perintah:
```
python apl.py
```
### 6. Pengujian API
a. Melalui Browser : http://localhost:5000/health   

b. Melalui Terminal : curl http://localhost:5000/health

### 7. Hasil
![img](https://i.imgur.com/vs1OFJr.png)
![img](https://i.imgur.com/87WLd5L.png)



# DOCKER 
### 1. Pembuatan Dockerfile
Sebelum build, dibuat file bernama Dockerfile.
```
nano Dockerfile
```
Dengan Isi :
```
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install flask

CMD ["python", "apl.py"]
```

2. Build Docker Image
```
docker build -t health-api .
```

### 3. Menjalankan Container
```
docker run -p 5000:5000 health-api
```
Port 5000 lokal dihubungkan ke port 5000 dalam container
API dapat diakses dari luar container

### 4. Pengujian
a. Melalui Browser : http://localhost:5000/health  

b. Melalui Terminal : curl http://localhost:5000/health

### 5. Hasil
![img](https://i.imgur.com/1pv0MQV.png)
![img](https://i.imgur.com/f7hsUaN.png)


# VPS(Azure)
VPS dibuat menggunakan layanan Microsoft Azure.

### 1. Akses ke VPS
Koneksi ke VPS dilakukan menggunakan SSH:
```
ssh -i ~/naulita_key.pem naulita@20.195.8.104
```
naulita_key.pem didapatkan dari saat pembuatan VPS.

### 2. Clone Repository
```
git clone https://github.com/K-naulita/health-api.git
cd health-api
```
Mengambil source code aplikasi dari repository GitHub ke VPS.

### 3. Build Docker Image
```
sudo docker build -t health-api .
```
Membuat Docker image dari aplikasi yang telah dibuat.

### 4. Menjalankan Container
```
sudo docker run -d -p 5000:5000 --name api health-api
```
### 5. Verifikasi Container
```
sudo docker ps
```
### 6. Pengujian di VPS
```
curl http://localhost:5000/health
```
### 7. Membuka Port di Azure
Pada konfigurasi jaringan di Microsoft Azure, ditambahkan aturan:
```
Port: 5000
Protocol: TCP
Action: Allow
```
### 8. Pengujian dari Browser
http://20.195.8.104:5000/health

### 9. Konfigurasi Nginx (Reverse Proxy)
- Instalasi Nginx
```
sudo apt update
sudo apt install nginx -y
```
- Menjalankan Nginx
```
sudo systemctl start nginx
sudo systemctl enable nginx
```
- Konfigurasi Nginx
Edit :
```
sudo nano /etc/nginx/sites-available/default
```
```
server {
   listen 8080;

   location / {
       proxy_pass http://localhost:5000;
   }
}
```
Port 8080 digunakan sebagai akses publik
Request akan diteruskan ke API di port 5000

- Restart Nginx
```
sudo systemctl restart nginx
```
- Membuka Port 8080
```
Port: 8080
Protocol: TCP
Action: Allow
```
### 10. Otomatisasi dengan Ansible
- Instalasi Ansible  
  Lakukan di Local (exit dari VPS)
```
sudo apt update
sudo apt install ansible -y
```
- Membuat Inventory
File: inventory.ini
```
[server]
20.195.8.104 ansible_user=naulita ansible_ssh_private_key_file=~/naulita_key.pem
```
- Membuat Playbook
```
nano nginx.yml
```
```
- hosts: server
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Copy configuration nginx
      copy:
        dest: /etc/nginx/sites-available/default
        content: |
          server {
              listen 8080;
              location / {
                  proxy_pass http://localhost:5000;
              }
          }

    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```
- Menjalankan Playbook
```
ansible-playbook -i inventory.ini nginx.yml
```
Akan menginstall Nginx -> Mengatur konfigurasi -> Merestart service

### 11. Pengujian  
http://20.195.8.104:8080/health  
http://20.195.8.104:5000/health

### 12. Hasil
![img](https://i.imgur.com/r9dvdfG.png)
![ansible](https://i.imgur.com/fkwi78i.png)
![5000](https://i.imgur.com/qW9Cf6T.png)
![8080](https://i.imgur.com/qAZVy9V.png)


# GitHub
### 1. Buat Workflow CI/CD
File:
```
health-api/.github/workflows/deploy.yml
```
```
on:
 push:
   branches:
     - main

jobs:
 deploy:
   runs-on: ubuntu-latest

   steps:
     - name: Deploy via SSH
       uses: appleboy/ssh-action@v1.0.0
       with:
         host: 20.195.8.104
         username: naulita
         key: ${{ secrets.SSH_PRIVATE_KEY }}
         script: |
           set -e
           cd /home/naulita
           rm -rf health-api
           git clone https://github.com/K-naulita/health-api.git
           cd health-api
           sudo docker stop api || true
           sudo docker rm api || true
           sudo docker rmi health-api || true
           sudo docker build --no-cache -t health-api .
           sudo docker run -d -p 5000:5000 --name api health-api
```
### 2. Konfigurasi Secret
Untuk menjaga keamanan, private key tidak disimpan langsung di repository, melainkan menggunakan GitHub Secrets.

### 3. Proses Deployment
Dilakukan dengan mencoba mengubah misal status pada apl.py kemudian di push dan di cek hasil deploynya pada tab "Action" di repository.
```
git add .
git commit -m "update api"
git push
```
### 4. Pengujian
http://20.195.8.104:8080/health   
http://20.195.8.104:5000/health

### 5. Hasil
![img](https://i.imgur.com/FdhefZY.png)
![img](https://i.imgur.com/Dx8en7L.png)
![img](https://i.imgur.com/krCCoQL.png)


## Resource
https://github.com/MrWhok/penugasan-netics-1-2025/blob/main/README.md
https://medium.com/@kakamber07/how-to-set-up-ci-cd-with-docker-a-step-by-step-hands-on-guide-c6e180436daa
https://chatgpt.com/share/69c54300-1224-8324-933a-b8e2349bd23c

## Link
Docker Image:  
https://hub.docker.com/r/knaulita/health-api

URL API (via Nginx):  
http://20.195.8.104:8080/health

URL API langsung (container):  
http://20.195.8.104:5000/health
