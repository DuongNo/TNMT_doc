# TNMT
### PLVB cho tài nguyên mt

## Run code on Server
### Run Front End
1. Build docker environtment  ( run one time when turn on server or has upate)

```
cd /home/vdc/project/nlp/TNMT
cd frontEnd/TNMT/frontend
docker-compose build
```

2. Run Frond End
```
cd /home/vdc/project/nlp/TNMT
./scripts/runfe.sh
```

go to : local 172.16.50.201:18000 or internet http://113.20.109.148:2599  to view web app document

# Run Backend PLVB
 
1. Activate Environtment

```
conda activate PLVB
```

2. Run Backend

```
cd /home/vdc/project/nlp/TNMT
./scripts/run.sh
```

## Run code on new project
### Run Front End

```
git clone https://github.com/DuongNo/TNMT.git
cd TNMT
mkdir frontEnd
cd frontEnd
git clone https://github.com/DuongNo/TNMT.git
cd TNMT
git checkout trang-fe
cd frontend
docker-compose build
docker compose up
```

```
cd /home/vdc/project/nlp/TNMT
conda activate PLVB
cp -r /home/vdc/project/nlp/TNMT/weights .

```

1. Build docker environtment  ( run one time when turn on server or has upate)

```
cd /home/vdc/project/nlp/TNMT
cd frontEnd/TNMT/frontend
docker-compose build
```

2. Run Frond End
```
cd /home/vdc/project/nlp/TNMT
./scripts/runfe.sh
```

go to : local 172.16.50.201:18000 or internet http://113.20.109.148:2599  to view web app document

# Run Backend PLVB
 
1. Activate Environtment

```
conda activate PLVB
```

2. Run Backend

```
cd /home/vdc/project/nlp/TNMT
./scripts/run.sh
```