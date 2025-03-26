import paho.mqtt.client as mqtt
import cv2
import numpy as np
import time

# MQTT Configuration
BROKER = "localhost"
CAPTURE_TOPIC = "capture/image"
IMAGE_TOPIC = "image/data"

# Initialize webcam
camera = cv2.VideoCapture(0)

def on_message(client, userdata, message):
    """
    Callback function triggered when a message is received.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata: User-defined data of any type.
        message (mqtt.MQTTMessage): The message instance containing the payload.
    """
    print("Capture command received. Capturing image...")

    # Capture a single image
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image.")
        return

    # Encode the image to bytes
    _, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()

    # Publish the image bytes
    client.publish(IMAGE_TOPIC, img_bytes, qos=1)
    print("Image published successfully.")

# Setup MQTT Client
client = mqtt.Client(client_id="Subscriber", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, 1883, 60)

# Subscribe to the capture command topic
client.subscribe(CAPTURE_TOPIC, qos=1)

print("Waiting for capture command...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
    camera.release()