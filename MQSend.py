# coding=utf-8
import pika
import Setting as ST

# def send2MQRegister(uid, xuehao, result, name, type):
#     try:
#         connParameters = ST.OUT_CONPARAM
#         mqconnect = pika.BlockingConnection(connParameters)
#         channel = mqconnect.channel()
#         channel.basic_publish(exchange='',
#                               properties=pika.BasicProperties(
#                                   headers={'uid': uid,
#                                            'success': result,
#                                            'xuehao': xuehao,
#                                            'name': name,
#                                            'type': type}  # Add a key/value header
#                               ),
#                               body=[],
#                               routing_key='queue.regout')
#         print("sent 1 response")
#     except Exception as e:
#         print(e)
#     finally:
#         mqconnect.close()
#
#
# def send2MQLogin(uid, name, success, bestId, type):
#     try:
#         connParameters = ST.OUT_CONPARAM
#         mqconnect = pika.BlockingConnection(connParameters)
#         channel = mqconnect.channel()
#         channel.basic_publish(exchange='',
#                               properties=pika.BasicProperties(
#                                   headers={'uid': uid,
#                                            'success': success,
#                                            'xuehao': bestId,
#                                            'name': name,
#                                            'type': type}  # Add a key/value header
#                               ),
#                               body=[],
#                               routing_key='queue.regout')
#         print("sent 1 response")
#     except Exception as e:
#         print(e)
#     finally:
#         mqconnect.close()

def send2MQRegister(uid, xuehao, result, name, type):
    try:
        c = pika.PlainCredentials(user_out, password_out)
        connParameters = (
            pika.ConnectionParameters(host=host1, virtual_host=vhost, credentials=c),
            pika.ConnectionParameters(host=host2, virtual_host=vhost, credentials=c),
            pika.ConnectionParameters(host=host3, virtual_host=vhost, credentials=c)
            )
        mqconnect = pika.BlockingConnection(connParameters)
        channel = mqconnect.channel()
        channel.basic_publish(exchange='',
                              properties=pika.BasicProperties(
                                  headers={'uid': uid,
                                           'success': result,
                                           'xuehao': xuehao,
                                           'name': name,
                                           'type': type}  # Add a key/value header
                              ),
                              body=[],
                              routing_key='queue.regout')
    except Exception as e:
        print(e)
    finally:
        mqconnect.close()


def send2MQLogin(uid, name, success, bestId, type):
    try:
        c = pika.PlainCredentials(user_out, password_out)
        connParameters = (
            pika.ConnectionParameters(host=host1, virtual_host=vhost, credentials=c),
            pika.ConnectionParameters(host=host2, virtual_host=vhost, credentials=c),
            pika.ConnectionParameters(host=host3, virtual_host=vhost, credentials=c)
            )
        mqconnect = pika.BlockingConnection(connParameters)
        channel = mqconnect.channel()
        channel.basic_publish(exchange='',
                              properties=pika.BasicProperties(
                                  headers={'uid': uid,
                                           'success': success,
                                           'xuehao': bestId,
                                           'name': name,
                                           'type': type}  # Add a key/value header
                              ),
                              body=[],
                              routing_key='queue.regout')
    except Exception as e:
        print(e)
    finally:
        mqconnect.close()