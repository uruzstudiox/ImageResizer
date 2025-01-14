import sys
from os import path as os_path
from os import access as os_access
from os import R_OK as os_R_OK
from pathlib import Path as pathlib_path
from time import sleep as time_sleep
from typing import Literal


class FileValidator:
    """
    Bir dosya yolunun doğruluğunu, varlığını ve erişilebilirliğini kontrol
    etmek için işlevler sağlar.

    Methods:
        validate_path (None): Bir yolun boş veya geçersiz olup olmadığını
        doğrular. Yol boş veya geçersizse bir istisna fırlatır.
        validate_file (None): Bir dosyanın belirtilen konumda bulunup
        bulunmadığını doğrular. Belirtilen konumda yoksa bir istisna fırlatır.
        is_file_readable (None): Bir dosyanın okuma izinlerini kontrol eder.
        Dosya, okuma izinlerine sahip değilse bir istisna fırlatır.
        validate_file_name (None): Bir dosya adının boş bir metin olup
        olmadığını kontrol eder. Boşsa bir istisna fırlatır.
    """
    @staticmethod
    def validate_path(file_path: pathlib_path) -> None:
        """
        Bir yolun boş veya geçersiz olup olmadığını doğrular.

        Raises:
            ValueError: Boş bir yol veya geçersiz bir değer girilmişse.
        """
        if not file_path or not isinstance(file_path, pathlib_path):
            raise ValueError(
                f"Dosya yolu boş veya geçersiz: {file_path}"           
            )
        

    @staticmethod
    def validate_file(file_path: pathlib_path) -> None:
        """
        Bir dosyanın belirtilen konumda bulunup bulunmadığını doğrular.

        Raises:
            FileNotFoundError: Dosya belirtilen konumda yoksa.
        """
        if not os_path.exists(file_path):
            raise FileNotFoundError(
                f"Belirtilen dosya bulunamadı: {file_path}"
            )


    @staticmethod
    def validate_read_permission(file_path: pathlib_path) -> None:
        """
        Bir dosyanın okuma izinlerini kontrol eder.

        Raises:
            PermissionError: Dosyanın okuma izinleri yoksa.
        """ 
        if not os_access(file_path, os_R_OK):
            raise PermissionError(
                f"Dosya okunabilir değil: {file_path}"
            )
        
    
    @staticmethod
    def validate_file_name(file_name: str):
        """
        Bir dosya adının boş bir metin olup olmadığını kontrol eder.

        Raises:
            ValueError: Dosya adı boş bir metinse.
        """
        if file_name == "":
            raise ValueError(
                "Dosya adı boş bir metin olamaz."
            )


