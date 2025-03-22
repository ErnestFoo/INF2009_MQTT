import paho.mqtt.client as mqtt
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
client.subscribe(IMAGE_TOPIC)

print("Sending capture command...")
client.publish(CAPTURE_TOPIC, "Capture Now")

# Start listening for the images
print("Waiting for image...")
client.loop_forever()