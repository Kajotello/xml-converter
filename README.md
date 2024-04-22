### Konwerter plików JSON-XML

W ramach zadania zrealizowano prosty konwerter plików z formatu JSON do formatu XML. Program  napisany został z wykorzystaniem języka Python w wesji 3.11 i uruchamiany jest z odpowiednimi argumnetami wywołania, które można poznać za pomocą flagi `-h` :

```
$ python3 converter.py -h
usage: JSON2XML converter [-h] [--logfile LOGFILE] [--loglevel {ERROR,INFO,DEBUG}] input_folder output_folder

Convert JSON fueling files to XML

positional arguments:
  input_folder          folder with input files in JSON format
  output_folder         folder in which files after conversion will be saved

options:
  -h, --help            show this help message and exit
  --logfile LOGFILE     folder in which logs will be saved
  --loglevel {ERROR,INFO,DEBUG}
                        level of logging information
```

Program w obecnej formie, zgodnie z zapreznetowanymi wymaganiami, po uruchomieniu dokonuje konwersji (jeśli jest ona możliwa) plików znajdujących się w folderze źródłowym a następnie poztaje w nieskończonej pętli, konwertując na bieżąco pliki umieszczone w folderze. Możliwe jest również jednak wywołanie programu jedyni jeden raz, jak opisano w powyższym menu.

Weryfikację procesu przebiegu konwersji umożliwiają zbierane na bieżąco logi. Dzięki trzem możliwym do wyboru poziomom mamy możliwość wyboru, czy chcemy, aby zapisywane były jedynie informacje o błędach (które dzięki temu nie zatrzymują daleszego przetwarzania), czy także podstawowe informacje lub nawet szczegółowe informacje o zawartości poszczególnych plików (tryb DEBUG).

Do projektu dołączono także mały zestaw testów, które sprawdzają poprawność działania konwersji w różnych przypadkach, w tym tych powinnych powodować błędy.


### Popozycje do części 2 zadania
a. System monitoringu powinien na bieżąco analizować logi zapisywane do opdowiedniego pliku, w szczególności informację o pojawiających się błędach i szukać potencalnych podobieństw w zawartości tych plików (informacje te zbierane są przez program przy odpowiendnio ustawionej szczegółowości logów). Zakładając, że dane wejściowe do systemu mogą pochodzić z różnych źródeł (<i>część danych docierających od dostawc<ins>ów</ins></i>), warto, żebyśmy zachowywali informacje na temat pochodzenia tych danych (np. w nazwie pliku). Jeśli występowanie błędów zależne będzie od pochodzenia pomoże nam to zlokalizować problem, który może polegać na niespójnych założeniach co do formatu danych wejściowych.

b. Skrypt na serwerze powinnen być uruchomiany i monitorować zawartość folderu źródłowego przez cały czas. W związku z tym moją propozycją, zakładając serwer z systemem operacyjnym Linux, jest dodanie odpowiedniego zadania CRON, które w określonych interwałach czasowych, np. co 30 min, będzie weryfikować, czy skrypt jest uruchomiony i w przypadku negatywnej odpowiedzi uruchomi go ponownie. Uruchomienie skryptu powinno odbywać się w środowisku wirtualnym, wszystkie zależności skryptu opsiano w pliku ```requirements.txt```