# dappr-azure-service-bus

# aks configuration

```bash
az aks update --resource-group {RESOURCE-GROUP} --name {CLUSTER-NAME} --enable-oidc-issuer --enable-workload-identity
```

# create federated credential

```bash
az identity federated-credential create \
    --name {FEDERATED-IDENTITY-CREDENTIAL} \
    --identity-name {IDENTITY-NAME} \
    --resource-group {RESOURCE-GROUP} \
    --issuer "https://australiaeast.oic.prod-aks.azure.com/56ae9e11-e439-4ee4-a872-3718b0b7df82/89d1125a-aa47-47c8-a90b-55e6b918fe3e/" \
    --subject system:serviceaccount:"default":"svc-dappr" \
    --audience api://AzureADTokenExchange 
```