class FilePathManager:
    """
    Dosya yollarını oluşturmak, yönetmek ve saklamak gibi sıkça kullanılan 
    işlemler için işlevler sağlar.

    Methods:
        get_py_or_exe_dir (pathlib.Path): Uygulamanın bir betik dosyası veya 
        executable olarak çalışmasına göre çalıştığı dizini alır.
        convert_f_name_to_path (pathlib.Path): Bir dosya adına ve hedef 
        klasöre göre tam dosya yolunu oluşturur. Dosya adı boş bir metinse
        bir istisna fırlatır.
        save_f_path (None): Bir dosya yolunun başka bir dosyada saklanmasını
        sağlar. Verinin saklanacağı dosya belirtilen yolda zaten mevcutsa, 
        yeni veriyi eski verinin üzerine yazar.
        read_f_path (str): Belirtilen kayıt dosyasında saklanan yol bilgisini
        okur.
    """
    @staticmethod
    def get_py_or_exe_dir() -> pathlib_path:
        """
        Uygulamanın bir betik dosyası veya executable olarak çalışmasına göre
        çalıştığı dizini alır.

        Eğer uygulama bir pyhon betiği olarak çalışıyorsa,
        bu method betiğin bulunduğu dizini döndürür.
        Eğer uygulama bir executable (örneğin .exe) olarak paketlenmişse,
        çalıştırılabilir dosyanın bulunduğu dizini dödürür.
    
        Returns:
            pathlib.Path: Uygulamanın bulunduğu dizin.
        """
        if getattr(sys, 'frozen', False):
            return pathlib_path(sys.executable).parent
        else:
            return pathlib_path(__file__).parent


    @staticmethod
    def convert_f_name_to_path(
        file_name:str,
        *,
        target_folder: str = None
    ) -> pathlib_path:
        """
        Bir dosya adına ve hedef klasöre göre tam dosya yolunu oluşturur.

        Args:
            file_name (str): İşlenecek dosya adı.
            target_folder (str): İsteğe bağlı dosyanın bulunduğu veya
            bulunacağı hedef klasör adı.

        Returns:
            pathlib.Path: Tam dosya yolu.

        Raises:
            ValueError: Dosya adı boş bir metinse.
        """
        FileValidator.validate_file_name(file_name)  # ValueError

        base_dir = FilePathManager.get_py_or_exe_dir()

        if target_folder:
            return base_dir / target_folder / file_name
        return base_dir / file_name
    

    @staticmethod
    def save_f_path(
        file_path: pathlib_path,
        *,
        data:str,
        exempt: bool = False
        ) -> None:
        """
        Bir dosya yolunun başka bir dosyada saklanmasını sağlar. Verinin 
        saklanacağı dosya belirtilen yolda zaten mevcutsa, yeni veriyi eski
        verinin üzerine yazar.

        Args:
            file_path (pathlib.Path): Kayıt dosyasının yolu.
            data (str): Kayıt edilecek yol bilgisi.
            exempt (bool): Eğer 'true' girilirse kayıt edilecek yol bilgisinin
            dosyaya ait olup olmadığına bakılmaz.

        Raises:
            ValueError: Boş bir yol veya geçersiz bir değer girilmişse.
            FileNotFoundError: Dosya kayıt edilecek konumda yoksa.
            RuntimeError: Beklenmeyen hatalar oluşmuşsa.
        """
        FileValidator.validate_path(file_path)  # ValueError
        if not exempt:
            FileValidator.validate_file(data)  # FileNotFoundError

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(data)
        except Exception as e:
            raise RuntimeError(
                f"Dosya yazma sırasında beklenmedik bir hata oluştu: {e}"
            )
    

    @staticmethod
    def read_f_path(file_path: pathlib_path) -> str:
        """
        Belirtilen kayıt dosyasında saklanan yol bilgisini okur.

        Args:
            file_path(pathlib.Path): Kayıt dosyanın bulunduğu dizin.

        Returns:
            str: Tam dosya yolu.

        Raises:
            ValueError: Boş bir yol veya geçersiz bir değer girilmişse.
            FileNotFoundError: Dosya belirtilen konumda yoksa.
            PermissionError: Dosyanın okuma izinleri yoksa.
            RuntimeError: Beklenmeyen hatalar oluşmuşsa.
        """
        FileValidator.validate_path(file_path)  # ValueError
        FileValidator.validate_file(file_path)  # FileNotFoundError
        FileValidator.validate_read_permission(file_path)  # PermissionError

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(
                f"Dosya okuma sırasında beklenmedik bir hata oluştu: {e}"
            )
  

