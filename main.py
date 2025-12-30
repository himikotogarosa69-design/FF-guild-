import threading
import jwt
import random
from threading import Thread
import json
import requests
import google.protobuf
from protobuf_decoder.protobuf_decoder import Parser
import datetime
from google.protobuf.json_format import MessageToJson
import my_message_pb2
import data_pb2
import base64
import logging
import re
import socket
from google.protobuf.timestamp_pb2 import Timestamp
import jwt_generator_pb2
import os
import binascii
import sys
import psutil
import MajorLoginRes_pb2
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import urllib3
from important_zitado import *
from byte import *

# Global flags / state (kept from original)
tempid = None
sent_inv = False
start_par = False
pleaseaccept = False
nameinv = "none"
idinv = 0
senthi = False
statusinfo = False
tempdata1 = None
tempdata = None
leaveee = False
leaveee1 = False
data22 = None
isroom = False
isroom2 = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Helper functions
def encrypt_packet(plain_text, key, iv):
    # Ensure data is bytes
    if isinstance(plain_text, str):
        data = plain_text.encode('utf-8')
    elif isinstance(plain_text, bytes):
        data = plain_text
    else:
        data = str(plain_text).encode('utf-8')

    # Convert key and iv from hex string → bytes if needed
    if isinstance(key, str):
        try:
            key = bytes.fromhex(key)
        except ValueError:
            key = key.encode('utf-8')

    if isinstance(iv, str):
        try:
            iv = bytes.fromhex(iv)
        except ValueError:
            iv = iv.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(data, AES.block_size))
    return cipher_text.hex()

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def gethashteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['7']

def getownteam(hexxx):
    a = zitado_get_proto(hexxx)
    if not a:
        raise ValueError("Invalid hex format or empty response from zitado_get_proto")
    data = json.loads(a)
    return data['5']['1']

def generate_random_color():
    color_list = [
        "[00FF00][b][c]", "[FFDD00][b][c]", "[3813F3][b][c]", "[FF0000][b][c]",
        "[0000FF][b][c]", "[FFA500][b][c]", "[DF07F8][b][c]", "[11EAFD][b][c]",
        "[DCE775][b][c]", "[A8E6CF][b][c]", "[7CB342][b][c]", "[FF0000][b][c]",
        "[FFB300][b][c]", "[90EE90][b][c]"
    ]
    return random.choice(color_list)

def fix_num(num):
    fixed = ""
    count = 0
    num_str = str(num)
    for char in num_str:
        if char.isdigit():
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0
    return fixed

def fix_word(num):
    fixed = ""
    count = 0
    for char in num:
        if char:
            count += 1
        fixed += char
        if count == 3:
            fixed += "[c]"
            count = 0
    return fixed

def check_banned_status(player_id):
    url = f"http://mossa-api.vercel.app/check_banned?player_id={player_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def encode_varint(number):
    encoded_bytes = []
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes).hex()

def get_random_avatar():
    avatar_list = [
        '902000061', '902000060', '902000064', '902000065', '902000066',
        '902000074', '902000075', '902000077', '902000078', '902000084',
        '902000085', '902000087', '902000091', '902000094', '902000306',
        '902000091', '902000208', '902000209', '902000210', '902000211',
        '902047016', '902047016', '902000347'
    ]
    return random.choice(avatar_list)

def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
    return final_result

def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        # Return None and log error so callers can check for it
        logging.debug(f"get_available_room parse error: {e}")
        return None

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def encrypt_message(plaintext):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(encrypted_message).decode('utf-8')

def extract_jwt_from_hex(hexin):
    byte_data = binascii.unhexlify(hexin)
    message = jwt_generator_pb2.Garena_420()
    message.ParseFromString(byte_data)
    json_output = MessageToJson(message)
    token_data = json.loads(json_output)
    return token_data

