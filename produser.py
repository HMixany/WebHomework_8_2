import pika
from faker import Faker

from models import User

fake = Faker('uk-Ua')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange = 'web_homework_8_2'
queue_name = 'web_homework_8_past_2'

channel.exchange_declare(exchange=exchange, exchange_type='direct')     # створюємо біржу
channel.queue_declare(queue=queue_name, durable=True)       # durable=True збереже черги якщо перезапуститься контейнер
channel.queue_bind(exchange=exchange, queue=queue_name)     # під'єднали бірржу до черги


def create_users(nums: int):
    for i in range(nums):
        user = User(fullname=fake.name(), email=fake.email()).save()

        channel.basic_publish(exchange=exchange, routing_key=queue_name, body=str(user.id).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()


if __name__ == '__main__':
    create_users(10)
