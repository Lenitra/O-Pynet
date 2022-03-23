import os
# write "lol" in tmp.sh
# delete tmp.sh
os.system("rm -rf tmp.sh")
os.system("echo echo lol > tmp.sh")
os.system("bash tmp.sh")
