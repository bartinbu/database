
# Raspberry Pi Mobil İstasyon Kurulumu



## Yol haritası

- Raspberry Pi işletim sistemi kurulması

- Gsm Modülünün kurulması

- Veri Tabanı deposunun kurulması


  

  
### Raspberry Pi kurulumu

Raspberry pi önerilen dağıtımı Raspberry pi imaj yöneticisi ile kurun.
[Drive](https://drive.google.com/file/d/1MwOQPS_AYD92W2GKPYwThBw7UUbwXvsc/view?usp=sharing) linkinden kurulum dosylarını indirin ve arşivden çıkarın.

Çıkartılan gsmsetup isimli klasör mutlaka masaüstünde olmalı ve kurulumdan sonra silinmemeli !
Raspberrydeki kullanıcı adı mutlaka pi olmalı değiştirilirse çalışmayacaktır.

![Alt text](/Images/Resim1.png?raw=true "Optional Title")
![Alt text](/Images/Resim2.png?raw=true "Optional Title")
![Alt text](/Images/Resim3.png?raw=true "Optional Title")
![Alt text](/Images/Resim4.png?raw=true "Optional Title")

pi kullanıcısının şifresini girin daha sonra lazım olacak not alın.
Bu ayarlar wifiye otomatik bağlanması için yapılmıştır. ssh ile bağlantı almak için yapılmaktadır. Monitörlü kurulumda wifiye monitör ile bağlanılabilir.  
### Gsm Modülün Kurulması
Gsm modülün ilk kurulumunda internete ihtiyaç vardır bu yüzden wifi ile veya ethernet kablosu ile internete bağlayın.

Masaüstünde terminal açın

Proje dizinine gidin
```bash
cd gsmsetup
```
Kuruluma başlamadan önce bluetooth servislerini devre dışı bırakmak için aşağıda ki komutu çalıştırın.
```sh
systemctl mask serial-getty@ttyAMA0.service
```


gsm-bootup.sh dosyasına +x modu ekleyin
```sh
chmod +x gsm-bootup.sh
```
install.sh dosyasına +x modu ekleyin
```sh
chmod +x install.sh
```
sudo haklarıyla install.sh dosyasını çalıştırın.
```sh
sudo ./install.sh
```
GSM shiled üzerindeki ışıklar yanmaya başlayacaktır. İnternet bağlantısı için hat takılı olmalıdır. Hat takılı değilken de kurulum yapılabilir.

GSM bağlantısını kontrol etmek için pingtest.sh scriptini çalıştırabilirsiniz.(zorunlu değil)
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
