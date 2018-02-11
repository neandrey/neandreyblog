Title: Linux System Mining with Python
Date: 2018-02-04 10:20
Category: Python

В этой статье мы исследуем инструменты языка 
python для получения различной информации о 
работе системы Linux. Давайте начнем.

####Какой интерпритатор python?
Когда я говорю о python я ссылаюсь на CPython2 (2.7 если быть точным). Я должен упамянуть об
этом явно потому что тот же код не будет работает на python3 (3.3) и будет предоставлен
альтернативный код, объясняя различия. Просто чтобы убедиться, что у вас установлен CPython
введите 'python' или `python3` на терминале и вы должны увидеть подстроку python на своей 
дисплее.

####Примечание.
Пожалуйста заметьте, что все программы имеют первую строку `#!/usr/bin/env python` которая 
означает,что вы хотите использовать интерпритатор python для выполнения данного скрипта.
Если вы хотите сделать свой скрипт исполняемым используйте команду `chmod + x your-script.py`. 
Для выполнения вашего скрипта используйте команду `./your-script.py`

####Исследование модулей системы.
модуль `platform` в стандартной библиотеки имеет ряд функций которые позволяют нам возвращать
информацию о системных переменных. Давайте запустим наш интерпритатор `python` и выполним
некоторые из них, начнем с функции `platform.uname()`

        >>> import platform
        >>> platform.uname()
            ('Linux', 'fedora.echorand', '3.7.4-204.fc18.x86_64', '#1 SMP Wed Jan 23 16:44:29 UTC 2013', 'x86_64') 


Если вы в курсе о команде `uname` в системе Linux вы сразу поймете, что это функция является
интерфейсом данной команды. На python2 эта функция возвращает кортеж 
состоящий из: названия системы (названия Ядра), имени хоста, версии, релиза, разрядность машины и
информацию о процессоре. Вы можете получить доступ к отдельным атрибутам вот так:

        >>> platform.uname()[0]
            'Linux'
