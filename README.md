# TNMT
### PLVB cho tài nguyên mt

# Front End
1. Build docker environtment  ( run one time when turn on server or has upate)

```
cd frontEnd/TNMT/frontend
docker-compose build
```

2. Run Frond End

```
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
./scripts/run.sh
```