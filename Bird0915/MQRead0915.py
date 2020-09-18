import functools
import pika
import Setting as ST
from Bird0915.Assignment0915 import Assign


def MQread():
    OK = True
    while OK:
        try:
            OK = False
            connParameters = ST.IN_CONPARAM
            mqconnect = pika.BlockingConnection(connParameters)
            channel = mqconnect.channel()
            for method_frame, properties, body in channel.consume('queue.regin'):
                mqconnect.add_callback_threadsafe(
                    functools.partial(Assign, channel, method_frame.delivery_tag, properties, body))
            OK = True
        except Exception as e:
            print(e)
            continue
        except pika.exceptions.ConnectionClosedByBroker:
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError:
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            continue
        finally:
            # channel.basic_ack(method_frame.delivery_tag)
            mqconnect.close()

    pass


MQread()


