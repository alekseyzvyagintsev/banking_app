# Документация по банковскому приложению

## Модуль masks.py

### Функция get_mask_card_number
```python
def get_mask_card_number(card_number: Optional[int] = None) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты в виде 16-ти значного числа
    и выводит замаскированный вариант в формате XXXX XX** **** XXXX
    """
```

### Функция get_mask_account
```python
def get_mask_account(account_number: Optional[int] = None) -> str:
    """
    Функция принимает на вход 20-ти значное число (номер счета)
    и возвращает маску номера по правилу **XXXX
    """
```

## Модуль utils.py

### Функция get_json_data
```python
def get_json_data(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
```

### Функция get_csv_data
```python
def get_csv_data(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до csv-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
```

### Функция get_xlsx_data
```python
def get_xlsx_data(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до excel-файла
    и возвращает DataFrame с финансовыми транзакциями.
    Если файл пустой или путь не верный, возвращает пустой список.
    """
```

### Функция search_operations
```python
def search_operations(operations_list: list, search_string: str) -> list:
    """
    Функция принимает на вход список словарей с данными о банковских операциях
    и строку поиска, а возвращать список словарей, у которых в описании есть данная строка.
    """
```

### Функция count_operations_by_category
```python
def count_operations_by_category(operations_list_for_count: list, categories_list: list) -> dict[Any] | dict[Any, int]:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращать словарь, в котором ключи — это названия категорий, а значения — это количество операций
    в каждой категории. Категории операций хранятся в поле description.
    """
```

### Функция read_user_settings
```python
def read_user_settings(file_path: str) -> dict:
    """Функция для получения курса акций из входящего списка акций."""
```

## Модуль processing.py

### Функция filter_by_state
```python
def filter_by_state(list_of_actions: list[dict[str, Any]], state: Optional[str] = "EXECUTED") -> list[Any]:
    """
    принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
```

### Функция sort_by_date
```python
def sort_by_date(list_of_actions: Iterable[dict[str, Any]], descending: Optional[bool] = True) -> list[dict[str, Any]]:
    """
    принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """
```

### Функция filter_by_description
```python
def filter_by_description(
    list_of_actions: Iterable[dict[str, Any]], search_string: str
) -> list[dict[str, Any]] | None:
    """
    Функция принимает список словарей и слово для фильтрации списка транзакций,
    Функция возвращает новый список, отсортированный по предложенному слову.
    """
```

### Функция calculate_total_expense
```python
def calculate_total_expense(df: pd.DataFrame) -> float:
    """общее суммирование расходов"""
```

### Функция group_expenses_by_category
```python
def group_expenses_by_category(df: pd.DataFrame, top_n=7) -> list:
    """группировка расходов по основным категориям"""
```

### Функция get_transfers_and_cash
```python
def get_transfers_and_cash(df: pd.DataFrame) -> list:
    """Функция для получения переводов и наличных."""
```

### Функция calculate_total_income
```python
def calculate_total_income(df: pd.DataFrame) -> float:
    """общее суммирование доходов"""
```

### Функция group_income_by_category
```python
def group_income_by_category(df: pd.DataFrame, top_n=7) -> List[dict]:
    """группировка доходов по основным категориям"""
```

### Функция sort_by_descending
```python
def sort_by_descending(data: List[Dict]) -> List[Dict]:
    """сортировать по убыванию"""
```

## Модуль reports.py

### Функция spending_by_category
```python
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
```

## Модуль services.py

### Функция investment_bank
```python
def investment_bank(month: str, transactions: list, limit: int) -> float:
    """
    Функция позволяет копить через округление трат.
    Можно задать комфортный порог округления: 10, 50 или 100 ₽.
    Траты округляются, и разница между фактической суммой трат по карте
    и суммой округления попадает насчет «Инвесткопилки».
    """
```

## Модуль generators.py

### Функция filter_by_currency
```python
def filter_by_currency(
    list_of_actions: Iterable[dict[str, Any]], currency_code: Optional[str] = None
) -> Iterator[Any] | list[dict[str, Any]]:
    """
    Фильтр списка транзакций по типу валюты.
    На вход принимает список транзакций.
    На выходе возвращает отфильтрованный список транзакций.
    """
```

### Функция transaction_descriptions
```python
def transaction_descriptions(
    list_of_actions: Optional[Iterable[dict[str, Any]]] = None,
) -> Generator[Any, str | None, Iterator[Any] | None]:
    """
    Фильтр списка транзакций.
    На вход принимает список транзакций.
    На выход отдает список с описаниями транзакций.
    """
```

### Функция card_number_generator
```python
def card_number_generator(start: int = 1, stop: int = 9999999999999999) -> Generator[str, Any, None]:
    """
    Простой генератор номеров кредитных карт.
    На вход принимает два числа от 1 до 16-ти знаков.
    На выход отдает список номеров в указанном диапазоне,
    в формате "ХХХХ ХХХХ ХХХХ ХХХХ"
    """
```

## Модуль external_api.py

### Функция returns_the_transaction_amount
```python
def returns_the_transaction_amount(transaction: Any) -> Any:
    """
    Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
    тип данных — float. Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
    Для конвертации валюты воспользуйтесь Exchange Rates Data API: https://apilayer.com/exchangerates_data-api.
    """
```

### Функция fetch_exchange_rates
```python
def fetch_exchange_rates(currencies: list[str]) -> list[dict]:  # [CurrencyRate]
    """Функция для получения курса валют из входящего списка валют."""
```

### Функция fetch_stock_prices
```python
def fetch_stock_prices(stocks: list) -> list[dict]:
    """Функция для получения курса акций из входящего списка акций."""
```

## Модуль views.py

### Функция generate_report
```python
def generate_report(date_str: str, period: str = "M") -> str:
    """
    Функция формирующая json - ответ для страницы событий на портале банка.
    Ответ содержит в себе:
    Раздел расходов за период
    1. Все расходы
    2. В категории Основные - Топ-7 расходов
    3. В категории Остальное - Переводы и наличные
    Раздел поступлений за период
    1. Все поступления
    2. В категории Основные - Топ-7 поступлений отсортированные по убыванию
    """
```

### Функция determine_period
```python
def determine_period(date_obj: datetime.datetime, period: str) -> Tuple[datetime.date, datetime.date]:
    """
    Формирование периодов для фильтрации DataFrame.
    Можно выбрать:
    W - неделя, на которую приходится дата.
    M - месяц, на который приходится дата.
    Y - год, на который приходится дата.
    ALL - все данные до указанной даты.
    """
```

### Функция filter_data
```python
def filter_data(df: pd.DataFrame, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """
    Фильтрация данных по выбранному периоду W, M, Y или ALL
    """
```

## Модуль widget.py

### Функция mask_account_card
```python
def mask_account_card(account_card: Optional[str] = None) -> str:
    """
    Принимает один аргумент — строку, содержащую тип и номер карты или счета.
    Возвращать строку с замаскированным номером.
    """
```

### Функция get_date
```python
def get_date(date_and_time: Optional[str] = None) -> str:
    """
    принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407" (ISO8601)
    и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
    """
```
