import subprocess
   
domain = "cubicbits.com"
command = "whois {} | grep 'This query returned 0 objects'".format(domain)
whois_output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) 

if whois_output.returncode == 0:
    print("Domain {} does not exist".format(domain))
else:
    print("Domain {} exists".format(domain)) 