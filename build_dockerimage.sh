rm dossier-aggr.tar
docker build . -t dossier-aggr
docker save dossier-aggr -o dossier-aggr.tar
