# NuCypher's Proxy Re-Encryption and Umbral

Link to their work (Proxy Re-Encryption): [Proxy Re-Encryption](https://blog.nucypher.com/proxy-re-encryption-playground-in-python-3bc66170b9bf)

Link to their work (Umbral): [Umbral](https://github.com/nucypher/pyUmbral)

## USE CASE

**Proxy Re-Encryption** is an algorithm that allows a message encrypted for User A to be re-encrypted by a proxy so that User B can decrypt it. The fantastic thing about this algorithm is that the act of re-encrypting the message (with a **reencryption key** generated by User A) **never** allows the proxy to see the underlying message, just converts the ciphertextA to ciphertextB directly. This allows messages that are meant for User A, to be transferred and re-encrypted semi-automatically (through a Proxy - which does **not** see the underlying message) for User B without User A having to be online.

**The usual procedure is that User A would have to manually decrypt the ciphertextA with its secret key and encrypt again with User B's public key.**

The following image explains the mechanism that Proxy Re-Encryption uses:

![Proxy Re-Encryption](https://cdn-images-1.medium.com/max/1000/0*yTKUeeuKPu-aIZdw.)


**Umbral** works in basically the same way that Proxy Re-Encryption does, with the important difference that it **splits** the re-encryption key - generated by User A into N fragments, and to correctly decrypt the message, you have to recover at least M fragments (M <= N) - M is chosen at the moment you split the re-encryption key. Doing this, you don't have to trust one single proxy, but instead, you split the responsibility between N proxys and only need M of them to respond with their corresponding fragment for User B to be able to correctly decrypt the message.


To show the capabilities of NuCypher's Re-Encryption and Umbral, 2 Proofs of Concepts (PoC) have been developed.

1. Proxy Re-Encryption
2. Umbral

# Proxy Re-Encryption

The PoC for this concept is a web interface:

