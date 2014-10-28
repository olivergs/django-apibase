<?php
/*
Requires phpseclib: http://phpseclib.sourceforge.net/
*/

include('Crypt/RSA.php');

$apiurl = 'API_URL_ENDPOINT';
$apikey = 'API_KEY';
$privatekey = <<<EOD
-----BEGIN RSA PRIVATE KEY-----
PRIVATE_KEY_CONTENTS
-----END RSA PRIVATE KEY-----
EOD;

$rsa = new Crypt_RSA();

//$rsa->setPassword('password');
$rsa->loadKey($privatekey); // private key

$mydata = array(
    'data1' => 'value1',
    'data2' => array(
    	'moredata' => 'morevalue',
    ),
);

$jsondata=json_encode($mydata);

$rsa->setSignatureMode(CRYPT_RSA_SIGNATURE_PKCS1);
$signature = base64_encode($rsa->sign($jsondata));

$postdata = array(
    'key' => $apikey,
    'data' => $jsondata,
    'signature' => $signature,
);

$ch = curl_init($apiurl);
curl_setopt_array($ch, array(
    CURLOPT_POST => TRUE,
    CURLOPT_RETURNTRANSFER => TRUE,
    CURLOPT_POSTFIELDS => $postdata,
));

echo "EXEC REQUEST";
// Send the request
$response = curl_exec($ch);
// print_r(curl_getinfo($ch));

// Check for errors
if($response === FALSE){
    die(curl_error($ch));
}

echo $response;

?>