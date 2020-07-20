curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/windows/amd64/kubectl.exe

kubectl version --client

minikube start

minikube status

minikube stop

minikube start

kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.10

kubectl expose deployment hello-minikube --type=NodePort --port=8080

kubectl get pod

kubectl get pod

minikube service hello-minikube --url

http://...

kubectl delete services hello-minikube

kubectl delete deployment hello-minikube

minikube stop

minikube delete

minikube start --kubernetes-version v1.18.0

minikube start --driver=virtualbox

minikube status

kubectl config use-context minikube

minikube dashboard

minikube stop

minikube delete
