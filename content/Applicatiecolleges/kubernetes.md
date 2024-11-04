---
title: "Kubernetes"
weight: 10
author: Arne Duyver
draft: false
---

## Wat is Kubernetes?

Kubernetes (afgekort als K8s) is een open-source platform ontworpen voor het automatiseren van de uitrol, schaalvergroting en beheer van gecontaineriseerde applicaties. Het helpt ontwikkelaars en operationele teams om applicaties in containers (zoals Docker) te beheren en te schalen. Kubernetes biedt een flexibele, gedistribueerde infrastructuur waarin je eenvoudig verschillende services kunt orkestreren en beheren.

### Kernconcepten van Kubernetes:

- **Pods**: De kleinste eenheid in Kubernetes die een of meerdere containers bevat. Pods draaien op nodes in een cluster.
- **Nodes**: Fysieke of virtuele machines waarop containers draaien. Een Kubernetes-cluster bestaat uit meerdere nodes.
- **Cluster**: Een verzameling nodes beheerd door Kubernetes, waarin je je gecontaineriseerde applicaties kunt draaien.
- **Deployment**: Een object dat ervoor zorgt dat je applicaties in een bepaalde staat blijven, door pods te schalen en up-to-date te houden.
- **Service**: Een abstractie die een stabiel netwerk-IP biedt om toegang te krijgen tot een set pods.
- **Namespace**: Een mechanisme voor logische scheiding in een cluster, zodat meerdere teams of projecten resources kunnen delen.

## Hoe gebruik je Kubernetes?

### 1. Installatie van Kubernetes
Je kunt Kubernetes lokaal installeren met tools zoals Minikube of in de cloud met platforms als Google Kubernetes Engine (GKE), Amazon Elastic Kubernetes Service (EKS) of Microsoft Azure Kubernetes Service (AKS).

### 2. Containerizen van Applicaties
Gebruik containertechnologieën zoals Docker om je applicaties in containers te plaatsen. Een container bevat de code, afhankelijkheden en configuraties die nodig zijn om de applicatie uit te voeren.

### 3. Het creëren van Kubernetes-configuratiebestanden
Kubernetes gebruikt YAML-bestanden om de gewenste toestand van je applicaties te definiëren.

## Opdracht

Bekijk volgende [video](https://www.youtube.com/watch?v=s_o8dwzRlu4&t=5s) om de basis te leren en vertrokken te raken met Minicube en K8S. Volgende les breiden we dit uit om een cluster te maken van echte servers en je eigen applicaties er op te installeren.

## Een eigen cluster aanmaken

### Prerequisites
We hebben 2 of meerdere pc's nodig waar we ssh toegang tot hebben. Op beide pc's moeten docker geïnstalleerd zijn. Daarna installeren we kubernetes op beide pc's: zie de officiële [documentatie](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl) hiervoor. We hebben ook volgende package nodig: `sudo apt install kubernetes-cni -y`.
```bash
sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip that package
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
# If the directory `/etc/apt/keyrings` does not exist, it should be created before the curl command, read the note below.
# sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
# This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt install kubernetes-cni -y
```

#### Configure Containerd
```bash
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd
```

### Finally starting
We gaan nu de cluster beginnen bouwen: 
Op de master: `sudo kubeadm init` en sla het join-commando dat verschijnt in de output op zodat we dit kunnen gebruiken om onze ander pc als workernode toe te voegen aan de cluster. Dit kan even duren aangezien dit commando de eerste keer ook een image moet downloaden.

Voorbeeld:
```bash
kubeadm join 192.168.1.118:6443 --token rjh5kb.xblms76erx48rxy9 \
        --discovery-token-ca-cert-hash sha256:bc985d257e40951df77d17c4d9469d7254b77c2d1ec15b4e284aec0569d7ab12
```

We kunnen op de master dan onze nodes bekijken met `kubectl get nodes`. Je zal echter een error krijgen van `Connection on socket refused`.
Om dit op te lossen moeten we nog een aantal cofiguration files aanmaken:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl get nodes
```

Je krijgt te zien dat de nodes voorlopig nog status `NotReady` hebben.
Als laatste stap moeten we container networking nog initialiseren.

We gaan hiervoor Calico gebruiken:
```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/refs/heads/master/manifests/calico.yaml
```

Nu is onze cluster klaar voor gebruik.

Als we naar het voorbeeld uit de video kijken kunnen we onze applicatie starten met:
```bash
kubectl apply -f mongo-config.yaml
kubectl apply -f mongo-secret.yaml
kubectl apply -f mongo.yaml
kubectl apply -f webapp.yaml
kubectl get svc
kubectl get node -o wide
# info
kubectl get all
kubectl describe service <servicename>
kubectl describe pod <podname>
```


## Moeilijkheden met Kubernetes

Het is moeilijk om over verschillende database pods een identieke state te garanderen. Daarom is het soms nuttig om de databases extern te beheren en via api calls je applicatie de juiste data te laten ophalen.
Tegenwoordig bevatten hosted database solutions simpele methoden om backups en redundantie te voorzien. Dit moet je dan niet specifiek in Kubernetes opstellen. (Het is wel mogelijk dit op te stellen in Kubernetes!)