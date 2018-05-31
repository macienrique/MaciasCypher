from cryptography.hazmat.primitives.asymmetric import ec

from umbral._pre import assess_cfrag_correctness, verify_kfrag
from umbral.curvebn import CurveBN
from umbral.config import default_curve, default_params
from umbral.keys import UmbralPublicKey
from umbral.point import Point
from umbral.params import UmbralParameters

from io import BytesIO


class KFrag(object):
    def __init__(self, id, bn_key, point_noninteractive, 
                 point_commitment, point_xcoord, bn_sig1, bn_sig2):
        self._id = id
        self._bn_key = bn_key
        self._point_noninteractive = point_noninteractive
        self._point_commitment = point_commitment
        self._point_xcoord = point_xcoord
        self._bn_sig1 = bn_sig1
        self._bn_sig2 = bn_sig2

    @classmethod
    def get_size(cls, curve: ec.EllipticCurve=None):
        """
        Returns the size (in bytes) of a KFrag given the curve.
        If no curve is provided, it will use the default curve.
        """
        curve = curve if curve is not None else default_curve()
        bn_size = CurveBN.get_size(curve)
        point_size = Point.get_size(curve)

        return (bn_size * 4) + (point_size * 3)

    @classmethod
    def from_bytes(cls, data: bytes, curve: ec.EllipticCurve = None):
        """
        Instantiate a KFrag object from the serialized data.
        """
        curve = curve if curve is not None else default_curve()
        bn_size = CurveBN.get_size(curve)
        point_size = Point.get_size(curve)
        data = BytesIO(data)

        # CurveBNs are the keysize in bytes, Points are compressed and the
        # keysize + 1 bytes long.
        id = data.read(bn_size)
        key = CurveBN.from_bytes(data.read(bn_size), curve)
        ni = Point.from_bytes(data.read(point_size), curve)
        commitment = Point.from_bytes(data.read(point_size), curve)
        xcoord = Point.from_bytes(data.read(point_size), curve)
        sig1 = CurveBN.from_bytes(data.read(bn_size), curve)
        sig2 = CurveBN.from_bytes(data.read(bn_size), curve)

        return cls(id, key, ni, commitment, xcoord, sig1, sig2)

    def to_bytes(self):
        """
        Serialize the KFrag into a bytestring.
        """
        key = self._bn_key.to_bytes()
        ni = self._point_noninteractive.to_bytes()
        commitment = self._point_commitment.to_bytes()
        xcoord = self._point_xcoord.to_bytes()
        sig1 = self._bn_sig1.to_bytes()
        sig2 = self._bn_sig2.to_bytes()

        return self._id + key + ni + commitment + xcoord + sig1 + sig2

    def verify(self, pubkey_a: UmbralPublicKey,
                        pubkey_b: UmbralPublicKey,
                        params: UmbralParameters=None):
        pubkey_a_point = pubkey_a.point_key
        pubkey_b_point = pubkey_b.point_key

        return verify_kfrag(self, pubkey_a_point, pubkey_b_point, params)

    def __bytes__(self):
        return self.to_bytes()


class CorrectnessProof(object):
    def __init__(self, point_e2, point_v2, point_kfrag_commitment, 
                 point_kfrag_pok, bn_kfrag_sig1, bn_kfrag_sig2, bn_sig, 
                 metadata:bytes=None):
        self._point_e2 = point_e2
        self._point_v2 = point_v2
        self._point_kfrag_commitment = point_kfrag_commitment
        self._point_kfrag_pok = point_kfrag_pok
        self._bn_kfrag_sig1 = bn_kfrag_sig1
        self._bn_kfrag_sig2 = bn_kfrag_sig2
        self._bn_sig = bn_sig
        self.metadata = metadata

    @classmethod
    def get_size(cls, curve: ec.EllipticCurve=None):
        """
        Returns the size (in bytes) of a CorrectnessProof without the metadata.
        If no curve is given, it will use the default curve.
        """
        curve = curve if curve is not None else default_curve()
        bn_size = CurveBN.get_size(curve=curve)
        point_size = Point.get_size(curve=curve)

        return (bn_size * 3) + (point_size * 4)

    @classmethod
    def from_bytes(cls, data: bytes, curve: ec.EllipticCurve=None):
        """
        Instantiate CorrectnessProof from serialized data.
        """
        curve = curve if curve is not None else default_curve()
        bn_size = CurveBN.get_size(curve)
        point_size = Point.get_size(curve)
        data = BytesIO(data)

        # CurveBNs are the keysize in bytes, Points are compressed and the
        # keysize + 1 bytes long.
        e2 = Point.from_bytes(data.read(point_size), curve)
        v2 = Point.from_bytes(data.read(point_size), curve)
        kfrag_commitment = Point.from_bytes(data.read(point_size), curve)
        kfrag_pok = Point.from_bytes(data.read(point_size), curve)
        kfrag_sig1 = CurveBN.from_bytes(data.read(bn_size), curve)
        kfrag_sig2 = CurveBN.from_bytes(data.read(bn_size), curve)
        sig = CurveBN.from_bytes(data.read(bn_size), curve)

        metadata = data.read() or None

        return cls(e2, v2, kfrag_commitment, kfrag_pok, 
                   kfrag_sig1, kfrag_sig2, sig, metadata=metadata)

    def to_bytes(self) -> bytes:
        """
        Serialize the CorrectnessProof to a bytestring.
        """
        e2 = self._point_e2.to_bytes()
        v2 = self._point_v2.to_bytes()
        kfrag_commitment = self._point_kfrag_commitment.to_bytes()
        kfrag_pok = self._point_kfrag_pok.to_bytes()
        kfrag_sig1 = self._bn_kfrag_sig1.to_bytes()
        kfrag_sig2 = self._bn_kfrag_sig2.to_bytes()
        sig = self._bn_sig.to_bytes()

        result = e2            \
            + v2               \
            + kfrag_commitment \
            + kfrag_pok        \
            + kfrag_sig1       \
            + kfrag_sig2       \
            + sig              

        result += self.metadata or b''

        return result

    def _bn_keytes__(self):
        return self.to_bytes()


