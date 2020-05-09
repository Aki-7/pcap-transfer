# Pcap Transfer

## 証明書を用いた安全な通信

今回の通信では自分が配布するRaspberry Piと自分が管理する管理サーバとの通信をTLSを用いてセキュアに行うことを目指す。

### 目的

Rapsberry Pi(Client)と管理サーバー(server)の双方において

- 通信内容が傍受されない(機密性)
- 通信内容が改竄されていないことが確かめられる (完全性)

以上を満たした上でsocketを用いて安全に通信したい。

### TLSを用いた解決

今回は管理サーバが認証局の役割を果たし、Raspberry Piを配布する際にSDカードなどでserverで発行したRoot証明書をダウンロードし、それを用いてTLS socketを作成することで目的を達成する。

### Demo Setup

#### require

`openssl`

#### setup

二つのホスト(server, client)を用意してください
(同一ホストでlocalhostで通信でも大丈夫です。)

```sh
# server

# clone this repository
$ git clone git@github.com:Aki-7/pcap-transfer.git
$ cd pcap-transfer
$ git checkout cert
# 秘密鍵に対するパスワードを設定する(option)
$ vim passwd
# host名を設定する。
$ vim create_certs.sh # 1行目を編集
# 各種証明書などを発行 (certs/にすべて発行します)
$ ./create_certs.sh

# 以下localhost以外から接続する場合。
# server.pyでlistenするホストを"0.0.0.0"に
$ vim server.py # 26行目 "localhost" -> "0.0.0.0"

# firewallを外すのも忘れずに(port 5000)
```

```sh
# client

# clone this repository
$ git clone git@github.com:Aki-7/pcap-transfer.git
$ cd pcap-transfer
$ git checkout cert
# 秘密鍵に対するパスワードを設定する server側の設定と同じにしてください(簡単のためです)
$ vim passwd
$ vim client.sh # 6行目を編集

# host名を設定する。
# クライアントで必要なものをコピー
# 任意の方法でserverホストにある
# - certs/clt.pem
# - certs/clt.chain.pem
# - certs/ca.crt.pem
# をclientホストのcerts/にコピーしてください。

# 実際は配布前にSDカードなどでダウンロードさせるので、
# これらのファイルは改竄される恐れなどなく信用できることになります。
```

### Run

```sh
# server
$ python server.py
```

```sh
# client
$ python client.py
```
