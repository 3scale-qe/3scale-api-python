#!/bin/bash

echo "#!/bin/bash" > exports.sh
chmod u+x exports.sh

# namespace with 3scale

NAMESPACE="$(oc project -q)"
if [ $# -gt 0 ]; then
  NAMESPACE=$1
fi

# Tenant

SEC_NAME="threescale-provider-account-${RANDOM}"
DOMAIN="https://$(oc get route --namespace=${NAMESPACE} | grep 3scale-admin | awk '{print $2}')"
TOKEN="$(oc get secret system-seed --namespace=${NAMESPACE} -o go-template --template="{{.data.ADMIN_ACCESS_TOKEN|base64decode}}")"

echo "curl -X POST "${DOMAIN}/admin/api/personal/access_tokens.json" -d 'name=hu&permission=rw&scopes%5B%5D=finance&scopes%5B%5D=stats&scopes%5B%5D=account_management&scopes%5B%5D=policy_registry&access_token=${TOKEN}' -k | jq -r .access_token.value"

ACCESS_TOKEN="$(curl -X POST "${DOMAIN}/admin/api/personal/access_tokens.json" -d "name=hu&permission=rw&scopes%5B%5D=finance&scopes%5B%5D=stats&scopes%5B%5D=account_management&scopes%5B%5D=policy_registry&access_token=${TOKEN}" -k | jq -r .access_token.value)"

echo "Create secret with ${DOMAIN} ${ACCESS_TOKEN}"

oc create secret generic ${SEC_NAME} --from-literal="adminURL=${DOMAIN}" --from-literal="token=${ACCESS_TOKEN}"

echo "export THREESCALE_PROVIDER_URL=\"${DOMAIN}\"" >> exports.sh
echo "export THREESCALE_PROVIDER_TOKEN=\"${ACCESS_TOKEN}\"" >> exports.sh
echo "export OCP_PROVIDER_ACCOUNT_REF=\"${SEC_NAME}\"" >> exports.sh

# Master

SEC_NAME="threescale-master-account-${RANDOM}"

DOMAIN="https://$(oc get route --namespace=${NAMESPACE} | grep master | awk '{print $2}')"

TOKEN="$(oc get secret system-seed --namespace=${NAMESPACE} -o go-template --template="{{.data.MASTER_ACCESS_TOKEN|base64decode}}")"

echo "curl -X POST "${DOMAIN}/admin/api/personal/access_tokens.json" -d 'name=hu&permission=rw&scopes%5B%5D=stats&scopes%5B%5D=account_management&scopes%5B%5D=policy_registry&access_token=${TOKEN}' -k | jq -r .access_token.value"
ACCESS_TOKEN="$(curl -X POST "${DOMAIN}/admin/api/personal/access_tokens.json" -d "name=hu&permission=rw&scopes%5B%5D=stats&scopes%5B%5D=account_management&scopes%5B%5D=policy_registry&access_token=${TOKEN}" -k | jq -r .access_token.value)"

echo "Create master secret with ${DOMAIN} ${ACCESS_TOKEN}"

oc create secret generic ${SEC_NAME} --from-literal="MASTER_ACCESS_TOKEN=${ACCESS_TOKEN}"

echo "export THREESCALE_MASTER_URL=\"${DOMAIN}\"" >> exports.sh
echo "export THREESCALE_MASTER_TOKEN=\"${ACCESS_TOKEN}\"" >> exports.sh
