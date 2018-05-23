from flask import Flask, jsonify, request
import json
import base64
from npre import bbs98

app = Flask(__name__)

@app.route('/reencrypt/<string:msg>', methods=['PUT'])

def update_task(msg):

    data={}

    pre = bbs98.PRE()

    sk_Alice = pre.gen_priv(dtype=bytes)
    sk_Alice = pre.gen_priv(dtype=bytes)
    pk_Alice = pre.priv2pub(sk_Alice)
    sk_Bob = pre.gen_priv(dtype=bytes)
    pk_Bob = pre.priv2pub(sk_Bob)
    sk_Aux = pre.gen_priv(dtype=bytes)
    re_AliceAux = pre.rekey(sk_Alice, sk_Aux)

    emsg = pre.encrypt(pk_Alice, msg)

    emsg_Aux = pre.reencrypt(re_AliceAux, emsg) # Mensaje encriptado para Bob
    e_Aux = pre.encrypt(pk_Bob, sk_Aux)

    bob_Aux = pre.decrypt(sk_Bob, e_Aux)
    msgFinal = pre.decrypt(bob_Aux, emsg_Aux).decode('UTF-8')
    #encoded = base64.encodestring(msgFinalB)
    #msgFinal = encoded.decode('ascii')

    return jsonify({'task': msgFinal})

@app.route('/')
def hello():
    return '\nHello World! times\n' 
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)