import json


def format_operation(operation):
    formatted_date = operation['date'].split('T')[0]
    operation_amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']
    description = operation['description']
    card_number = operation.get('from', '')
    masked_card_number = f'XXXX XX** **** {card_number[-4:]}' if card_number else ''
    account_number = operation.get('to', '')
    masked_account_number = f'**{account_number[-4:]}' if account_number else ''
    state = operation.get('state', 'UNKNOWN')

    formatted_operation = f'{formatted_date.replace("-", ".")} {description}\n{masked_card_number} -> Счет {masked_account_number}\n{operation_amount} {currency} ({state})'
    return formatted_operation


def main():
    with open('C:\\Users\\kutalov\\Desktop\\Coursework Basics of backend development\\operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    executed_operations = [operation for operation in data if operation.get('state') in ['EXECUTED']]
    sorted_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)
    last_5_operations = sorted_operations[:5]

    for operation in last_5_operations:
        formatted_operation = format_operation(operation)
        print(formatted_operation)

# Опционально, вы можете также добавить этот код после цикла for
# print("Finished processing operations")  # Это для отладки

if __name__ == "__main__":
    main()