class ImageResizer:
    """
    'BMP' uzantılı bir dosyaya ızgara eklemek ve yeniden boyutlandırmak için
    işlevler sağlar.

    Methods:
        _validate_byte_len (None): Mevcut bayt sayısı ile beklenen bayt 
        sayısını karşılaştıran, özel metot. Bayt sayıları eşit değilse 
        bir istisna fırlatır.
        _split_bytes (int): Bit derinliğini baza alarak, piksel başına bayt
        sayısını belirleyen, özel metot. Bit derinliği desteklenmiyorsa bir
        istisna fırlatır.
        _convert_to_int (int): Tanımlı renk adını, RGB formatında bir 
        bytearray'e dönüştüren, özel metot. Renk tanımlı değilse bir istisna
        fırlatır.
        _convert_color_to_byte (bytearray): Tanımlı renk adını, RGB formatında
        bir bytearray'e dönüştüren, özel metot. Renk tanımlı değilse bir 
        istisna fırlatır.

        read_image (bytearray): Görüntüyü binary (ikili) olarak okur.
        save_image (None): Görüntü dosyasının güncellenmiş binary içeriğin
        belirtilen konuma kaydeder.

        add_grid (bytearray): Resme ızgara ekler.
        resize_image (bytearray):  Resmi yeniden boyutlandırır.
    """
    @staticmethod
    def _validate_byte_len(byte_len: int, excepted_len: int) -> None:
        """
        Mevcut bayt sayısı ile beklenen bayt sayısını karşılaştıran,
        özel metot.

        Raises:
            ValueError: Mevcut bayt sayısı, beklenen bayt sayısına eşit
            değilse.
        """
        if byte_len != excepted_len:
            raise ValueError(
                f"Piksel baytlarının sayısı ({byte_len}) "
                f"beklenenden ({excepted_len}) farklı."
                "\n(?) Bu hata genellikle bir iç işlem sorunudur ve "
                "kullanıcı hatasından kaynaklanmaz."
                "Eğer bir geliştirici değilseniz, lütfen bu sorun hakkında "
                "proje geliştiricisi ile iletişime geçin. Daha fazla bilgi "
                "ve destek için proje belgelerine göz atabilirsiniz."
            )


    @staticmethod
    def _split_bytes(bit_depth: int) -> int:
        """
        Bit derinliğini baza alarak, piksel başına bayt sayısını belirleyen,
        özel metot.

        Returns:
            int: Piksel başına düşen bayt sayısı.

        Raises:
            ValueError: Desteklenmeyen bir bit derinliği girilmişse.
        """
        if bit_depth == 32:
            return 4  # bytes_per_pixel = 4 Byte
        elif bit_depth == 24:
            return 3
        elif bit_depth == 16:
            return 2
        elif bit_depth == 8:
            return 1
        else:
            raise ValueError(f"Desteklenmeyen bit derinliği: {bit_depth}")


    @staticmethod
    def _convert_to_int(number: str) -> int:
        """
        Sayısal bir metin değerini 'int' bir değere dönüştüren, özel metot. 

        Returns:
            int: Dönüştürülen tamsayı değeri.

        Raises:
            TypeError: Girilen değer 'str' türünde değilse.
            ValueError: Girilen metin sayısal bir değer içermiyorsa.
        """
        try:
            return int(number)
        except (TypeError, ValueError):
            raise TypeError (
                f"'{number}' bir tamsayı değil."
            )


    @staticmethod
    def _convert_color_to_byte(
        color: Literal[
            "white",
            "black",
            "red",
            "green",
            "blue",
            "yellow",
            "magenta",
            "cyan"
        ]
    ) -> bytearray:
        """
        Tanımlı renk adını, RGB formatında bir 'bytearray''e dönüştüren,
        özel metot.

        Renkler şu şekilde dönüştürülür:
        - color_name -> B\\G\\R\\
        - "white" -> \\xFF\\xFF\\xFF
        - "black" -> \\x00\\x00\\x00
        - "red" -> \\x00\\x00\\xFF
        - "green" -> \\x00\\xFF\\x00
        - "blue" -> \\xFF\\x00\\x00
        - "yellow" -> \\x00\\xFF\\xFF
        - "magenta" -> \\xFF\\x00\\xFF
        - "cyan" -> \\xFF\\xFF\\x00

        Returns:
            bytearray: Bayt dizisine dönüştürülmüş renk bilgisi.

        Raises:
            ValueError: Tanımlanmamış bir renk girilmişse.
        """
        match color:
            case "white":
                return bytearray(b'\xFF\xFF\xFF')
            case "black":
                return bytearray(b'\x00\x00\x00')
            case "red":
                return bytearray(b'\x00\x00\xFF')
            case "green":
                return bytearray(b'\x00\xFF\x00')
            case "blue":
                return bytearray(b'\xFF\x00\x00')
            case "yellow":
                return bytearray(b'\x00\xFF\xFF')
            case "magenta":
                return bytearray(b'\xFF\x00\xFF')
            case "cyan":
                return bytearray(b'\xFF\xFF\x00')
            case _:
                raise ValueError(f"Desteklenmeyen bir renk: {color}")


    @staticmethod
    def read_image(file_path: pathlib_path) -> bytearray:
        """
        Görüntü dosyasını binary (ikili) olarak okur.

        Args:
            file_path (pathlib.Path): Görüntü dosyasının bulunduğu dizin.
        
        Raises:
            ValueError: Boş bir yol veya geçersiz bir değer girilmişse.
            FileNotFoundError: Dosya belirtilen konumda yoksa.
            PermissionError: Dosyanın okuma izinleri yoksa.
            RuntimeError: Beklenmeyen hatalar oluşmuşsa.
        """      
        FileValidator.validate_path(file_path)  # ValueError
        FileValidator.validate_path(file_path)  # FileNotFoundError
        FileValidator.validate_read_permission(file_path)  # PermissionError

        try:
            with open(file_path, "rb") as file:
                # İkili diziye çevir ve döndür.
                return bytearray(file.read())  
        except Exception as e:
            raise RuntimeError(
                f"Dosya okuma sırasında beklenmedik bir hata oluştu: {e}"
            )
    

    @staticmethod
    def save_image(file_path: pathlib_path, *, data: bytearray) -> None:
        """
        Görüntü dosyasının güncellenmiş binary içeriğini belirtilen konuma
        kaydeder.

        Args:
            data (bytearray): Kaydedilecek içerik.
            file_path (pathlib.Path): Görüntü dosyasının kaydedileceği dizin.

        Raises:
            ValueError: Boş bir yol veya geçersiz bir değer girilmişse.
            RuntimeError: Beklenmeyen hatalar oluşmuşsa.

        """
        FileValidator.validate_path(file_path)  # ValueError

        try:
            with open(file_path, "wb") as file:
                file.write(data)
        except Exception as e:
            raise RuntimeError(
                f"Dosya yazma sırasında beklenmedik bir hata oluştu: {e}"
            )
        
    
    @staticmethod
    def add_grid(
        data: bytearray,
        *,
        grid_size: str,
        grid_color: str = "white"
    ) -> bytearray:
        """
        Resme ızgara ekler.

        Args:
            data (bytearray): Grid eklenecek içerik.
            width (int): Resmin genişliği (piksel cinsinden).
            height (int): Resmin yüksekliği (piksel cinsinden).
            grid_size (int): Grid karelerinin boyutu (piksel cinsinden).
            grid_color (str): Grid piksellerinin rengi.

        Raises:
            ValueError: Tanımlanmamış bir renk girilmişse.
            TypeError: Sayısal bir metin değeri girilmemişse.
            ValueError: Desteklenmeyen bir bit derinliği girilmişse.
        """
        # (!) Eğer veriyi doğru şekilde okuyamıyorsanız, 3.0'dan sonraki
        # BMP sürümlerinde başlık yapıları farklılık gösterebilir.
        # byteorder = little-endian
        start_px_data = int.from_bytes(data[10:14], byteorder="little")
        pixel_data = data[start_px_data:]

        width = int.from_bytes(data[18:22], byteorder="little") 
        height = int.from_bytes(data[22:26], byteorder="little")

        bit_depth = int.from_bytes(data[28:30], byteorder="little")
        bytes_per_pixel = ImageResizer._split_bytes(bit_depth)  # ValueError

        grid_size = ImageResizer._convert_to_int(grid_size)  # TypeError
        pixel_color = ImageResizer._convert_color_to_byte(
            grid_color  # ValueError
        )

        for y in range(height):  # Satır sırası
            for x in range(width):  # Sütun sırası
                start_px_bytes = (y * width + x) * bytes_per_pixel

                # Eğer piksel grid çizgisi üzerindeyse, renk değiştir.
                if x % grid_size == 0 or y % grid_size == 0:
                    pixel_data[
                        start_px_bytes:start_px_bytes + 3  # İlk 3 bayt (BGR)
                    ] = pixel_color

        # Pixel verisini güncelle.
        data[start_px_data:] = pixel_data

        return data

   
    @staticmethod
    def resize_image(
        data: bytearray,
        *,
        new_width: str,
        new_height: str,
        startx: str,
        starty: str,
    ) -> bytearray:
        """
        Resmi yeniden boyutlandırır.

        Args:
            data (bytearray): Yeniden boyutlandırılacak içerik.
            new_width (str): İstenilen genişlik.
            new_height (str): İstenilen yükseklik.
            startx (str): Yatay eksende sol alt köşeye olan uzaklık.
            starty (str): Dikey eksende sol alt köşeye olan uzaklık.

        Raises:
            ValueError: Desteklenmeyen bir bit derinliği girilmişse.
            TypeError: 'new_with' için sayısal bir metin değeri girilmemişse.
            ValueError: '4 <= new_width <= width' değilse.
            TypeError: 'new_heigth' için sayısal bir metin değeri
            girilmemişse.
            ValueError: '4 <= new_height <= height' değilse.
            TypeError: 'startx' için sayısal bir metin değeri girilmemişse.
            ValueError: 'startx' negatif bir değerse.
            ValueError: 'Başlangıç x + Genişlik' orjinal sınırlar dışındaysa.
            TypeError: 'starty' için sayısal bir metin değeri girilmemişse.
            ValueError: 'starty' negatif bir değerse.
            ValueError: 'Başlangıç y + Yükseklik' orjinal sınırlar dışındaysa.
            ValueError: Mevcut bayt sayısı ve beklenen sayıya eşit değilse.
        """
        # (!) Eğer veriyi doğru şekilde okuyamıyorsanız, 3.0'dan sonraki
        # BMP sürümlerinde başlık yapıları farklılık gösterebilir.
        # byteorder = little-endian
        start_px_data = int.from_bytes(data[10:14], byteorder="little")
        pixel_data = data[start_px_data:]

        width = int.from_bytes(data[18:22], byteorder="little")
        height = int.from_bytes(data[22:26], byteorder="little")

        bit_depth = int.from_bytes(data[28:30], byteorder="little")
        bytes_per_pixel = ImageResizer._split_bytes(bit_depth)  # ValueError

        new_width = ImageResizer._convert_to_int(new_width)  # TypeError
        if new_width < 4 or new_width > width:
            raise ValueError(
                f"'{new_width}' değeri '4 <= Yeni Genişlik <= {width}' "
                "eşitliğini sağlamalıdır."
            )
        new_height = ImageResizer._convert_to_int(new_height)  # TypeError
        if new_height < 4 or new_height > height:
            raise ValueError(
                f"'{new_height}' değeri '4 <= Yeni Yükseklik <= {height}' "
                "eşitliğini sağlamalıdır."
            )

        startx = ImageResizer._convert_to_int(startx)  # TypeError
        if startx < 0:
            raise ValueError("Başlangıç x pozitif bir tamsayı olmalı.")
        elif startx + new_width > width:
            # Kontrol sırarası ihtimali yüksek -> ihtimali düşük.
            raise ValueError(
                f"'Başlangıç x + Genişlik ({startx + new_width})' "
                "orjinal sınırlar dışında kalıyor."
            )
        starty = ImageResizer._convert_to_int(starty)  # TypeError
        if starty < 0:
            raise ValueError("Başlangıç y pozitif bir tamsayı olmalı.")
        elif starty + new_height > height:
            raise ValueError(
                f"'Başlangıç y + Yükseklik ({starty + new_height })' "
                "orjinal sınırlar dışında kalıyor."
            )

        new_data = bytearray()

        # sıra (1, 2, ...) = n, index (0, 1, ...) = n-1 (width, height)
        for y in range(height):  # Satır sırası
            if y < starty:
                continue
            elif y >= starty + new_height:
                continue

            for x in range(width):  # Sütun sırası
                if x < startx:
                    continue
                elif x >= startx + new_width:
                    continue
                    
                #row_size = ((width * bytes_per_pixel + 3) // 4) * 4
                start_px_bytes = (y * width + x) * bytes_per_pixel

                new_data.extend(
                    pixel_data[
                        start_px_bytes:start_px_bytes + bytes_per_pixel
                    ]
                )

        # Bayt sayılarını kontrol et.
        ImageResizer._validate_byte_len(
            byte_len=len(new_data),
            excepted_len=new_width * new_height * bytes_per_pixel
        )  # ValueError
        
        # Genişlik ve yükseklik bilgisini güncelle.
        # new_width (int).to_bytes()
        data[18:22] = new_width.to_bytes(length=4, byteorder="little")
        data[22:26] = new_height.to_bytes(length=4, byteorder="little")
        
        # Pixel verisini güncelle.
        data[start_px_data:] = new_data

        return data



