var apigClient = apigClientFactory.newClient({
    accessKey: 'AKIAVPQAZP4ZPCHYRHH6',
    secretKey: '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'
});



function submitAll() {

console.log("inside submitAll");

var name = document.getElementById("name").value;
var phone = document.getElementById("phone").value;
var id = document.getElementById("FaceID").value

console.log(name + " " + phone);

if (validation()) 
{

  var params = {};
  var additionalParams = {};
  var body = {
    "name" : name,
    "phone" : phone,
    "faceId" : id
    };

    console.log(name + phone + id);

    apigClient.ownerPost(params, body, additionalParams)
      .then(function(result){
        console.log("inside then");
      }).catch( function(result){
          console.log("Inside Catch Function");
      });

}

}

function validation() {
	return true;
}