def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def restart_program():
    try:
        p = psutil.Process(os.getpid())
        try:
            open_files = p.open_files()
        except Exception:
            open_files = []

        # Attempt to get network connections but skip if permission denied
        try:
            connections = psutil.net_connections()
        except Exception as e:
            logging.warning(f"[WARN] Unable to get network connections: {e}")
            connections = []

        # Safely close open file descriptors
        for handler in open_files:
            try:
                os.close(handler.fd)
            except Exception:
                pass

    except Exception as e:
        logging.warning(f"[WARN] restart_program encountered an error: {e}")

    logging.info("[INFO] Restarting program...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Single, full-featured FF_CLIENT class (fixed references to self.key/self.iv and other issues)
class FF_CLIENT(threading.Thread):
    def __init__(self, id, password):
        super().__init__()
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        self.g_token = None
        # do not call get_tok here synchronously (start() will call run) — you can call it here if desired
        # self.get_tok()

    # central parser for MajorLoginRes
    def parse_my_message(self, serialized_data):
        try:
            MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
            MajorLogRes.ParseFromString(serialized_data)

            key = MajorLogRes.ak
            iv = MajorLogRes.aiv
            combined_timestamp = getattr(MajorLogRes, "timestamp", 0)
            BASE64_TOKEN = getattr(MajorLogRes, "token", "")

            if isinstance(key, bytes):
                key = key.hex()
            if isinstance(iv, bytes):
                iv = iv.hex()

            self.key = key
            self.iv = iv
            logging.debug(f"Key: {self.key} | IV: {self.iv}")
            return combined_timestamp, self.key, self.iv, BASE64_TOKEN

        except Exception as e:
            logging.error(f"Error parsing message: {e}")
            return 0, None, None, ""

    # encrypt helper using instance key/iv
    def nmnmmmmn(self, data):
        try:
            key = self.key if isinstance(self.key, bytes) else bytes.fromhex(self.key)
            iv = self.iv if isinstance(self.iv, bytes) else bytes.fromhex(self.iv)
            data_bytes = bytes.fromhex(data)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = cipher.encrypt(pad(data_bytes, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            logging.error(f"Error in nmnmmmmn: {e}")
            return ""

    # many packet-building methods must use self.key / self.iv when calling encrypt_packet or nmnmmmmn
    def _build_with_header(self, packet_hex, header_prefix):
        """Utility to build final packet bytes given packet hex and header prefix"""
        if not self.key or not self.iv:
            raise RuntimeError("Key/IV not set")
        header_length = len(encrypt_packet(packet_hex, self.key, self.iv)) // 2
        header_length_final = dec_to_hex(header_length)
        # prefix + header_length_final may need zero padding depending on expected length, keep behavior similar to original
        # choose prefix combined with header length
        # Normalize header length field to variable width previously done ad-hoc — keep simpler: always append header_length_final
        final_packet_hex = f"{header_prefix}{header_length_final}{self.nmnmmmmn(packet_hex)}"
        try:
            return bytes.fromhex(final_packet_hex)
        except Exception as e:
            logging.error(f"Failed to construct packet hex: {e}")
            return b""

    def spam_room(self, idroom, idplayer):
        fields = {
            1: 78,
            2: {
                1: int(idroom),
                2: "[C][B]VNXR[FF0000]TEAM",
                4: 330,
                5: 6000,
                6: 201,
                10: int(get_random_avatar()),
                11: int(idplayer),
                12: 1
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0E15000000")

    def send_squad(self, idplayer):
        fields = {
            1: 33,
            2: {
                1: int(idplayer),
                2: "IND",
                3: 1,
                4: 1,
                7: 330,
                8: 19459,
                9: 100,
                12: 1,
                16: 1,
                17: {
                    2: 94,
                    6: 11,
                    8: "1.109.5",
                    9: 3,
                    10: 2
                },
                18: 201,
                23: {
                    2: 1,
                    3: 1
                },
                24: int(get_random_avatar()),
                26: {},
                28: {}
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def start_autooo(self):
        fields = {
            1: 9,
            2: {
                1: 11371687918
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def invite_skwad(self, idplayer):
        fields = {
            1: 2,
            2: {
                1: int(idplayer),
                2: "IND",
                4: 1
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def request_skwad(self, idplayer):
        # same as send_squad in original
        return self.send_squad(idplayer)

    def skwad_maker(self):
        fields = {
            1: 1,
            2: {
                2: "\u0001",
                3: 1,
                4: 1,
                5: "en",
                9: 1,
                11: 1,
                13: 1,
                14: {
                    2: 5756,
                    6: 11,
                    8: "1.109.5",
                    9: 3,
                    10: 2
                },
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def changes(self, num):
        fields = {
            1: 17,
            2: {
                1: 11371687918,
                2: 1,
                3: int(num),
                4: 62,
                5: "\u001a",
                8: 5,
                13: 329
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def leave_s(self):
        fields = {
            1: 7,
            2: {
                1: 11371687918
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def leave_room(self, idroom):
        fields = {
            1: 6,
            2: {
                1: int(idroom)
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0E15000000")

    def stauts_infoo(self, idd):
        fields = {
            1: 7,
            2: {
                1: 11371687918
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def GenResponsMsg(self, Msg, Enc_Id):
        fields = {
            1: 1,
            2: {
                1: 12947146032,
                2: Enc_Id,
                3: 2,
                4: str(Msg),
                5: int(datetime.datetime.now().timestamp()),
                7: 2,
                9: {
                    1: "mossa",
                    2: int(get_random_avatar()),
                    3: 901049014,
                    4: 330,
                    5: int(get_random_avatar()),
                    8: "GUILD|Friend",
                    10: 1,
                    11: random.choice([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
                    13: {
                        1: 2,
                        2: 1,
                    },
                    14: {
                        1: 11017917409,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    }
                },
                10: "IND",
                13: {
                    1: "https://graph.facebook.com/v9.0/253082355523299/picture?width=160&height=160",
                    2: 1,
                    3: 1
                },
                14: {
                    1: {
                        1: random.choice([1, 4]),
                        2: 1,
                        3: random.randint(1, 180),
                        4: 1,
                        5: int(datetime.datetime.now().timestamp()),
                        6: "IND"
                    }
                }
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "1215000000")

    def send_team_message(self, message_text):
        fields = {
            1: 2,
            2: {
                1: 3557944186,
                2: 0,
                3: 1,
                4: str(message_text),
                5: int(datetime.datetime.now().timestamp()),
                9: {
                    2: int(get_random_avatar()),
                    3: 901041021,
                    4: 330,
                    10: 1,
                    11: 155
                },
                10: "en",
                13: {
                    1: "https://graph.facebook.com/v9.0/104076471965380/picture?width=160&height=160",
                    2: 1,
                    3: 1
                }
            },
            14: ""
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "1315000000")

    def createpacketinfo(self, idddd):
        ida = Encrypt(idddd)
        packet = f"080112090A05{ida}1005"
        return self._build_with_header(packet, "0F15000000")

    def accept_sq(self, hashteam, idplayer, ownerr):
        fields = {
            1: 4,
            2: {
                1: int(ownerr),
                3: int(idplayer),
                4: "\u0001\u0007\t\n\u0012\u0019\u001a ",
                8: 1,
                9: {
                    2: 1393,
                    4: "mossa",
                    6: 11,
                    8: "1.109.5",
                    9: 3,
                    10: 2
                },
                10: hashteam,
                12: 1,
                13: "en",
                16: "OR"
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0515000000")

    def info_room(self, idrooom):
        fields = {
            1: 1,
            2: {
                1: int(idrooom),
                3: {},
                4: 1,
                6: "en"
            }
        }
        packet = create_protobuf_packet(fields).hex()
        return self._build_with_header(packet, "0E15000000")

    def sockf1(self, tok, online_ip, online_port, packet, key, iv):
        global socket_client, sent_inv, tempid, start_par, clients, pleaseaccept
        global tempdata1, nameinv, idinv, senthi, statusinfo, tempdata, data22, leaveee, isroom, isroom2

        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socket_client.connect((online_ip, int(online_port)))
        except Exception as e:
            logging.error(f"sockf1 connect error: {e}")
            return

        logging.info(f"Connected to online host {online_ip}:{online_port}")
        try:
            socket_client.send(bytes.fromhex(tok))
        except Exception as e:
            logging.error(f"sockf1 send tok error: {e}")
            return

        while True:
            try:
                data2 = socket_client.recv(9999)
            except Exception as e:
                logging.error(f"sockf1 recv error: {e}")
                break

            if not data2:
                logging.info("Connection closed by remote host")
                break

            logging.debug(f"Received (sockf1) {len(data2)} bytes")
            hexprefix = data2.hex()[:4]
            # handle different packet types defensively
            try:
                if "0500" in hexprefix:
                    accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(accept_packet)
                    if kk:
                        parsed_data = json.loads(kk)
                        fark = parsed_data.get("4", {}).get("data", None)
                        if fark is not None:
                            if fark == 18:
                                if sent_inv:
                                    aa = gethashteam(accept_packet)
                                    ownerid = getownteam(accept_packet)
                                    ss = self.accept_sq(aa, tempid, int(ownerid))
                                    socket_client.send(ss)
                                    sleep(1)
                                    startauto = self.start_autooo()
                                    socket_client.send(startauto)
                                    start_par = False
                                    sent_inv = False
                            elif fark == 6:
                                leaveee = True
                            elif fark == 50:
                                pleaseaccept = True

                if "0600" in hexprefix and len(data2.hex()) > 700:
                    accept_packet = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(accept_packet)
                    if kk:
                        parsed_data = json.loads(kk)
                        idinv = parsed_data["5"]["data"]["1"]["data"]
                        nameinv = parsed_data["5"]["data"]["3"]["data"]
                        senthi = True

                if "0f00" in hexprefix:
                    packett = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(packett)
                    if kk:
                        parsed_data = json.loads(kk)
                        asdj = parsed_data.get("2", {}).get("data")
                        tempdata_local = get_player_status(packett)
                        if asdj == 15:
                            if tempdata_local == "OFFLINE":
                                tempdata_local = f"The id is {tempdata_local}"
                            else:
                                idplayer = parsed_data["5"]["data"]["1"]["data"]["1"]["data"]
                                idplayer1 = fix_num(idplayer)
                                if tempdata_local == "IN ROOM":
                                    idrooom = get_idroom_by_idplayer(packett)
                                    idrooom1 = fix_num(idrooom)
                                    tempdata_local = f"id : {idplayer1}\nstatus : {tempdata_local}\nid room : {idrooom1}"
                                    data22 = packett
                                elif "INSQUAD" in tempdata_local:
                                    idleader = get_leader(packett)
                                    idleader1 = fix_num(idleader)
                                    tempdata_local = f"id : {idplayer1}\nstatus : {tempdata_local}\nleader id : {idleader1}"
                                else:
                                    tempdata_local = f"id : {idplayer1}\nstatus : {tempdata_local}"
                            statusinfo = True
                            tempdata = tempdata_local

                if "0e00" in hexprefix:
                    packett = f'08{data2.hex().split("08", 1)[1]}'
                    kk = get_available_room(packett)
                    if kk:
                        parsed_data = json.loads(kk)
                        asdj = parsed_data.get("2", {}).get("data")
                        if asdj == 14:
                            nameroom = parsed_data["5"]["data"]["1"]["data"]["2"]["data"]
                            maxplayer = parsed_data["5"]["data"]["1"]["data"]["7"]["data"]
                            nowplayer = parsed_data["5"]["data"]["1"]["data"]["6"]["data"]
                            tempdata1 = f"{tempdata}\nRoom name : {nameroom}\nMax player : {fix_num(maxplayer)}\nLive player : {fix_num(nowplayer)}"
            except Exception as e:
                logging.debug(f"Error processing socket data in sockf1: {e}")
                continue

    def connect(self, tok, packet, key, iv, whisper_ip, whisper_port, online_ip, online_port):
        global clients, socket_client, threads
        clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clients.connect((whisper_ip, int(whisper_port)))
            clients.send(bytes.fromhex(tok))
        except Exception as e:
            logging.error(f"connect() whisper connect/send failed: {e}")
            return

        # spawn sockf1 thread to handle the online socket
        thread = threading.Thread(
            target=self.sockf1, args=(tok, online_ip, online_port, "anything", key, iv)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

        while True:
            try:
                data = clients.recv(9999)
            except Exception as e:
                logging.error(f"clients.recv error: {e}")
                break

            if not data:
                logging.info("Connection closed by remote host (whisper)")
                break

            # handle /glori command parsing carefully
            if b"/glori" in data and data.hex().startswith("1200"):
                kk = get_available_room(data.hex()[10:])
                if not kk:
                    continue
                try:
                    parsed_data = json.loads(kk)
                    uid = parsed_data["5"]["data"]["1"]["data"]
                except Exception:
                    continue

                # parse player id from the raw bytes data string safely
                try:
                    text = data.decode(errors='ignore')
                    parts = re.split(r"/glori\s+", text)
                    if len(parts) < 2:
                        continue
                    player_id = parts[1].split()[0]
                    # remove masking like "***" -> replace with something logical if needed
                    player_id = player_id.replace("***", "106")
                    if not player_id.isdigit():
                        clients.send(self.GenResponsMsg(f"[C][B][FF0000]Enter /glori [uid_clan] 15", uid))
                        continue

                    # send spam invites in background thread to avoid blocking
                    def send_spam_invite():
                        try:
                            for i in range(50):
                                invskwad = self.request_skwad(player_id)
                                # ensure socket_client is available
                                try:
                                    socket_client.send(invskwad)
                                except Exception as e:
                                    logging.error(f"send_spam_invite send error: {e}")
                                    break
                                time.sleep(0.1)
                                if (i + 1) % 10 == 0:
                                    clients.send(self.GenResponsMsg(f"[C][B][00FF00]✅ Sent {i+1} Request", uid))
                            logging.info(f"Finished spam invites to {player_id}")
                        except Exception as e:
                            logging.error(f"Error sending join requests: {e}")
                            clients.send(self.GenResponsMsg(f"[C][B][FF0000]❌ An error occurred while sending.", uid))

                    Thread(target=send_spam_invite, daemon=True).start()
                except Exception as e:
                    logging.error(f"Error in /glori handling: {e}")

    def GET_PAYLOAD_BY_DATA(self, JWT_TOKEN, NEW_ACCESS_TOKEN, date):
        # decode token payload to grab external_id and signature_md5
        token_payload_base64 = JWT_TOKEN.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
        decoded_payload = json.loads(decoded_payload)
        NEW_EXTERNAL_ID = decoded_payload.get('external_id', '')
        SIGNATURE_MD5 = decoded_payload.get('signature_md5', '')
        now = str(datetime.datetime.now())[:len(str(datetime.datetime.now())) - 7]
        payload = bytes.fromhex("1a13323032352d30372d30323031313a30323a3531220966726565206669726528013a07312e3131342e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033")
        payload = payload.replace(b"2025-07-02 11:02:51", str(now).encode())
        payload = payload.replace(b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a", NEW_ACCESS_TOKEN.encode("UTF-8"))
        payload = payload.replace(b"996a629dbcdb3964be6b6978f5d814db", NEW_EXTERNAL_ID.encode("UTF-8"))
        payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
        PAYLOAD = payload.hex()
        PAYLOAD = encrypt_api(PAYLOAD)
        PAYLOAD = bytes.fromhex(PAYLOAD)
        whisper_ip, whisper_port, online_ip, online_port = self.GET_LOGIN_DATA(JWT_TOKEN, PAYLOAD)
        return whisper_ip, whisper_port, online_ip, online_port

    @staticmethod
    def convert_to_hex(PAYLOAD):
        hex_payload = ''.join([f'{byte:02x}' for byte in PAYLOAD])
        return hex_payload

    @staticmethod
    def convert_to_bytes(PAYLOAD):
        payload = bytes.fromhex(PAYLOAD)
        return payload

    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD):
        url = "https://client.ind.freefiremobile.com/GetLoginData"
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'client.ind.freefiremobile.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.post(url, headers=headers, data=PAYLOAD, verify=False)
                response.raise_for_status()
                x = response.content.hex()
                json_result = get_available_room(x)
                if not json_result:
                    raise ValueError("Failed to parse GetLoginData response")
                parsed_data = json.loads(json_result)

                whisper_address = parsed_data['32']['data']
                online_address = parsed_data['14']['data']
                online_ip = online_address[:len(online_address) - 6]
                whisper_ip = whisper_address[:len(whisper_address) - 6]
                online_port = int(online_address[len(online_address) - 5:])
                whisper_port = int(whisper_address[len(whisper_address) - 5:])
                return whisper_ip, whisper_port, online_ip, online_port

            except requests.RequestException as e:
                logging.warning(f"Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Retrying...")
                attempt += 1
                time.sleep(2)
            except Exception as e:
                logging.error(f"GET_LOGIN_DATA parse or other error: {e}")
                return None, None, None, None

        logging.error("Failed to get login data after multiple attempts.")
        return None, None, None, None

    def guest_token(self, uid, password):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
        }
        data = {
            "uid": f"{uid}",
            "password": f"{password}",
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067",
        }
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        NEW_ACCESS_TOKEN = data.get('access_token')
        NEW_OPEN_ID = data.get('open_id')
        OLD_ACCESS_TOKEN = "ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a"
        OLD_OPEN_ID = "996a629dbcdb3964be6b6978f5d814db"
        time.sleep(0.2)
        return self.TOKEN_MAKER(OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, uid)

    def TOKEN_MAKER(self, OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, id):
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.common.ggbluefox.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        data = bytes.fromhex('1a13323032352d30372d30323031313a30323a3531220966726565206669726528013a07312e3131342e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033')
        data = data.replace(OLD_OPEN_ID.encode(), NEW_OPEN_ID.encode())
        data = data.replace(OLD_ACCESS_TOKEN.encode(), NEW_ACCESS_TOKEN.encode())
        d = encrypt_api(data.hex())
        Final_Payload = bytes.fromhex(d)
        URL = "https://loginbp.ggpolarbear.com/MajorLogin"

        try:
            RESPONSE = requests.post(URL, headers=headers, data=Final_Payload, verify=False)
        except Exception as e:
            logging.error(f"TOKEN_MAKER request error: {e}")
            return False

        combined_timestamp, key, iv, BASE64_TOKEN = self.parse_my_message(RESPONSE.content)
        if RESPONSE.status_code == 200 and len(RESPONSE.content) > 10:
            whisper_ip, whisper_port, online_ip, online_port = self.GET_PAYLOAD_BY_DATA(BASE64_TOKEN, NEW_ACCESS_TOKEN, 1)
            self.key = key
            self.iv = iv
            logging.info(f"TOKEN_MAKER got key/iv")
            return (BASE64_TOKEN, key, iv, combined_timestamp, whisper_ip, whisper_port, online_ip, online_port)
        else:
            logging.error("TOKEN_MAKER failed or returned unexpected response")
            return False

    def get_tok(self):
        try:
            token_data = self.guest_token(self.id, self.password)
            if not token_data:
                raise RuntimeError("guest_token failed")
            token, key, iv, Timestamp, whisper_ip, whisper_port, online_ip, online_port = token_data
            self.g_token = token

            # decode token to get account_id
            decoded = jwt.decode(token, options={"verify_signature": False})
            account_id = decoded.get('account_id')
            encoded_acc = hex(account_id)[2:]
            time_hex = dec_to_hex(Timestamp)

            BASE64_TOKEN_ = token.encode()

            head = hex(len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2)[2:]
            length = len(encoded_acc)
            zeros = '00000000'
            if length == 9:
                zeros = '0000000'
            elif length == 8:
                zeros = '00000000'
            elif length == 10:
                zeros = '000000'
            elif length == 7:
                zeros = '000000000'
            else:
                logging.debug('Unexpected length encountered for encoded_acc')

            final_token = f'0115{zeros}{encoded_acc}{time_hex}00000{head}' + encrypt_packet(BASE64_TOKEN_, key, iv)

            logging.info("Final token constructed successfully.")
            self.key = key
            self.iv = iv

            # Connect using the constructed token
            self.connect(final_token, 'anything', key, iv, whisper_ip, whisper_port, online_ip, online_port)
            return final_token, key, iv
        except Exception as e:
            logging.error(f"[ERROR] get_tok failed: {e}")
            return None, None, None

    def run(self):
        # When thread starts, get token & connect
        self.get_tok()

# runner helpers
def run_client(id, password):
    logging.info(f"ID: {id}, Password: {password}")
    client = FF_CLIENT(id, password)
    client.start()

# Example main: try list of credentials until one connects — also prevents invalid except chaining
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    credentials = [
        ("4365164848", "GOKU_ZMNQP_BY_SPIDEERIO_GAMING_WXYIH"),
        ("4365164845", "GOKU_G4APU_BY_SPIDEERIO_GAMING_PCEBW"),
        ("4365164844", "GOKU_KL0YY_BY_SPIDEERIO_GAMING_9006F"),
        ("4365165705", "GOKU_LQXAK_BY_SPIDEERIO_GAMING_K8I9O"),
        ("4365165695", "GOKU_39SP5_BY_SPIDEERIO_GAMING_3K8TK"),
        # add more pairs as desired...
    ]

    threads = []
    for uid, pwd in credentials:
        try:
            client_thread = FF_CLIENT(id=uid, password=pwd)
            client_thread.start()
            threads.append(client_thread)
            # small delay between starting clients
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to start client for {uid}: {e}")

    # Optionally join threads or keep main alive
    # for t in threads:
    #     t.join()