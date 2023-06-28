
# Raspberry Pi Mobil İstasyon Kurulumu



## Yol haritası

- Raspberry Pi işletim sistemi kurulması

- Gsm Modülünün kurulması

- Veri Tabanı deposunun kurulması


  

  
### Raspberry Pi kurulumu

Raspberry pi OS other kısmından Raspberry Pi OS Lite (64-bit) olan versiyonu Raspberry pi imaj yöneticisi ile kurun.
Raspberrydeki kullanıcı adı mutlaka pi olmalı değiştirilirse çalışmayacaktır.


![Alt text](/Images/Resim1.png?raw=true "Optional Title")
![Alt text](/Images/Resim2.png?raw=true "Optional Title")
![Alt text](/Images/Resim3.png?raw=true "Optional Title")
![Alt text](/Images/Resim4.png?raw=true "Optional Title")

pi kullanıcısının şifresini girin daha sonra lazım olacak not alın.
Bu ayarlar wifiye otomatik bağlanması için yapılmıştır. ssh ile bağlantı almak için yapılmaktadır. Monitörlü kurulumda wifiye monitör ile bağlanılabilir.  
### Gsm Modülün Kurulması
Gsm modülün ilk kurulumunda internete ihtiyaç vardır bu yüzden wifi ile veya ethernet kablosu ile internete bağlayın.

gsmsetup.zip dosyasını raspberry pi'nin /home/pi dizinine aktarın 
```bash
wget https://github.com/bartinbu/gsmsetup/raw/main/gsmsetup.zip
```

/home/pi dizininde terminal açın
Önemli not : Çıkartılan gsmsetup isimli klasör mutlaka /home/pi dizininde olmalı ve kurulumdan sonra silinmemeli !

Zip dosyasını çıkartın
```bash
unzip gsmsetup.zip
```
/home/pi/gsmsetup dizinine gidin
```bash
cd gsmsetup
```
Tüm .sh uzantılı dosyalara +x yetkisi verin
```sh
sudo chmod +x *.sh
```
sudo haklarıyla install.sh dosyasını çalıştırın.
```sh
sudo ./install.sh
```
GSM shiled üzerindeki ışıklar yanmaya başlayacaktır. İnternet bağlantısı için hat takılı olmalıdır. Hat takılı değilken de kurulum yapılabilir.

GSM bağlantısını kontrol etmek için pingtest.sh scriptini çalıştırabilirsiniz.(zorunlu değil) Eğer ppp0 arayüzü gelmiyorsa hat çekmiyordur çeken bir yerlerde kendisi otoatik olarak gelecektir. 
```sh
./pingtest.sh
``` 
### Veri Tabanı deposunun kurulması
Masaüstünde terminal açın.
Depoyu klonlayın
```git
git clone https://github.com/bartinbu/database.git
``` 

Klasörün içine girin
```git
cd database
``` 
install.sh dosyasına +x modu ekleyin
```sh
chmod +x init.sh
```
sync.sh dosyasına +x modu ekleyin
```sh
chmod +x sync.sh
```
sudo haklarıyla init.sh dosyasını çalıştırın.
```sh
./init.sh
```


Kurulum esnasında size bir ssh key verilecek bu keyi githubın ayarlar kısmında SSH and GPG keys kısmına ekleyin.

Yine Kurulum kısmında size Node Name soracaktır bu da istasyonun adı olacak diğer istasyon adlarından farklı bir isim kullanmalısınız yoksa çakışma olacak ve her iki istasyonda da baştan kurulum yapılması gerekecektir.

Kurulum işlemi bittikten sonra cihazları bağlayıp ilk sync işlemini yapmalısınız.
sudo haklarıyla init.sh dosyasını çalıştırın.
```sh
./sync.sh
```
ilk eşitlemede yes demeniz gerkmektedir. 
Sistem her 1 dakikada bir veri gönderecektir.
