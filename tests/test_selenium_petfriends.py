

def test_count_mypets(login_and_get_list_mypets):
    """проверка п.1 - Присутствуют все питомцы"""
    count_mypets, data_pets, _, _, _, _ = login_and_get_list_mypets
    assert int(count_mypets) == len(data_pets)


def test_half_with_photo(login_and_get_list_mypets):
    """проверка п.2 - Хотя бы у половины питомцев есть фото"""
    count_mypets, _, pets_without_images, _, _, _ = login_and_get_list_mypets
    assert int(count_mypets) - pets_without_images >= int(count_mypets) / 2, "Больше чем у половины питомцев отсутствует фото"


def test_all_mypets_have_description(login_and_get_list_mypets):
    """проверка п.3 - у всех питомцев есть имя, возраст и порода"""
    _, _, _, names, species, age = login_and_get_list_mypets
    assert '' not in names, "В карточках питомцев присутствует пустое поле ИМЯ"
    assert '' not in species, "В карточках питомцев присутствует пустое поле ПОРОДА"
    assert '' not in age, "В карточках питомцев присутствует пустое поле ВОЗРАСТ"


def test_all_mypets_have_different_names(login_and_get_list_mypets):
    """проверка п.4 - У всех питомцев разные имена"""
    _, _, _, names, _, _ = login_and_get_list_mypets
    assert len(names) == len(set(names)), "В таблице присутствуют питомцы с одинаковым именем"


def test_mypets_have_no_identical_records(login_and_get_list_mypets):
    """проверка п.5 - в списке нет повторяющихся питомцев"""
    _, data_pets, _, _, _, _  = login_and_get_list_mypets
    assert len(data_pets) == len(set(data_pets)), "В таблице присутствуют повторяющиеся питомцы (имя, возраст, порода)"
