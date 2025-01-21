import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import logging
import csv
from utils.check_datetime import check_data

# Включение логирования
logging.basicConfig(level=logging.DEBUG)


def paginate_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, proxy={
            "server": "http://46.8.110.242:1050",
            "username": "LO7M5x",
            "password": "CjPnAwhoLU"
        })

        # context = browser.new_context()
        # page = context.new_page()
        page = browser.new_page()

        # Переход на нужную страницу
        page.goto(
            'https://www.aiscore.com/ru/basketball/tournament-national-basketball-league/jw34kgpspf1ko92', wait_until="domcontentloaded"
        )  # Замените на ваш URL

        # Функция для перехода на конкретную страницу по номеру
        def go_to_page(page_number):
            # Используем XPath для поиска кнопки с номером страницы
            page_button = page.query_selector(
                f'xpath=//li[contains(@class, "number") and text()="{page_number}"]')
            if page_button and page_button.is_visible() and page_button.is_enabled():
                page_button.click(button="left")

                print(f'Кнопка страницы {page_number} нажата')
                # Ожидание обновления данных
                page.wait_for_selector(
                    f'xpath=//li[contains(@class, "number active") and text()="{
                        page_number
                    }"]', state='visible', timeout=60000
                )
            else:
                print(
                    f'Кнопка страницы {page_number} не найдена или недоступна'
                )

        page.wait_for_selector(".el-pagination",  state="visible")
        page_buttons = page.query_selector_all(
            '.el-pagination .el-pager .number')
        logging.info(f"Всего страниц: {page_buttons[-1].text_content()}")

        time.sleep(2)

        for i in range(4, int(page_buttons[-1].text_content())+1)[:2]:  # для тестов берем только две страницы.
            go_to_page(i)
            time.sleep(1)
            elements = page.query_selector_all(
                "//div[@class='matches']//div[@class='flex items']")
            logging.info(f"Строк на странице: {len(elements)}")
            for element in elements:
                # берем дату из селектора а не из text
                what_date = check_data(element.query_selector(
                    "meta[itemprop='startDate']").get_attribute('content'))
                logging.info(f"Дата: {what_date}")
       
                if what_date:
                    # в element берем ссылку на коэффициенты
                    link = element.query_selector(
                        "//a[@title='Коэффициенты']"
                    )
                    href = link.get_attribute("href")

                    with page.context.expect_page() as new_page_info:
                        page.evaluate(
                            f"window.open('https://www.aiscore.com/{href}')"
                        )

                    new_page = new_page_info.value

                    new_page.bring_to_front()

                    # заголовок страницы в нем находится дата и названия команд которые играют
                    title = new_page.title()
                    # Строки поставщиков коэффициентов
                    # Ожидаем появления
                    new_page.wait_for_selector("div.flex.w100.borderBottom")
                    # присваиваем в переменную
                    row_elements = new_page.query_selector_all("div.flex.w100.borderBottom")
                    # выбираем второй
                    open_rate = row_elements[1].query_selector("div.box.flex.w100.brr.openingBg1").inner_text().replace("\n", "-")
                    prematch_rate = row_elements[1].query_selector("div.box.flex.w100.brr.preMatchBg1").inner_text().replace("\n", "-")
                    modal_window = row_elements[1].query_selector(".iconfont.icon-youjiantou")
                    modal_window.click()
                    # print(len(row_elements))

                    # ожидаем появления модального окна с таблицей
                    new_page.wait_for_selector(".el-dialog__body")

                    dialog_body = new_page.query_selector(".el-dialog__body")
                    if dialog_body:
                        # кнопка переключения на таблицу Тотал Очков
                        total_points = new_page.locator(".el-dialog__body").get_by_text("Тотал Очков")
                        if total_points.count() > 0:
                            # Кликаем по кнопке Тотал Очков
                            total_points.click()
                            logging.info("Клик по 'Тотал Очков' выполнен.")

                            # ожидаем таблицу
                            new_page.wait_for_selector(".el-table__body")
                            # ожидание загрузки таблицы
                            time.sleep(5)

                            # Извлечение данных из таблицы
                            rows = new_page.query_selector_all(".el-table__row")
                            logging.info(f"строк: {len(rows)}")
                            data = []

                            for row in rows:
                                row.wait_for_selector("td", state="visible")
                                cells = row.query_selector_all("td")
                                # logging.info(len(cells))
                                first_data =  [title, open_rate, prematch_rate]
                                row_data = [cell.inner_text().strip() for cell in cells]
                                # добавляем title к каждой строчке данных
                                first_data.extend(row_data)
                                data.append(first_data)
                                logging.info(first_data)
                                # new_page.wait_for_timeout(500)

                            with open("filename.csv", mode="a", newline="", encoding="utf-8") as file:
                                writer = csv.writer(file)
                                writer.writerow(["title", "open_rate", "prematch_rate", "time", "score", "total", "max", "min"])  # Заголовки столбцов
                                writer.writerows(data)
                            logging.info("Данные сохранены")
                    # Закрываем новую вкладку
                    new_page.close()

                    page.wait_for_timeout(1000)

        # Закрытие браузера
        browser.close()

# Запуск функции
paginate_with_playwright()
