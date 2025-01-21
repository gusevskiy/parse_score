"""
Отдельный вспомогательный скрипт.
Простая проверка прокси адреса. ЗАпрос без прокси и запрос с прокси.
ip разные
"""

import requests
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
)
logger = logging.getLogger(__name__)

# Константы
MYIP_URL = "https://api.myip.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def check_proxy_connection(proxy):
    """
    Проверяет, работает ли прокси, сравнивая IP-адреса.
    Возвращает True, если прокси работает (IP-адреса разные), иначе False.
    """
    try:
        # Запрос без прокси
        response_without_proxy = requests.get(MYIP_URL)
        response_without_proxy.raise_for_status()
        ip_without_proxy = response_without_proxy.json()["ip"]
        logger.info(f"Без прокси: {response_without_proxy.json()}")

        # Запрос с прокси
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        headers = {"User-Agent": USER_AGENT}
        response_with_proxy = requests.get(MYIP_URL, headers=headers, proxies=proxies)
        response_with_proxy.raise_for_status()
        ip_with_proxy = response_with_proxy.json()["ip"]
        logger.info(f"C прокси: {response_with_proxy.json()}")


        # Сравнение IP-адресов
        return ip_without_proxy != ip_with_proxy

    except requests.RequestException as e:
        logger.error(f"Ошибка при проверке прокси: {e}")
        return False

if __name__ == '__main__':
    proxy = "LO7M5x:CjPnAwhoLU@46.8.110.242:1050"
    result = check_proxy_connection(proxy)
    logger.info(f"Прокси работает: {result}")
