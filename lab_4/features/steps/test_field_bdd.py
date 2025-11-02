from behave import given, when, then
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field import field

@given('список товаров с различными полями')
def step_given_product_list(context):
    context.products = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'},
        {'title': None, 'price': 1500},
        {'price': 3000}
    ]

@when('я извлекаю поле "{field_name}"')
def step_when_extract_single_field(context, field_name):
    context.result = list(field(context.products, field_name))

@then('я получаю список значений этого поля')
def step_then_get_values_list(context):
    expected = ['Ковер', 'Диван для отдыха']
    assert context.result == expected, f"Ожидалось {expected}, получено {context.result}"

@given('список товаров с названиями и ценами')
def step_given_products_with_prices(context):
    context.products = [
        {'title': 'Ковер', 'price': 2000},
        {'title': 'Диван', 'price': 5000},
        {'title': 'Стул', 'price': 1000}
    ]

@when('я извлекаю поля "{field1}" и "{field2}"')
def step_when_extract_multiple_fields(context, field1, field2):
    context.result = list(field(context.products, field1, field2))

@then('я получаю список словарей с этими полями')
def step_then_get_dicts_list(context):
    expected = [
        {'title': 'Ковер', 'price': 2000},
        {'title': 'Диван', 'price': 5000},
        {'title': 'Стул', 'price': 1000}
    ]
    assert context.result == expected

@given('список товаров с отсутствующими значениями')
def step_given_products_with_missing_values(context):
    context.products = [
        {'title': 'Товар 1', 'color': 'red'},
        {'title': None, 'color': 'blue'},
        {'color': 'green'}
    ]

@when('я фильтрую по полю с пропущенными значениями')
def step_when_filter_with_missing_values(context):
    context.result = list(field(context.products, 'title'))

@then('пропущенные значения исключаются из результата')
def step_then_missing_values_excluded(context):
    assert context.result == ['Товар 1']