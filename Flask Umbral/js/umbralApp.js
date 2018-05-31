function GenerateKeys() {

	$.ajax({
            url: "http://localhost:5000/genKeys",
            data: "", //ur data to be sent to server
            contentType: "application/json; charset=utf-8",
            type: "GET",
            success: function (data) {
	       
               $('#AliceSK').val(data['sk_A']);
               $('#AlicePK').val(data['pk_A']);
               $('#BobSK').val(data['sk_B']);
               $('#BobPK').val(data['pk_B']);

            },
            error: function (x, y, z) {
               alert(x.responseText +"  " +x.status);
            }
        });

}

function Encrypt() {

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

	$.ajax({
            url: "http://localhost:5000/encrypt",
            dataType : 'json',
            data : JSON.stringify(sendData),
            contentType: "application/json; charset=utf-8",
	    headers: {
		'Access-Control-Allow-Headers' : '*'
	    },
            type: "POST",
            success: function (data) {
	       $('#emsg').val(data['emsg'])
	       $('#capsule').val(data['capsule'])
            },
            error: function (x, y, z) {
               alert(x.responseText +"  " +x.status);
            }
        });

}

function Umbralize() {

	var sk_A = $('#AliceSK').val();
	var pk_B = $('#BobPK').val();
	var M = parseInt($('#M').val());
	var N = parseInt($('#N').val());

    console.log(typeof M)

	if(M === '') {
		M = 10;
		$('#M').val(10);
	}
	if(N === '') {
		$('#N').val(20);
		N = 20;
	}

	if(M < N) {

		if(sk_A !== '' && pk_B !== '' && typeof M === 'number' && typeof N === 'number' ) {

			sendData = {
					 'sk_A': sk_A,
					 'pk_B': pk_B,
				       'M' : M,
				       'N' : N
		   			   }

			$.ajax({

				url: "http://localhost:5000/umbralize",
				dataType : 'json',
				data : JSON.stringify(sendData),
				contentType: "application/json; charset=utf-8",
				headers: {
					'Access-Control-Allow-Headers' : '*'
				},
				type: "POST",
				success: function (data) {

				   for(var i=0; i< data['bytekfrags'].length;i++) {

					  jQuery('<option/>', {
							value: data['bytekfrags'][i],
							html: data['bytekfrags'][i]
							}).appendTo('#kfrags select');
					}



				},
				error: function (x, y, z) {
				   alert(x.responseText +"  " +x.status);
				}
			});

		}

	} else {
		alert('Ingrese M menor a N ' + M + ' ' + N)
	}	

}

function Decrypt() {

	var capsule = $('#capsule').val();
	var sk_B = $('#BobSK').val();
	var pk_A = $('#AlicePK').val();
	var emsg = $('#emsg').val();

    var kfragsSel = [];


	$('#kfrags :selected').each(function(i, selected){ 
	  kfragsSel[i] = $(selected).text(); 
	});


	sendData = {
			     'capsule' : capsule,
		         'sk_B' : sk_B,
                 'pk_A' : pk_A,
                 'emsg' : emsg,
                 'kfragsSel' : kfragsSel
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
		   $('#omsg').val(data['omsg'])
        },
        error: function (x, y, z) {
           alert(x.responseText +"  " +x.status);
        }

	    });

}


$(function() {
  $(window).load(function() {
  });
});

