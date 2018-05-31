from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import base64
from npre import bbs98

app = Flask(__name__)
CORS(app)

@app.route('/genKeys', methods=['GET'])
def genKeys():

    data = {}

    pre = bbs98.PRE()
	
	#Keys of person A
    sk_A = pre.gen_priv(dtype=bytes)
    pk_A = pre.priv2pub(sk_A)
	
	#Keys of person B
    sk_B = pre.gen_priv(dtype=bytes)
    pk_B = pre.priv2pub(sk_B)
	
	#Keys Ephimeral
    sk_Eph = pre.gen_priv(dtype=bytes)
	
	#Reencryption Key
    reeK = pre.rekey(sk_A, sk_Eph)

    #Guardar parametros en data
    data['sk_A'] = base64.encodestring(sk_A).decode('ascii')
    data['pk_A'] = base64.encodestring(pk_A).decode('ascii')

    data['sk_B'] = base64.encodestring(sk_B).decode('ascii')
    data['pk_B'] = base64.encodestring(pk_B).decode('ascii')

    data['sk_Eph'] = base64.encodestring(sk_Eph).decode('ascii')
    data['reeK'] = base64.encodestring(reeK).decode('ascii')

    return jsonify(data)


@app.route('/encryptA', methods=['POST'])
def encryptA():

    data = request.get_json()

    pk_A = data['pk_A']
    msg = data['msg']

    pk_A = base64.b64decode(pk_A)

    pre = bbs98.PRE()
    emsg = pre.encrypt(pk_A, msg)
    emsg = base64.encodestring(emsg).decode('ascii')

    return jsonify(emsg)


@app.route('/decrypt', methods=['POST'])
def decryptA():

    data = request.get_json()

    key = data['key']
    emsg = data['emsg']

    key = base64.b64decode(key)
    emsg = base64.b64decode(emsg)

    pre = bbs98.PRE()
    msg = pre.decrypt(key, emsg).decode('ascii')

    return jsonify(msg)


@app.route('/reencrypt', methods=['POST'])
def reencrypt():

    data = request.get_json()
    resp = {}

    emsg = data['emsg']
    reeK = data['reeK']
    pk_B = data['pk_B']
    EphSK = data['EphSK']

    emsg = base64.b64decode(emsg)
    reeK = base64.b64decode(reeK)
    pk_B = base64.b64decode(pk_B)
    EphSK = base64.b64decode(EphSK)

    pre = bbs98.PRE()

    remsg = pre.reencrypt(reeK, emsg)

    BEphPK = pre.encrypt(pk_B, EphSK)

    resp['BEphPK'] = base64.encodestring(BEphPK).decode('ascii')
    resp['remsg'] = base64.encodestring(remsg).decode('ascii')

    return jsonify(resp)


@app.route('/decryptEphKey', methods=['POST'])
def decryptEphKey():

    data = request.get_json()

    sk_B = data['sk_B']
    BEphPK = data['BEphPK']

    sk_B = base64.b64decode(sk_B)
    BEphPK = base64.b64decode(BEphPK)

    pre = bbs98.PRE()

    EphPKDec = pre.decrypt(sk_B, BEphPK)
    EphPKDec = base64.encodestring(EphPKDec).decode('ascii')

    return jsonify(EphPKDec)


@app.route('/')
def PREMacias():
    return '\nPOC for NuCypher\'s Umbral and Proxy Reencryption\n' 
if __name__ == '__main__':
    app.run(host="localhost",debug=True)