if __name__ == "__main__":
    ## ADDITIONAL FUNCTIONS 

    def get_input(txt) -> str:
        return input(f"{txt}: ")


    def getting_log_f_path() -> pathlib_path:
        """
        Kayıt dosyası yolunu alır. (Bu işlem, bakımı daha kolay olması için
        ayrı bir işlev olarak tanımlanmıştır.)
        """
        return FilePathManager.convert_f_name_to_path(
            "imagepath.txt", target_folder="data"
        )


    def resetting_log_f_path() -> None:
        """
        Kayıtlı dosya yolunu sıfırlamak için gereken süreci işler.
        """
        # Kayıt dosyası yolunu al.
        log_f_path = getting_log_f_path()

        # Kayıtlı dosya yolunu oku ve yazdır.
        try:
            image_path = FilePathManager.read_f_path(log_f_path)
        except (
            ValueError, FileNotFoundError, PermissionError, RuntimeError
        ) as e:
            print(f"\n(!) Kayıtlı dosya yolunu okuma başarısız: {e}")
            return
        print(f"Kayıtlı dosya yolu: {image_path}")

        # Kullanıcıyı sıfırlama işlemi hakkında uyar.
        print("\n(!) Kayıtlı dosya yolu sıfırlanmak üzere.")

        # İşleme devam edilsin mi?
        continue_processing()

        # Kayıt dosyasına “Kayıtlı dosya yolu yok.” yazdır.
        try:
            FilePathManager.save_f_path(
                log_f_path,
                data="Kayıtlı dosya yolu yok.",
                exempt=True
            )
        except (ValueError, FileNotFoundError, RuntimeError) as e:
            print(f"\n(!) Dosya yolu sıfırlama işlemi başarısız: {e}")
            return

        # İşlemin başarılı olduğunu  bildir.
        print(f"\n(+) Dosya yolu sıfırlandı.")
        

    def selecting_file_to_process() -> None:
        """
        İşlenecek dosyanın yolunu oluşturmak ve saklamak için gereken süreci
        işler.

        Kullanıcıdan işlenecek dosyanın adını alır ve hedef klasörü
        'images' olarak kabul ederek tam dosya yolunu oluşturup, yolu bir
        '.txt' dosyasında saklar.
        """
        # Kayıt dosyası yolunu al.
        log_f_path = getting_log_f_path()

        # Kayıtlı dosya yolunu oku ve yazdır.
        try:
            image_path = FilePathManager.read_f_path(log_f_path)
        except (
            ValueError, FileNotFoundError, PermissionError, RuntimeError
        ) as e:
            print(f"\n(!) Kayıtlı dosya yolunu okuma başarısız: {e}")
            return
        print(f"Kayıtlı dosya yolu: {image_path}")

        # Düzenlenecek görselin tam adını (uzantı dahil) al.
        image_name = get_input("\nİşlenecek dosyanın adı")

        # İşleme devam edilsin mi?
        continue_processing()

        # Alınan görsel ismini kullanarak görselin tam yolunu oluştur.
        try:
            image_path = FilePathManager.convert_f_name_to_path(
                image_name,
                target_folder="images"
            )
        except ValueError as e:
            print(f"\n(!) Yeni dosya adı geçersiz: {e}")
            return

       # Oluşturulan dosya yolunu ‘str’ olarak kayıt dosyasına yazdır.
        try:
            FilePathManager.save_f_path(log_f_path, data=str(image_path))
        except (ValueError, FileNotFoundError, RuntimeError) as e:
            print(f"\n(!) Yeni dosya yolu kayıt işlemi başarısız: {e}")
            return

        # İşlemin başarılı olduğunu  bildir.
        print(
            f"\n(+) işlenecek dosyanın yol bilgisi güncellendi: {image_path}"
        )


    def image_gridding() -> None:
        """
        Seçilen görsele ızgara eklemek ve yeni bir dosya olarak kaydetmek
        için gereken süreci işler. 
        """
        # Kayıt dosyasının yolunu al.
        log_f_path = getting_log_f_path()

        # 'imagepath.txt' dosyasından görselin bulunduğu yol bilgisini oku.
        try:
            file_path = FilePathManager.read_f_path(log_f_path)
        except (
            ValueError, FileNotFoundError, PermissionError, RuntimeError
        ) as e:
            print(f"\n(!) Kayıtlı yol bilgisini okuma işlemi başarısız: {e}")
            return 
        # Okunan yol bilgisini (string), pathlib.Path'e çevir 
        # read_image(): validate_path() hata vermemesi için.
        file_path = pathlib_path(file_path)

       # Görsel dosyasını oku.
        try:
            image_data = ImageResizer.read_image(file_path)
        except (
            ValueError, FileNotFoundError, PermissionError, RuntimeError
        ) as e:
            print(f"\n(!) Görsel dosyası okuma işlemi başarısız: {e}")
            return

        # Yeni görselin kaydedileceği ismi al.
        output_f_name = get_input("İşlenmiş dosyanın kaydedileceği isim")
        # Alınan ismi bir yola dönüştür.
        try:
            output_file = FilePathManager.convert_f_name_to_path(
                output_f_name, target_folder="edited_images"
            )
        except ValueError as e:
            print(f"(!) Yeni görselin kaydedileceği yol oluşturulamadı: {e}")
            return

        # Izgara kareleri için bir büyüklük al.
        grid_size = get_input("Grid kareleri için istenen büyüklük (piksel)")

        # Izgara çizgileri için bir renk al.
        print("(black, red, green, blue, yellow, magenta, cyan)")
        grid_color = get_input(
            "Grid çizgileri için bir renk seçin (varsayılan=white)"
        ).strip().lower()
        # Alınan renk boş string veya boşluksa varsayılan olarak 'beyaz' al.
        if not grid_color: 
            grid_color = "white"

        # İşleme devam edilsin mi?
        continue_processing()

        # Izgara ekle
        try:
            image_with_grid = ImageResizer.add_grid(
                data=image_data,
                grid_size=grid_size,
                grid_color=grid_color  # Default (white)
            )
        except (ValueError, TypeError) as e:
            print(f"\n(!) Izgara ekleme işlemi başarısız: {e}")
            return

        # Yeni resmi kaydet.
        try:
            ImageResizer.save_image(output_file, data=image_with_grid)
        except (ValueError, RuntimeError) as e:
            print(f"\n(!) İşlenmiş dosyayı yazma işlemi başarısız: {e}")
            return
        
        # İşlemin başarılı olduğunu  bildir.
        print("\n(+) Izgara ekleme işlemi başarıyla tamamlandı.")


    def image_resizing() -> None:
        """
        Seçilen görseli yeniden boyutlandırmak ve yeni bir dosya olarak
        kaydetmek için gereken süreci işler.
        """
        # Kayıt dosyasının yolunu al.
        log_f_path = getting_log_f_path()

        # 'imagepath.txt' dosyasından görselin bulunduğu yol bilgisini oku.
        try:
            file_path = FilePathManager.read_f_path(log_f_path)
        except (
            ValueError, FileNotFoundError, PermissionError, RuntimeError
        ) as e:
            print(f"\n(!) Kayıtlı yol bilgisini okuma işlemi başarısız: {e}")
            return 
        # Okunan yol bilgisini (string), pathlib.Path'e çevir 
        # read_image(): validate_path() metotlarının hata vermemesi için.
        file_path = pathlib_path(file_path)

       # Görsel dosyasını oku.
        try:
            image_data = ImageResizer.read_image(file_path)
        except (
            ValueError, FileNotFoundError, PermissionError, RuntimeError
        ) as e:
            print(f"\n(!) Görsel dosyası okuma işlemi başarısız: {e}")
            return
        
        # Yeni görselin kaydedileceği ismi al.
        output_f_name = get_input("İşlenmiş dosyanın kaydedileceği isim")
        # Alınan ismi bir yola dönüştür.
        try:
            output_file = FilePathManager.convert_f_name_to_path(
                output_f_name, target_folder="edited_images"
            )
        except ValueError as e:
            print(f"(!) Yeni görselin kaydedileceği yol oluşturulamadı: {e}")
            return
        
        new_width = get_input("İstenilen genişlik (piksel)")
        new_height = get_input("İstenilen yükseklik (piksel)")

        # Boyutlandırmanın başlayacağı yatay konumu (x) al.
        startx = get_input(
            "Yatayda sol alt köşeye olan uzaklık (piksel, varsayılan=0)"
        ).strip()
        # Alınan yatay konuma bir değer verilmişse varsayılan olarak 0 al.
        if not startx:
            startx = 0

        # Boyutlandırmanın başlayacağı dikey konumu (y) al.
        starty = get_input(
            "Dikeyde sol alt köşeye olan uzaklık (piksel, varsayılan=0)"
        ).strip()
        # Alınan dikey konuma bir değer verilmişse varsayılan olarak 0 al.
        if not starty:
            starty = 0

        # İşleme devam edilsin mi?
        continue_processing()

        # Yeniden boyutlandır.
        try:
            resized_image = ImageResizer.resize_image(
                data=image_data,
                new_width=new_width,
                new_height=new_height,
                startx=startx,
                starty=starty
            )
        except (ValueError, TypeError) as e:
            print(f"\n(!) Yeniden boyutlandırma işlemi başarısız: {e}")
            return
        
        # Yeni resmi kaydet.
        try:
            ImageResizer.save_image(output_file, data=resized_image)
        except (ValueError, RuntimeError) as e:
            print(f"\n(!) İşlenmiş dosyayı yazma işlemi başarısız: {e}")
            return

        # İşlemin başarılı olduğunu  bildir.
        print("\n(+) Yeniden boyutlandırma işlemi başarıyla tamamlandı.")


    ## MENU FUNCTIONS
    
    def continue_processing() -> None:
        """
        Kullanıcıya mevcut işleme devam edilip, edilmeyeceği sorulur. Cevap
        evetse işleme devam edilir, hayırsa ana menüye dönülür.
        """
        while True:
            result = get_input("İşleme devam et (e/h) ").lower()

            if result == "h":
                print("\nAna menüye dönülüyor...")

                time_sleep(0.5)
                main_menu()
            elif result == "e":
                break
            else:
                continue


    def main_menu() -> None:
        """
        Uygulamanın ana menüsünü başlatır. Kullanıcıdan bir işlem seçmesini
        ister ve seçilen işleme göre ilgili süreci başlatır.
        """
        menu_list = [
            "(0): Reset File Path",
            "(1): Select File",
            "(2): Image Gridding",
            "(3): Image Resizing",
            "(exit): Exit",
            "\n(!) Lütfen işlemek için bir dosya şeçmediyseniz veya son "
            "seçilen dosyadan devam etmek istemiyorsanız (0) anahtarını "
            "kullanın."
        ]
      
        while True:
            print(f"{"-"*100}\n>>> IMAGE RESIZER >>>\n")
            for i in menu_list:
                print(i)

            key = get_input(
                "İstenilen işleme ait anahtarı girin"
            ).lower()
           
            if key == "exit":
                print("\nUygulamadan çıkış yapılıyor...")
                print("-"*100)

                time_sleep(1)
                quit()
            elif key == "0":
                print(f"{"-"*100}\n>>> RESET FILE PATH >>>\n")

                resetting_log_f_path()
                    
                time_sleep(0.3)
                continue 
            elif key == "1":
                print(f"{"-"*100}\n>>> SELECT FILE >>>\n")

                selecting_file_to_process()

                time_sleep(0.3)
                continue 
            elif key == "2":
                print(f"{"-"*100}\n>>> IMAGE GRIDDING >>>\n")

                image_gridding()
                    
                time_sleep(0.3)
                continue
            elif key == "3":
                print(f"{"-"*100}\n>>> IMAGE RESIZING >>>\n")

                image_resizing()

                time_sleep(0.3)
                continue
            else:
                print(
                    "\n(?) Doğru anahtar için, "
                    "parantez içindeki değeri girdiğinizden emin olun."
                )

                time_sleep(0.3)
                continue


    main_menu()  # Program akışını başlat.


# Version0.0.0 - 25.12.2024 - Uruz - Raw version.
# Vesion0.1.0 - 07.01.2025 - Uruz - First version.