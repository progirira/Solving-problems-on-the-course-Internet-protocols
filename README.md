# Solving-problems-on-the-course-Internet-protocols
__Решение задач для курса "Протоколы Интернет"__
__Задача №1__
Трассировка автономных систем. Пользователь вводит доменное имя
или IP адрес. Осуществляется трассировка до указанного узла (например, с использованием
tracert), т. е. мы узнаем IP адреса маршрутизаторов, через которые проходит пакет. Необходимо определить к какой автономной системе относится каждый из полученных IP адресов
маршрутизаторов. Для определения номеров автономных систем обращаться к базам данных
региональных интернет регистраторов.
Выход: для каждого IP-адреса – вывести результат трассировки (или кусок результата до появления ***), для "белых" IP-адресов из него указать номер автономной системы.
В итоге должна получиться такая таблица
№ по порядку IP AS + определять страну и провайдера.
Стоимость = 10 баллов.