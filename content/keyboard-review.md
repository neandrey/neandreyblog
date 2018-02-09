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
компьютерах с 64-разрядной архитектурой. Следуящая программа показывает как вы это можете сдллать.

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
в файле `/proc/cpuinfo`.Следующий листинг показывает как можно это сделать.

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