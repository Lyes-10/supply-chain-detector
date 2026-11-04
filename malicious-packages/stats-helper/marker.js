const payload = "Y29uc3QgZnMgPSByZXF1aXJlKCdmcycpOyBmcy5hcHBlbmRGaWxlU3luYygnL3RtcC90aHJlYXRoaXZlX21hcmtlci50eHQnLCAnT2JmdXNjYXRlZCBwYXlsb2FkIGV4ZWN1dGVkIVxuJyk7";
eval(Buffer.from(payload, 'base64').toString('utf8'));
