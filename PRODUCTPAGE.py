# Productpage services

apiVersion: v1
kind: Service
metadata:
  name: productpage
  labels:
    app: productpage
    service: productpage
spec:
  ports:
  - port: 9080
    name: http
  selector:
    app: productpage
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: bookinfo-productpage
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: productpage-v1
  labels:
    app: productpage
    version: v1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: productpage
      version: v1
  template:
    metadata:
      labels:
        app: productpage
        version: v1
    spec:
      serviceAccountName: bookinfo-productpage
      containers:
      - name: productpage
        image: docker.io/istio/examples-bookinfo-productpage-v1:1.15.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 9080
---
apiVersion: extensions/v1
kind: Deployment
metadata: 
  name: nginx-ingress-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
      args:
        - /nginx-ingress-controller
        - --configmap=$(POD_REVIEWS)/nginx-oconfiguration
      env:
        - name: POD_REVIEW
          valueFrom:
            fieldRef:
              fieldPath: metadata.productpage
        - name: POD_REVIEW
          valueFrom:
            fieldPath: metadata.productpage
      ports:
        - name: http
          containerPort: 9080
        - name: https
          containerPort: 443
apiVersion: v1
kind: service
metadata: 
  name: nginx-ingress
spec:
  type: NodePort
  ports:
  - port: 9080
    targetPort: 9080
    protocol: TCP
    name: http
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
  selector:
    name:nginx-ingress
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount

kind: ConfigMap
apiVersion:v1
metadata:
  name: nginx-configuration
-