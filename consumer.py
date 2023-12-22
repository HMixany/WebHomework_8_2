import sys
import os

import pika

from models import User


def sending_letter(email):
    print(f"На адресу  {email} відправлено лист")


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    queue_name = 'web_homework_8_past_2'
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        user = User.objects(id=pk, completed=False).first()
        if user:
            sending_letter(user.email)
            user.update(set__completed=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    # consume слухає і коли баче що щось прийщло, викликає callback

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
