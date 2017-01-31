$(function(){
	$('#btnShowMap').click(function(){
		
		$.ajax({
			url: '/tmap',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){

				var responseObj = JSON.parse(response);
				window. markers = [];


				_.each(responseObj, function(geo){
					var coordinatesArray = geo.fields["geo.coordinates"];

					var markerLatLng = {
						lat: coordinatesArray[0], lng: coordinatesArray[1]
					};

					var marker = new google.maps.Marker({
			          position: markerLatLng,
			          map: window.map,
			          title: 'Hello World!'
			        });

			        markers.push(marker);

				})

			},
			error: function(error){
				alert("Failed");
				console.log(error);
			}
		});

	});






});
