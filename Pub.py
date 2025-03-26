import paho.mqtt.client as mqtt
    """
    The Python script sets up an MQTT client to receive and save images sent over a specified topic.
    
    :param client: The `client` parameter in the code snippet refers to the MQTT client instance created
    using the `mqtt.Client` class from the `paho.mqtt.client` module. This client is responsible for
    connecting to the MQTT broker, subscribing to topics, publishing messages, and handling incoming
    messages
    :param userdata: The `userdata` parameter in the `on_message` function is a user-defined data of any
    type that can be passed to the MQTT client when setting up the callback functions. It allows you to
    pass additional information or context to the callback function when handling messages. This
    parameter is optional and can be used
    :param message: The `message` parameter in the `on_message` function is of type `mqtt.MQTTMessage`
    and represents the message instance containing the payload received from the MQTT broker. It
    contains information such as the payload data, topic, QoS level, and other message attributes. In
    this context,
    """
import numpy as np
import cv2
import time

# MQTT Configuration
BROKER = "localhost" 
CAPTURE_TOPIC = "capture/image"
IMAGE_TOPIC = "image/data"

def on_message(client, userdata, message):
    """
    Callback function to handle received image.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata: User-defined data of any type.
        message (mqtt.MQTTMessage): The message instance containing the payload.

    """
    print("Image received. Saving...")

    # Convert byte data to image
    img_array = np.frombuffer(message.payload, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Save the image
    filename = "received_image.jpg"
    cv2.imwrite(filename, img)
    print(f"Image saved as {filename}")

# Setup MQTT Client
client = mqtt.Client(client_id="Publisher", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, 1883, 60)

# Subscribe to receive image data
client.subscribe(IMAGE_TOPIC, qos=1)

print("Sending capture command...")
client.publish(CAPTURE_TOPIC, "Capture Now", qos=1)

# Start listening for the images
print("Waiting for image...")
client.loop_forever()