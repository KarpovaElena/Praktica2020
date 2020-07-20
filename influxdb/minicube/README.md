curl -LO https://storage.googleapis.com/kubernetes-release/rel..`curl -s https://storage.googleapis.com/kubernetes-release/rel..`/bin/linux/amd64/kubectl

chmod +x ./kubectl

sudo mv ./kubectl /usr/local/bin/kubectl

kubectl version —client

grep -E —color 'vmx|svm' /proc/cpuinfo

curl -Lo minikube https://storage.googleapis.com/minikube/releases/late.. \

sudo mkdir -p /usr/local/bin/

sudo install minikube /usr/local/bin/

minikube start —driver=virtualbox

minikube status

minikube stop

kubectl version -o json

minikube start

kubectl cluster-info

kubectl config view

kubectl get nodes

minikube ssh

exit

minikube addons list

minikube dashboard

minikube stop

minikube delete
