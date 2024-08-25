from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_petfriends(driver):
    # Добавляем неявные ожидания
    driver.implicitly_wait(5)

    # Открываем стартовую страницу
    driver.get("https://petfriends.skillfactory.ru/")

    # Нажимаем на кнопку Зарегистрироваться
    btn_newuser = driver.find_element(By.XPATH, "(//button[@onclick=\"document.location='/new_user';\"])")
    btn_newuser.click()

    # Нажимаем на ссылку У меня уже есть аккаунт
    btn_exist_acc = driver.find_element(By.LINK_TEXT, "У меня уже есть аккаунт")
    btn_exist_acc.click()

    # Вводим почту
    field_email = driver.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("lady.pantelyuk@yandex.ru")

    # Вводим пароль
    field_pass = driver.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("Vsirf000")

    # Нажимаем Войти
    btn_submit = driver.find_element(By.XPATH, "(//button[@type='submit'])")
    btn_submit.click()
    # Проверяем что открылась нужная страница с карточками всех питомцев
    assert driver.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"

    # Проверяем что у всех питомцев есть имя, фото и возраст
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_all_pets_exists(driver):
    # Добавляем явные ожидания
    wait = WebDriverWait(driver, 5)

    # Вводим email
    wait.until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, 'email').send_keys('lady.pantelyuk@yandex.ru')

    # Вводим пароль
    wait.until(EC.presence_of_element_located((By.ID, "pass")))
    driver.find_element(By.ID, 'pass').send_keys('Vsirf000')

    # Нажимаем на кнопку входа в аккаунт
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Нажимаем на кнопку фильтрации моих питомцев
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Находим все имена, все картинки, все описания питомцев
    names = driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[1])')
    images = driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/th/img)')
    kind = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    # Находим кол-во питомцев из статистики и из таблицы
    pets_number = driver.find_element(By.CSS_SELECTOR, "div.\\.col-sm-4.left").text.split('\n')[1].split(': ')[1]
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # Проверяем все ли питомцы присутствуют
    assert int(pets_number) == len(pets_count)

    # Высчитываем кол-во питомцев с фото
    photo_count = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            photo_count += 1

    # Проверяем, что питомцев с картинками больше половины
    assert photo_count > len(pets_count) / 2

    # Проверяем, что у всех питомцев есть имя, возраст и порода
    for i in range(len(names)):
        assert names[i].text != ''
        assert kind[i].text != ''
        assert age[i].text != ''

    # Проверяем, что клички питомцев не повторяются
    n = len(names)
    for i in range(n - 1):
        for j in range(i + 1, n):
            assert names[i].text != names[j].text
