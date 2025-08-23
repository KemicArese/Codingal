import cv2
import matplotlib.pyplot as plt

image = cv2.imread('example.jpeg')

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.axis('off')
plt.show()

print('Image displayed successfully.')