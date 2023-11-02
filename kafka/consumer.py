import sys
import os
from config import ConfigEnum
from confluent_kafka import Consumer, KafkaException, KafkaError
import json 
import serial, time

if __name__ == '__main__':
    clKfkaTopic = (os.environ['CLOUDKARAFKA_TOPIC'] if 'CLOUDKARAFKA_TOPIC' in os.environ else ConfigEnum.CLOUDKARAFKA_TOPIC.value)
    topics = clKfkaTopic.split(",")        
    # ser = serial.Serial('/dev/ttyUSB0', 9600)
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        'client.id': 'python1Client',
        'bootstrap.servers': (os.environ['CLOUDKARAFKA_BROKERS'] if 'CLOUDKARAFKA_BROKERS' in os.environ else ConfigEnum.CLOUDKARAFKA_BROKERS.value),
        'group.id': "%s-consumer2" % (os.environ['CLOUDKARAFKA_USERNAME'] if 'CLOUDKARAFKA_USERNAME' in os.environ else ConfigEnum.CLOUDKARAFKA_USERNAME.value),
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
	    'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': (os.environ['CLOUDKARAFKA_USERNAME'] if 'CLOUDKARAFKA_USERNAME' in os.environ else ConfigEnum.CLOUDKARAFKA_USERNAME.value),
        'sasl.password': (os.environ['CLOUDKARAFKA_PASSWORD'] if 'CLOUDKARAFKA_PASSWORD' in os.environ else ConfigEnum.CLOUDKARAFKA_PASSWORD.value)
    }

    c = Consumer(**conf)
    c.subscribe(topics)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    # Error
                    raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                print(msg.value())
                if "sudo systemctl suspend" in msg.value():
                	print "a suspender vellacos"
                	# os.system("sudo systemctl suspend")
                        os.system("sudo shutdown now")
                        c.close()
                elif ("parameters" in msg.value()):
                    res = json.loads(msg.value())
                    print("Parameters : " + str(res['parameters']))
                    
                    time.sleep(1)
                    if "APAGAR BOMBA" in str(res['parameters']).strip().upper():      
                        print("ejecutandp Apagando bomba ")
                        # ser.write(b'OFF')

                    if "ENCENDER BOMBA" in str(res['parameters']).strip().upper():                        
                        print("ejecutando Encender bomba ")
                        # ser.write(b'ON')                        


    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    # Close down consumer to commit final offsets.
    c.close()
