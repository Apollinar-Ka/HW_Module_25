import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver  # подключение библиотеки
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = "https://petfriends.skillfactory.ru"
valid_email = "введите свой email"
valid_password = "введите свой пароль"

@pytest.fixture()
def login_and_get_list_mypets(web_browser):
    driver = web_browser
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@class="btn btn-success"]'))).click()
    wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT, u"У меня уже есть аккаунт"))).click()
    wait.until(EC.visibility_of_element_located(
        (By.ID, "email"))).send_keys(valid_email)
    wait.until(EC.visibility_of_element_located(
        (By.ID, "pass"))).send_keys(valid_password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    driver.implicitly_wait(10)
    if driver.current_url != f'{base_url}/all_pets':
        raise Exception("login error")

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/my_pets"]'))).click()

    # явное ожидание появления таблицы с моими питомцами
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "all_my_pets")))
    # Проверяем наличие карточек питомцев в таблице
    if element.text == "Вы пока не добавили ни одного питомца":
        raise Exception("Список моих питомцев пуст, проведение тестов невозможно!")

    driver.implicitly_wait(10)
    # считываем списки имен, пород и возрастов
    tag_data = driver.find_elements(By.TAG_NAME, 'td')
    names = [tag_data[i].text.lower() for i in range(0, len(tag_data), 4)]
    species = [tag_data[i].text for i in range(1, len(tag_data), 4)]
    age = [tag_data[i].text for i in range(2, len(tag_data), 4)]

    # Определяем количество питомцев из статистики пользователя:
    data_user = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    count_mypets = data_user[1].split(": ")

    # считываем массив с описанием питомцев, len(D_table)=len(data_pets) = количество питомцев
    D_table = driver.find_elements(By.CSS_SELECTOR, "tbody>tr")
    data_pets = [D_table[i].text.lower() for i in range(len(D_table))]

    # определяем количество карточек питомцев без фото
    pets_without_images = len(driver.find_elements(By.CSS_SELECTOR, 'img[src=""]'))

    # Возвращаем:  - количество питомцев из статистики,
    #              - массив с описанием питомцев, длина которого = количеству питомцев,
    #              - количество питомцев без фото,
    #              - список имен питомцев,
    #              - список видов/пород питомцев,
    #              - список возрастов питомцев.
    return count_mypets[1], data_pets, pets_without_images, names, species, age


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()  # получение объекта веб-драйвера для нужного браузера
    driver.set_window_size(1400, 1000)
    return driver


@pytest.fixture()
def web_browser(request, driver):
    browser = driver

    # Вернуть объект браузера
    yield browser

    # Этот код выполнится после отрабатывания теста:
    if request.node.rep_call.failed:
        # Сделать скриншот, если тест провалится:
        browser.execute_script("document.body.bgColor = 'white';")

        # Создаем папку screenshots и кладем туда скриншот с генерированным именем:
        browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

        # Для дебагинга, печатаем информацию в консоль
        print('URL: ', browser.current_url)
        print('Browser logs:')
        for log in browser.get_log('browser'):
            print(log)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep