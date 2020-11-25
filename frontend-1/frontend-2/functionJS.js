var apigClient = apigClientFactory.newClient({
    accessKey: 'AKIAVPQAZP4ZPCHYRHH6',
    secretKey: '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'
});


function trigger_kvs(){
  var params = {};
  var additionalParams = {};
  var body = {
    };
  }

function Response()
{

var params = {};
var additionalParams = {};
var body = {
    "lastUserMessage": lastUserMessage
};
apigClient.visitorPost(params, body, additionalParams).then(function(result) {
    var info = result['data']['body']
returnMessage = JSON.parse(info)
if (returnMessage['status'] == "Success"){
    popUpWindow("Success！");
}
else {
    popUpWindow("Permission denied.");
}
})
}


function newEntry() {
    lastUserMessage = document.getElementById("OTP_field").value;
    document.getElementById("OTP_field").value = "";
    Response();
  }
}


function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}
