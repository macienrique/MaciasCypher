function GenerateKeys() {

	$.ajax({
            url: "http://localhost:5000/genKeys",
            data: "", //ur data to be sent to server
            contentType: "application/json; charset=utf-8",
	    headers: {
		'Access-Control-Allow-Headers' : '*'
	    },
            type: "GET",
            success: function (data) {
	       
               $('#AliceSK').val(data['sk_A']);
               $('#AlicePK').val(data['pk_A']);
               $('#BobSK').val(data['sk_B']);
               $('#BobPK').val(data['pk_B']);
               $('#EphSK').val(data['sk_Eph']);
	       $('#reeK').val(data['reeK']);
            },
            error: function (x, y, z) {
               alert(x.responseText +"  " +x.status);
            }
        });

}

function EncryptA() {

var msg = $('#msg').val();
var emsg = $('#emsg');
var pk_A = $('#AlicePK').val();

if(msg == '') {
	$('#msg').val('PRE Everis Blockchain')
	msg = 'PRE Everis Blockchain';
}

sendData = {
	     'msg': msg,
             'pk_A': pk_A
           }
console.log("data", sendData)

	$.ajax({
            url: "http://localhost:5000/encryptA",
            dataType : 'json',
            data : JSON.stringify(sendData),
            contentType: "application/json; charset=utf-8",
	    headers: {
		'Access-Control-Allow-Headers' : '*'
	    },
            type: "POST",
            success: function (data) {
	       $('#emsg').val(data)
            },
            error: function (x, y, z) {
               alert(x.responseText +"  " +x.status);
            }
        });

}

function DecryptA() {

var emsg = $('#emsg').val();
var sk_A = $('#AliceSK').val();

if(emsg !== '' && sk_A !== '') {

	sendData = {
		     'emsg': emsg,
		     'key': sk_A
		   }


	$.ajax({
		    url: "http://localhost:5000/decrypt",
		    dataType : 'json',
		    data : JSON.stringify(sendData),
		    contentType: "application/json; charset=utf-8",
		    headers: {
			'Access-Control-Allow-Headers' : '*'
		    },
		    type: "POST",
		    success: function (data) {
		       $('#AliceDecMsg').val(data)
		    },
		    error: function (x, y, z) {
		       alert(x.responseText +"  " +x.status);
		    }
		});
}	

}

function Reencrypt() {

var emsg = $('#emsg').val();
var reeK = $('#reeK').val();
var BobPK = $('#BobPK').val();
var EphSK = $('#EphSK').val();

if(emsg !== '' && reeK !== '' && BobPK !== '' && EphSK !== '') {

	sendData = {
		     'emsg': emsg,
		     'reeK': reeK,
		     'pk_B' : BobPK,
		     'EphSK' : EphSK
		   }


	$.ajax({
		    url: "http://localhost:5000/reencrypt",
		    dataType : 'json',
		    data : JSON.stringify(sendData),
		    contentType: "application/json; charset=utf-8",
		    headers: {
			'Access-Control-Allow-Headers' : '*'
		    },
		    type: "POST",
		    success: function (data) {
		       $('#remsg').val(data['remsg'])
                       $('#BEphPK').val(data['BEphPK'])
		    },
		    error: function (x, y, z) {
		       alert(x.responseText +"  " +x.status);
		    }
		});
}	

}

function DecryptEphKey() {

var BobSK = $('#BobSK').val();
var BEphPK = $('#BEphPK').val();

if(BobSK !== '' && BEphPK !== '') {

	sendData = {
		     'sk_B': BobSK,
		     'BEphPK': BEphPK
		   }


	$.ajax({
		    url: "http://localhost:5000/decryptEphKey",
		    dataType : 'json',
		    data : JSON.stringify(sendData),
		    contentType: "application/json; charset=utf-8",
		    headers: {
			'Access-Control-Allow-Headers' : '*'
		    },
		    type: "POST",
		    success: function (data) {
		       $('#EphPKDec').val(data)
		    },
		    error: function (x, y, z) {
		       alert(x.responseText +"  " +x.status);
		    }
		});
}	

}

function BobDecryptMessage() {

var remsg = $('#remsg').val();
var EphPKDec = $('#EphPKDec').val();

if(remsg !== '' && EphPKDec !== '') {

	sendData = {
		     'emsg': remsg,
		     'key': EphPKDec
		   }


	$.ajax({
		    url: "http://localhost:5000/decrypt",
		    dataType : 'json',
		    data : JSON.stringify(sendData),
		    contentType: "application/json; charset=utf-8",
		    headers: {
			'Access-Control-Allow-Headers' : '*'
		    },
		    type: "POST",
		    success: function (data) {
		       $('#omsg').val(data)
		    },
		    error: function (x, y, z) {
		       alert(x.responseText +"  " +x.status);
		    }
		});
}	

}


$(function() {
  $(window).load(function() {
  });
});