class CapsuleFrag(object):
    def __init__(self, point_e1, point_v1, kfrag_id, point_noninteractive, 
                 point_xcoord, proof: CorrectnessProof=None):
        self._point_e1 = point_e1
        self._point_v1 = point_v1
        self._kfrag_id = kfrag_id
        self._point_noninteractive = point_noninteractive
        self._point_xcoord = point_xcoord
        self.proof = proof

    @classmethod
    def get_size(cls, curve: ec.EllipticCurve=None):
        """
        Returns the size (in bytes) of a CapsuleFrag given the curve without
        the CorrectnessProof.
        If no curve is provided, it will use the default curve.
        """
        curve = curve if curve is not None else default_curve()
        bn_size = CurveBN.get_size(curve)
        point_size = Point.get_size(curve)

        return (bn_size * 1) + (point_size * 4)

    @classmethod
    def from_bytes(cls, data: bytes, curve: ec.EllipticCurve = None):
        """
        Instantiates a CapsuleFrag object from the serialized data.
        """
        curve = curve if curve is not None else default_curve()
        bn_size = CurveBN.get_size(curve=curve)
        point_size = Point.get_size(curve=curve)
        data = BytesIO(data)

        # CurveBNs are the keysize in bytes, Points are compressed and the
        # keysize + 1 bytes long.
        e1 = Point.from_bytes(data.read(point_size), curve)
        v1 = Point.from_bytes(data.read(point_size), curve)
        kfrag_id = data.read(bn_size)
        ni = Point.from_bytes(data.read(point_size), curve)
        xcoord = Point.from_bytes(data.read(point_size), curve)

        proof = data.read() or None
        proof = CorrectnessProof.from_bytes(proof, curve) if proof else None

        return cls(e1, v1, kfrag_id, ni, xcoord, proof)

    def to_bytes(self):
        """
        Serialize the CapsuleFrag into a bytestring.
        """
        e1 = self._point_e1.to_bytes()
        v1 = self._point_v1.to_bytes()
        ni = self._point_noninteractive.to_bytes()
        xcoord = self._point_xcoord.to_bytes()

        serialized_cfrag = e1 + v1 + self._kfrag_id + ni + xcoord

        if self.proof is not None:
            serialized_cfrag += self.proof.to_bytes()

        return serialized_cfrag

    def verify_correctness(self,
                        capsule: "Capsule",
                        pubkey_a: UmbralPublicKey,
                        pubkey_b: UmbralPublicKey,
                        params: UmbralParameters=None):
        pubkey_a_point = pubkey_a.point_key
        pubkey_b_point = pubkey_b.point_key

        return assess_cfrag_correctness(self, capsule, pubkey_a_point,
                                        pubkey_b_point, params)

    def attach_proof(self, e2, v2, u1, u2, z1, z2, z3, metadata):
        self.proof = CorrectnessProof(point_e2=e2,
                         point_v2=v2,
                         point_kfrag_commitment=u1,
                         point_kfrag_pok=u2,
                         bn_kfrag_sig1=z1,
                         bn_kfrag_sig2=z2,
                         bn_sig=z3,
                         metadata=metadata)

    def __bytes__(self):
        return self.to_bytes()
