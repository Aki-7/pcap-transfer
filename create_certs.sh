SERVER_HOSTNAME="localhost"

confirm () {
  # return    # uncomment me if you don't want to type "y" anymore
  read -p "ok? (y/N): " yn
  case "$yn" in
    [yY]*) ;;
    *) exit;;
  esac
}

echo_and_exec () {
  echo "$ $1"
  eval $1
}

divider () {
  echo "\n* --------- *\n"
}

cd `dirname $0`

# Private 認証局のための秘密鍵の作成

CRT_DIR="$(pwd)/certs"

CA_SECKEY_PATH="${CRT_DIR}/ca.pem"
echo "認証局の秘密鍵を以下に作成します"
echo $CA_SECKEY_PATH
confirm
echo_and_exec "openssl genrsa -aes256 -out ${CA_SECKEY_PATH} -passout file:passwd 2048"
divider

CA_CSR_PATH="${CRT_DIR}/ca.csr"
echo "Root証明証発行要求ファイルを以下に作成します"
echo $CA_CSR_PATH
confirm
echo_and_exec "openssl req -new -key ${CA_SECKEY_PATH} -passin file:passwd -out ${CA_CSR_PATH} -subj '/CN=elab-root-cert-dev'"
divider

CA_CERT_PATH="${CRT_DIR}/ca.crt.pem"
echo "Root証明証を以下に発行します"
echo $CA_CERT_PATH
confirm
echo_and_exec "openssl x509 -days 365 -in ${CA_CSR_PATH} -passin file:passwd -req -signkey ${CA_SECKEY_PATH} -out ${CA_CERT_PATH}"
divider

SERVER_SECKEY_PATH="${CRT_DIR}/svr.pem"
echo "サーバーの秘密鍵を以下に作成します"
echo $SERVER_SECKEY_PATH
confirm
echo_and_exec "openssl genrsa -aes256 -out ${SERVER_SECKEY_PATH} -passout file:passwd 2048"
divider

SERVER_CSR_PATH="${CRT_DIR}/svr.csr"
echo "サーバー証明証発行要求ファイルを以下に作成します"
echo $SERVER_CSR_PATH
confirm
echo_and_exec "openssl req -new -key ${SERVER_SECKEY_PATH} -passin file:passwd -out ${SERVER_CSR_PATH} -subj '/CN=${SERVER_HOSTNAME}'"
divider

SERVER_CERT_PATH="${CRT_DIR}/svr.crt.pem"
echo "サーバー証明証を以下に発行します"
echo $SERVER_CERT_PATH
confirm
echo_and_exec "openssl x509 -req -in ${SERVER_CSR_PATH} -passin file:passwd -CA ${CA_CERT_PATH} -CAkey ${CA_SECKEY_PATH} -CAcreateserial -days 30 -out ${SERVER_CERT_PATH}"
divider

CLIENT_SECKEY_PATH="${CRT_DIR}/clt.pem"
echo "クライアントの秘密鍵を以下に作成します"
echo $CLIENT_SECKEY_PATH
confirm
echo_and_exec "openssl genrsa -aes256 -out ${CLIENT_SECKEY_PATH} -passout file:passwd 2048"
divider

CLIENT_CSR_PATH="${CRT_DIR}/clt.csr"
echo "クライアント証明証発行要求ファイルを以下に作成します"
echo $CLIENT_CSR_PATH
confirm
echo_and_exec "openssl req -new -key ${CLIENT_SECKEY_PATH} -passin file:passwd -out ${CLIENT_CSR_PATH} -subj '/CN=google.com'"
divider

CLIENT_CERT_PATH="${CRT_DIR}/clt.crt.pem"
echo "クライアント証明証を以下に発行します"
echo $CLIENT_CERT_PATH
confirm
echo_and_exec "openssl x509 -req -in ${CLIENT_CSR_PATH} -passin file:passwd -CA ${CA_CERT_PATH} -CAkey ${CA_SECKEY_PATH} -CAcreateserial -days 30 -out ${CLIENT_CERT_PATH}"
divider

DUMMY_SECKEY_PATH="${CRT_DIR}/dmy.pem"
echo "ダミー認証局の秘密鍵を以下に作成します"
echo $DUMMY_SECKEY_PATH
confirm
echo_and_exec "openssl genrsa -aes256 -out ${DUMMY_SECKEY_PATH} -passout file:passwd 2048"
divider

DUMMY_CSR_PATH="${CRT_DIR}/dmy.csr"
echo "ダミー自己証明証発行要求ファイルを以下に作成します"
echo $DUMMY_CSR_PATH
confirm
echo_and_exec "openssl req -new -key ${DUMMY_SECKEY_PATH} -passin file:passwd -out ${DUMMY_CSR_PATH} -subj '/CN=localhost'"
divider

DUMMY_CERT_PATH="${CRT_DIR}/dmy.crt.pem"
echo "ダミー自己証明証を以下に発行します"
echo $DUMMY_CERT_PATH
confirm
echo_and_exec "openssl x509 -days 365 -in ${DUMMY_CSR_PATH} -passin file:passwd -req -signkey ${DUMMY_SECKEY_PATH} -out ${DUMMY_CERT_PATH}"
divider

SERVER_CHAIN_PATH="${CRT_DIR}/svr.chain.pem"
echo "サーバーの証明書チェインを以下に作成します。"
echo $SERVER_CHAIN_PATH
confirm
echo_and_exec "cat ${SERVER_CERT_PATH} > ${SERVER_CHAIN_PATH}; cat ${CA_CERT_PATH} >> ${SERVER_CHAIN_PATH}"
divider

CLIENT_CHAIN_PATH="${CRT_DIR}/clt.chain.pem"
echo "クライアントの証明書チェインを以下に作成します。"
echo $CLIENT_CHAIN_PATH
confirm
echo_and_exec "cat ${CLIENT_CERT_PATH} > ${CLIENT_CHAIN_PATH}; cat ${CA_CERT_PATH} >> ${CLIENT_CHAIN_PATH}"
divider
