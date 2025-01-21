from datetime import datetime, date
import logging


logging.basicConfig(level=logging.DEBUG)


def check_data(date_str: str) -> bool:
    try:
        # отрезаем временную зону "+03:00"
        date_str_without_tz = date_str.split("T")[0]
        # Преобразуем строку в объект datetime
        # Указываем формат, соответствующий новой строке без временной зоны
        date_format = "%Y-%m-%d"
        parsed_date = datetime.strptime(date_str_without_tz, date_format).date()
        # Получаем текущую дату и время
        now = datetime.now().date()


        # Сравниваем даты
        if parsed_date > now:
            logging.info(f"{parsed_date} Дата в будущем")
            return False
        elif parsed_date < now:
            logging.info(f"{parsed_date} Дата в прошлом")
            return True
        else:
            logging.info(f"{parsed_date} Дата совпадает с текущей")
            return False
    except ValueError as e:
        logging.error(f"Строка не соответствует формату: {str(e)}")
        return False


if __name__ == '__main__':
    
    # Ваша строка с датой и временем
    date_str = "2025-01-18T11:30:00+03:00"
    print(check_data(date_str))