На Python 3, функция вернет именованный кортеж:

        >>> platform.uname()

        uname_result(system='Linux', node='fedora.echorand',
        release='3.7.4-204.fc18.x86_64', version='#1 SMP Wed Jan 23 16:44:29
        UTC 2013', machine='x86_64', processor='x86_64')
Поскольку возвращаемый результат - именованный кортеж, доступ к отдельным атребутам 
можно получить по имени, вместо того чтобы запоминать индекс.

        >>> platform.uname().system
            'Linux'
модуль `platform` так же имеет непосредственный доступ к вышеперечисленным атрибутам

        >>> platform.system()
            'Linux'

        >>> platform.release()
            '3.7.4-204.fc18.x86_64'
Функция ``linux_distribution()`` возвращает детали Linux дистрибутиве установленном на вашей машине.
Для примера взят дистрибутив Fedora 18 после вызова команда вернет:


        >>> platform.linux_distribution()
            ('Fedora', '18', 'Spherical Cow')
Результат возвращается в кортеже состоящем из имени дистрибутива, версии, и названием сборки.
Дистрибутивы поддерживающие вашу версию Python могут быть получены вызовом атрибута 

        >>> platform._supported_dists
        ('SuSE', 'debian', 'fedora', 'redhat', 'centos', 'mandrake',
        'mandriva', 'rocks', 'slackware', 'yellowdog', 'gentoo',
        'UnitedLinux', 'turbolinux')
Если вашего дистрибутива Linux нет в списке, тогда вы не увидите никакой информации из приведенного выше
вызова функции.

Последней функция из модуля `platform` мы рассмотрим ``architecture()``. Когда мы вызываем эту функцию без аргументов,
эта функция вернет кортеж с разрядностью архитектуры и типом исполняемого формата Python.

        >>> platform.architecture()
            ('64bit', 'ELF')
На 32-разрядных системах Linux вы увидите:

        >>> platform.architecture()
            ('32bit', 'ELF')
Вы получите тот же результат если укажите любой другой исполняемый файл:

        >>> platform.architecture(executable='/usr/bin/ls')
            ('64bit', 'ELF')
Вам предлагается изучить другие функции модуля `platform`, которые среди прочего позволяют найти текущуюю версию
Python которую вы используете. Если вы заинтересованы узнать как этот модуль извлекает информацию. 
Вам стоит рассмотреть файл lib\platform.py в каталоге с исходным кодом языка Python.

Модули `os` и `sys` так же предоставляют интерес для получения определенных системных атрибутов
таких как порядок следования байт. Далее мы выходим за рамки модулей стандартной библиотеки Python,
чтобы исследовать некоторые общие подходы для доступа к информации о системе Linux, доступной
через `proc` и `sysfs`. Следует отметить, что информация доступная через `proc` и `sysfs` может 
различаться на разных архитектурах и следовательно вы должны иметь это ввиду при написании сценариев.

####Информация о процессоре
Файл `/proc/cpuinfo` содержат информацию о процессоре на вашей системы. Для примера версия на команда.
когда вы выполняете эту программу на `python2` или `python3` вы должоны увидеть всё содержимое файла 
на своем монеторе.

    #! /usr/bin/env python
    """ print out the /proc/cpuinfo
    file
    """

    from __future__ import print_function

        with open('/proc/cpuinfo') as f:
        for line in f:
            print(line.rstrip('\n'))
В программе выше метод [rstrip()](https://www.tutorialspoint.com/python/string_rstrip.htm) 
удаляет конечные символы новой строки. 

Следуюший код показывает использования строкового мтеода 
[startswith()](https://www.tutorialspoint.com/python/string_startswith.htm) и
возвращает на дисплей модель вашего процессора.

    #! /usr/bin/env python

    """ Print the model of your
    processing units

    """

    from __future__ import print_function

    with open('/proc/cpuinfo') as f:
        for line in f:
            # Ignore the blank line separating the information between
            # details about two processing units
            if line.strip():
                if line.rstrip('\n').startswith('model name'):
                    model_name = line.rstrip('\n').split(':')[1]
                    print(model_name)
когда вы запустите эту программу вы должны увдеть назвние каждого процессорного модуля.

Для примера вот что получилось у меня:

    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz


Мы до сих пор видели несколько способов как определить архитектуру компьютерной системы в которой мы находимся.
Чтобы быть технически корректным оба этих подхода фактически сообщает об архитектуре
ядра в котором работает ваша система. Если ваш компьютер является 64-разрядным а работает на 32-разрядном ядре то эти 
методы сообщат вам о 32-разарядной архитектуре. Чтобы найти истенную архитектуру компьютера вам необходимо найти 
флаг `lm` в списке флагов в файле `/proc/cpuinfo`. Флаг `lm` обозначает длительный режим и присутствует только на 
компьютерах с 64-разрядной архитектурой. 
Следующий листинг показывает как вы можете это сделать.

    #! /usr/bin/env python

    """ 
    Find the real bit architecture
    """

    from __future__ import print_function

    with open('/proc/cpuinfo') as f:
        for line in f:
            # Ignore the blank line separating the information between
            # details about two processing units
            if line.strip():
                if line.rstrip('\n').startswith('flags') \
                        or line.rstrip('\n').startswith('Features'):
                    if 'lm' in line.rstrip('\n').split():
                        print('64-bit')
                    else:
                        print('32-bit')
Как мы уже видели чтение файла `/proc/cpuinfo` возможно с использованием простых текстовых методов.
Для того чтобы сделать чтение более удобным по отношению к другим программам использующие данные. 
Лучший способ создать структуру данных такую как словарь.
Идея простая если вы просмотрите содержимое  файла `/proc/cpuinfo` то можете заметить каждая обрабатываемая 
единица данных имеет пару ключ значение. 
(ранее мы выводили имя процессора здесь является ключем)
Информация о любых процессорных устройствах разделены друг от друга пустой строкой.
Проще построить словарь для которого каждое процессорное устройство используется как ключь.
Для каждого такого ключа значением является вся информация о соответствующем процессоре, предоставленная
в файле `/proc/cpuinfo`.
Следующий листинг показывает как можно это сделать:

    #!/usr/bin/env/ python

    """
    /proc/cpuinfo as a Python dict
    """
    from __future__ import print_function
    from collections import OrderedDict
    import pprint

    def cpuinfo():
        ''' Return the information in /proc/cpuinfo
        as a dictionary in the following format:
        cpu_info['proc0']={...}
        cpu_info['proc1']={...}
        '''

        cpuinfo=OrderedDict()
        procinfo=OrderedDict()

        nprocs = 0
        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    # end of one processor
                    cpuinfo['proc%s' % nprocs] = procinfo
                    nprocs=nprocs+1
                    # Reset
                    procinfo=OrderedDict()
                else:
                    if len(line.split(':')) == 2:
                        procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        procinfo[line.split(':')[0].strip()] = ''

    return cpuinfo

    if __name__=='__main__':
        cpuinfo = cpuinfo()
        for processor in cpuinfo.keys():
            print(cpuinfo[processor]['model name'])
            
Этот код использует  [OrderedDict](https://pymotw.com/2/collections/ordereddict.html)
вместо обычного словоря так что ключи и значения находятся в том порядке в котором они находятся
в файле. Следовательно данные для первого процессора за ним данные для второго и так далее (по порядку).
Если вы вызываете эту функцию то получите словарь в качестве возвращаемого значения.
Каждый ключ словоря является отдельным процессорным модулем.
Затем ва можете использовать цикл for для выбора нужной вам информации (как продемонстрировано в
блоке if __name__=='__main__').
Когда вы запустите программу вы еще раз увидите название каждого модуля процессора (как указано в вызове 
функции print(cpuinfo[processor]['model name']).

    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
    Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz


####Информация о памяти.
Аналогично /proc/cpuinfo файл /proc/meminfo содержит информацию о памяти установленной на вашем компьютере.
В следующей программе создается словарь с данными из этого файла.
Как вы видели ранее вы можете получить любую информацию используя её как ключ словоря.

    #!/usr/bin/env python

    from __future__ import print_function
    from collections import OrderedDict

    def meminfo():
        ''' Return the information in /proc/meminfo
        as a dictionary '''
        meminfo=OrderedDict()

        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        return meminfo

    if __name__=='__main__':
        #print(meminfo()) #выводит на печать все данные из файла /proc/meminfo

        meminfo = meminfo()
        print('Total memory: {0}'.format(meminfo['MemTotal']))
        print('Free memory: {0}'.format(meminfo['MemFree']))

Когда вы выполните программу вы должны увидеть что-то похожее на это.

    Total memory: 7897012 kB
    Free memory: 249508 kB
    
#### Сетевавя статистика.
Дальше мы исследуем сетевые устройства находящиеся на вашей компьютерной системе.
Мы будем извлекать название сетевого интерфейса и число байт полученных и переданных с момента 
последней перезагрузки системы.
Данная информация находится в файле /proc/net/dev. Если вы исследуете содержимое данного файла,
то заметите что первые две строчки содержат информационный заголовок - т.е. первая колонка этого файла 
имя сетевого интерфейса, а вторая и третья колонки число переданных и принятых байт(). 
Наш интерес здесь составляет выделение всех данных переданных и принятых от различных сетевых интерфейсов.
Следующий листинг показывает как мы можем извлечь информацию из файла /proc/net/dev.

    #!/usr/bin/env python
    from __future__ import print_function
    from collections import namedtuple

    def netdevs():
        ''' RX and TX bytes for each of the network devices '''

        with open('/proc/net/dev') as f:
            net_dump = f.readlines()

        device_data={}
        data = namedtuple('data',['rx','tx'])
        for line in net_dump[2:]:
            line = line.split(':')
            if line[0].strip() != 'lo':
                device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                    float(line[1].split()[8])/(1024.0*1024.0))

    return device_data

    if __name__=='__main__':

        netdevs = netdevs()
        for dev in netdevs.keys():
            print('{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))

Когда вы запустите эту программу вы увидите название интерфейса и общее число переданных и полученных байт с
момента последней перезагрузки системы.
    
    em1: 0.0 MiB 0.0 MiB
    wlan0: 2651.40951061 MiB 183.173976898 MiB
Возможно вы могли бы связать данную информацию с базой данных для написание своей собственной программы за
мониторингом сетевых данных.

####Процессы.
/proc содержит калоги для каждого работающего процесса.
Имя директории такое же как и ID запущенного процесса.
Следовательно, если вы сканируете /proc по всем каталогам у которых в название есть цифры, у вас будет список всех
запущенных процессов.
Функция process_list() в следующем листинге возвращает список с ID работающих процессов.
Длинна этого списка будет зависеть от количества работающих процессов на вашей системе как показано в
листинге ниже.

    #!/usr/bin/env python
    """
    List of all process IDs currently active
    """

    from __future__ import print_function
    import os
    
    def process_list():

        pids = []
        for subdir in os.listdir('/proc'):
            if subdir.isdigit():
                pids.append(subdir)

    return pids


    if __name__=='__main__':

        pids = process_list()
        print('Total number of running processes:: {0}'.format(len(pids)))
        
Вышепреведенная программа при выполнение покажет результат аналогичный этому:
    
    Total number of running processes:: 229
    
Каждый из каталогов в директории \\ содержит различную информацию о вызываемых командах,
используемызх библиотеках и прочем:

    #!/usr/bin/env python

    """
    Python interface to the /proc file system.
    Although this can be used as a replacement for cat /proc/... on the command line,
    its really aimed to be an interface to /proc for other Python programs.

    As long as the object you are looking for exists in /proc
    and is readable (you have permission and if you are reading a file,
    its contents are alphanumeric, this program will find it). If its a
    directory, it will return a list of all the files in that directory
    (and its sub-dirs) which you can then read using the same function.


    Example usage:

    Read /proc/cpuinfo:

    $ ./readproc.py proc.cpuinfo

    Read /proc/meminfo:

    $ ./readproc.py proc.meminfo

    Read /proc/cmdline:

    $ ./readproc.py proc.cmdline

    Read /proc/1/cmdline:

    $ ./readproc.py proc.1.cmdline

    Read /proc/net/dev:

    $ ./readproc.py proc.net.dev

    Comments/Suggestions:

    Amit Saha <@echorand>
    <http://echorand.me>

    """

    from __future__ import print_function
    import os
    import sys
    import re

    def toitem(path):
    """ Convert /foo/bar to foo.bar """
        path = path.lstrip('/').replace('/','.')
        return path

    def todir(item):
        """ Convert foo.bar to /foo/bar"""
        # TODO: breaks if there is a directory whose name is foo.bar (for
        # eg. conf.d/), but we don't have to worry as long as we are using
        # this for reading /proc
        return '/' + item.replace('.','/')

    def readproc(item):
        """
        Resolves proc.foo.bar items to /proc/foo/bar and returns the
        appropriate data.
        1. If its a file, simply return the lines in this file as a list
        2. If its a directory, return the files in this directory in the
        proc.foo.bar style as a list, so that this function can then be
        called to retrieve the contents
        """
        item = todir(item)

        if not os.path.exists(item):
            return 'Non-existent object'

        if os.path.isfile(item):
            # its a little tricky here. We don't want to read huge binary
            # files and return the contents. We will probably not need it
            # in the usual case.
            # utilities like 'file' on Linux and the Python interface to
            # libmagic are useless when it comes to files in /proc for
            # detecting the mime type, since the these are not on-disk
            # files.
            # Searching, i find this solution which seems to be a
            # reasonable assumption. If we find a '\0' in the first 1024
            # bytes of a file, we declare it as binary and return an empty string
            # however, some of the files in /proc which contain text may
            # also contain the null byte as a constituent character.
            # Hence, I use a RE expression that matches against any
            # combination of alphanumeric characters
            # If any of these conditions suffice, we read the file's contents

            pattern = re.compile('\w*')
            try:
                with open(item) as f:
                    chunk = f.read(1024)
                    if '\0' not in chunk or pattern.match(chunk) is not None:
                        f.seek(0)
                        data = f.readlines()
                        return data
                    else:
                        return '{0} is binary'.format(item)
            except IOError:
                return 'Error reading object'

        if os.path.isdir(item):
            data = []
            for dir_path, dir_name, files in os.walk(item):
                for file in files:
                    data.append(toitem(os.path.join(dir_path, file)))
            return data

    if __name__=='__main__':

        if len(sys.argv)>1:
            data = readproc(sys.argv[1])
        else:
            data = readproc('proc')
    
        if type(data) == list:
            for line in data:
                print(line)
        else:
            print(data)
            
####Блочные устройства.
В следующем программном листинге все блочные устройства читаются из виртуальной файловой системы
sysfs. Блочные устройства на вашем компьютере могут быть найдены в директории /sys/block.
Так же у вас может быть такие директории как /sys/block/sda, /sys/block/sdb.
Чтобы найти все блочные устройства надо выполнить сканирование \\ с помощью регулярного выражения 
в котором мы пишем интересующиее нас устройства.

    #!/usr/bin/env python

    """
    Read block device data from sysfs
    """

    from __future__ import print_function
    import glob
    import re
    import os

    # Add any other device pattern to read from
    dev_pattern = ['sd.*','mmcblk*']

    def size(device):
        nr_sectors = open(device+'/size').read().rstrip('\n')
        sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')
    
        # The sect_size is in bytes, so we convert it to GiB and then send it back
        return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

    def detect_devs():
        for device in glob.glob('/sys/block/*'):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    print('Device:: {0}, Size:: {1} GiB'.format(device, size(device)))

    if __name__=='__main__':
        detect_devs()

Если ва выполните эту программу то получите на выходе что-то подобное:

    Device:: /sys/block/sda, Size:: 465.761741638 GiB
    Device:: /sys/block/mmcblk0, Size:: 3.70703125 GiB
    
Когда явыполнял программу у меня была воткнута SD карта
и вы можете видеть что программа её обнаружила.

####Создание утилит командной строки.
Одной из основных особенностей утилит командной строки Linux является наличие
аргументов, которые позволяют настроить поведение программы.
Модуль argparse позваляет вашим программам иметь такой же интерфейс как и у программ командной строки Linux.
В следующей программе показано извлечение всех пользователей зарегеастрированных 
в вашей системе и печать их на терминале.

    #!/usr/bin/env python

    """
    Print all the users and their login shells
    """

    from __future__ import print_function
    import pwd


    # Get the users from /etc/passwd
    def getusers():
        users = pwd.getpwall()
        for user in users:
            print('{0}:{1}'.format(user.pw_name, user.pw_shell))

    if __name__=='__main__':
        getusers()
        
Когда вы запустите данную программу она напечатает всех пользователей в вашей системе и их оболочку для входа.

Теперь мы хотим чтобы пользователь программы мог выбрать хочет он видеть пользователей системы.
Мы увидем использование модуля argparse для реализации этой функции путем расширения предыдушего списка.

    #!/usr/bin/env python

    """
    Utility to play around with users and passwords on a Linux system
    """

    from __future__ import print_function
    import pwd
    import argparse
    import os

    def read_login_defs():

        uid_min = None
        uid_max = None

        if os.path.exists('/etc/login.defs'):
            with open('/etc/login.defs') as f:
                login_data = f.readlines()

            for line in login_data:
                if line.startswith('UID_MIN'):
                    uid_min = int(line.split()[1].strip())

                if line.startswith('UID_MAX'):
                    uid_max = int(line.split()[1].strip())

        return uid_min, uid_max

    # Get the users from /etc/passwd
    def getusers(no_system=False):

        uid_min, uid_max = read_login_defs()

        if uid_min is None:
            uid_min = 1000
        if uid_max is None:
            uid_max = 60000

        users = pwd.getpwall()
        for user in users:
            if no_system:
                if user.pw_uid >= uid_min and user.pw_uid <= uid_max:
                    print('{0}:{1}'.format(user.pw_name, user.pw_shell))
            else:
                print('{0}:{1}'.format(user.pw_name, user.pw_shell))

    if __name__=='__main__':

        parser = argparse.ArgumentParser(description='User/Password Utility')

        parser.add_argument('--no-system', action='store_true',dest='no_system',
                            default = False, help='Specify to omit system users')

        args = parser.parse_args()
        getusers(args.no_system)


При выполнении программы с опцией --help вы увидете справочное сообшение о работе программы и
используемых опциях.

    $ ./getusers.py --help
    usage: getusers.py [-h] [--no-system]

    User/Password Utility

    optional arguments:
        -h, --help   show this help message and exit
        --no-system  Specify to omit system users
Пример вызова программы выглядет следующим образом.

    $ ./getusers.py --no-system
    gene:/bin/bash
Когда вы передаете недопустимый параметр программа выводит предупреждение:

    $ ./getusers.py --param
    usage: getusers.py [-h] [--no-system]
    getusers.py: error: unrecognized arguments: --param
Попробуем вкратце понять, как работает argparse в программе. 
Инструкция: parser = argparse.ArgumentParser (description = 'User / Password Utility>) 
создает новый объект ArgumentParser с необязательным параметром описывающим что делает данная программа.
Затем добавляем аргументы, которые мы хотим, 
чтобы программа распознавала с помощью метода add_argument () 
в следующем выражении: parser.add_argument 
('--no-system', action = 'store_true', dest = 'no_system', default = False, help = 'Specify to omit system usersэ).
Первый параметр этого метода - это опция, которую пользователь программы 
будет подставлять в качестве аргумента при вызове программы, 
следующий параметр action = store_true указывает, что это логическая опция. 
То есть присутствие или отсутствие опции влияет на поведение программы. 
Параметр dest указывает переменную, в которой значение, которое значение этой опции будет доступно программе. 
Если эта опция не указана пользователем, значением по умолчанию является значение False, 
которое указывается параметром default = False, а последним параметром является справочное сообщение,
отображаемое программой об этой опции. Наконец, аргументы анализируются с использованием метода parse_args():
args = parser.parse_args (). Как только разбор выполняется, значения параметров, 
предоставленных пользователем, могут быть получены с использованием 
синтаксиса args.option_dest, где option_dest - это переменная dest, которую вы указали при настройке аргументов. 
Это утверждение: getusers (args.no_system) вызывает функцию getusers () с значением параметра для no_system, 
предоставленным пользователем. Следующая программа показывает, как вы можете указать параметры, 
которые позволяют пользователю указывать небулевые предпочтения для вашей программы. 

Эта программа является переписью листинга 6, с дополнительной опцией для указания сетевого устройства, 
которое может вас заинтересовать.

    #!/usr/bin/env python
    from __future__ import print_function
    from collections import namedtuple
    import argparse

    def netdevs(iface=None):
    ''' RX and TX bytes for each of the network devices '''

        with open('/proc/net/dev') as f:
            net_dump = f.readlines()

        device_data={}
        data = namedtuple('data',['rx','tx'])
        for line in net_dump[2:]:
            line = line.split(':')
            if not iface:
                if line[0].strip() != 'lo':
                    device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                        float(line[1].split()[8])/(1024.0*1024.0))
            else:
                if line[0].strip() == iface:
                    device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                        float(line[1].split()[8])/(1024.0*1024.0))
        return device_data

    if __name__=='__main__':

        parser = argparse.ArgumentParser(description='Network Interface Usage Monitor')
        parser.add_argument('-i','--interface', dest='iface',
                            help='Network interface')

        args = parser.parse_args()

        netdevs = netdevs(iface = args.iface)
        for dev in netdevs.keys():
            print('{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))
Когда вы выполняете программу без каких-либо аргументов, 
она ведет себя точно так же, как и предыдущая версия. 
Однако вы также можете указать сетевое устройство, 
которое вас может заинтересовать. Например:

    $ ./net_devs_2.py

    em1: 0.0 MiB 0.0 MiB
    wlan0: 146.099492073 MiB 12.9737148285 MiB
    virbr1: 0.0 MiB 0.0 MiB
    virbr1-nic: 0.0 MiB 0.0 MiB

    $ ./net_devs_2.py  --help
    usage: net_devs_2.py [-h] [-i IFACE]

    Network Interface Usage Monitor

    optional arguments:
        -h, --help            show this help message and exit
        -i IFACE, --interface IFACE
                        Network interface

    $ ./net_devs_2.py  -i wlan0
    wlan0: 146.100307465 MiB 12.9777050018 MiB
С помощью этой статьи вы, возможно, смогли написать один или несколько полезных скриптов для себя, 
которые вы хотите использовать каждый день, как и любую другую команду Linux.
Самый простой способ сделать этот скрипт выполнимым и настроить псевдоним(alias) 
оболочки для этого скрипта. 
Вы также можете удалить расширение .py 
и поместить этот файл в стандартное местоположение исполняемых программ, 
например /usr /local /sbin.

####Другие полезные библиотечные модули стандартной библиотеки.
Помимо стандартных библиотечных модулей, 
которые мы уже рассмотрели в этой статье, существует ряд других стандартных модулей, 
которые могут быть полезны: subprocess, ConfigParser, readline and curses. 
####Что дальше? 
На этом этапе, в зависимости от вашего собственного опыта работы с Python и изучения 
внутренних компонентов Linux, вы можете следовать одному из следующих путей. Если вы пишете 
много сценариев командной оболочки или командных конвейеров 
для изучения различных внутренних элементов
Linux, взгляните на Python. Если вам нужен более простой способ написать собственные 
скрипты для выполнения различных задач, взгляните на Python. Наконец, если вы использовали
Python для программирования других видов Linux, получайте удовольствие от использования 
Python для изучения внутренних компонентов Linux.

[Оригинал стастьи]( http://echorand.me/linux-system-mining-with-python.html)