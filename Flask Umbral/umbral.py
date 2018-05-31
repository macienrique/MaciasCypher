from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import base64
from umbral import pre, keys

app = Flask(__name__)
CORS(app)

@app.route('/genKeys', methods=['GET'])
def genKeys():

    data = {}
	
    #Keys of person A
    sk_A = keys.UmbralPrivateKey.gen_key()
    pk_A = sk_A.get_pubkey()
	
    #Keys of person B
    sk_B = keys.UmbralPrivateKey.gen_key()
    pk_B = sk_B.get_pubkey()

    #Guardar parametros en data
    data['sk_A'] = base64.encodestring(sk_A.bn_key.to_bytes()).decode('ascii')
    data['pk_A'] = base64.encodestring(pk_A.to_bytes()).decode('ascii')

    data['sk_B'] = base64.encodestring(sk_B.bn_key.to_bytes()).decode('ascii')
    data['pk_B'] = base64.encodestring(pk_B.to_bytes()).decode('ascii')

    return jsonify(data)

@app.route('/encrypt', methods=['POST'])
def encryptA():

    data = request.get_json()
    resp = {}

    pk_A = data['pk_A']
    msg = data['msg']

    pk_A = base64.b64decode(pk_A)
    pk_A = keys.UmbralPublicKey.from_bytes(pk_A)
    msg = bytes(msg, encoding='ascii')

    emsg, capsule = pre.encrypt(pk_A, msg)

    resp['emsg'] = base64.encodestring(emsg).decode('ascii')
    resp['capsule'] = base64.encodestring(pre.Capsule.to_bytes(capsule)).decode('ascii')

    return jsonify(resp)

@app.route('/umbralize', methods=['POST'])
def umbralize():

    data = request.get_json()
    resp = {}

    sk_A = data['sk_A']
    pk_B = data['pk_B']
    M = data['M']
    N = data['N']

    sk_A = base64.b64decode(sk_A)
    sk_A = keys.UmbralPrivateKey.from_bytes(sk_A)

    pk_B = base64.b64decode(pk_B)
    pk_B = keys.UmbralPublicKey.from_bytes(pk_B)

    kfrags = pre.split_rekey(sk_A, pk_B, M, N)

    bytekfrags = [base64.encodestring(bytes(kfrag)).decode('ascii') for kfrag in kfrags] 

    resp['bytekfrags'] = bytekfrags

    return jsonify(resp)

@app.route('/decrypt', methods=['POST'])
def decrypt():

    data = request.get_json()
    resp = {}

    kfragsSel = data['kfragsSel']
    capsule = data['capsule']
    sk_B = data['sk_B']
    pk_A = data['pk_A']
    emsg = data['emsg']

    kfrags = [pre.KFrag.from_bytes(base64.b64decode(kfrag)) for kfrag in kfragsSel]

    capsule = base64.b64decode(capsule)
    capsule = pre.Capsule.from_bytes(capsule)

    sk_B = base64.b64decode(sk_B)
    sk_B = keys.UmbralPrivateKey.from_bytes(sk_B)

    pk_A = base64.b64decode(pk_A)
    pk_A = keys.UmbralPublicKey.from_bytes(pk_A)

    emsg = base64.b64decode(emsg)

    for kfrag in kfrags:
        cfrag = pre.reencrypt(kfrag, capsule)
        capsule.attach_cfrag(cfrag)

    try:
        omsg = pre.decrypt(emsg, capsule, sk_B, pk_A)
    except:
        omsg = b'No se pudo descifrar el mensaje, se debe elegir mas fragmentos'

    resp['omsg'] = omsg.decode('ascii')

    return jsonify(resp)


@app.route('/')
def PREMacias():
    return '\nPoC of NuCypher\'s Umbral and Proxy Reencryption\n' 
if __name__ == '__main__':
    app.run(host="localhost",debug=True)
