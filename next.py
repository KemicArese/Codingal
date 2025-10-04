import cv2

img = cv2.imread('example.png')

if img is None:
    print("Error: Could not load image.")
    exit()  
else:
    transform_type = 'original'

    print("Press the following keys to change transforms:")
    print("r - Rotate 90 degrees clockwise")
    print("f - Flip horizontally")
    print("v - Flip vertically")
    print("g - Convert to grayscale")
    print("z - Resize to half")
    print("l -")
    print("o - Original Image")
    print("q - Quit")

    while True:
        if transform_type == 'original':
            display_img = img
        elif transform_type == 'rotate':
            display_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif transform_type == 'flip_horizontal':
            display_img = cv2.flip(img, 1)
        elif transform_type == 'flip_vertical':
            display_img = cv2.flip(img, 0)
        elif transform_type == 'grayscale':
            display_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif transform_type == 'resize':
            display_img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
        else:
            transform_img = img

        cv2.imshow('Image Transformations', display_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            transform_type = 'rotate'
        elif key == ord('f'):
            transform_type = 'flip_horizontal'
        elif key == ord('v'):
            transform_type = 'flip_vertical'
        elif key == ord('g'):
            transform_type = 'grayscale'
        elif key == ord('z'):
            transform_type = 'resize'
        elif key == ord('o'):
            transform_type = 'original'
        elif key == ord('q'):
            break
        else:
            print("Invalid key. Please try again.")

    cv2.destroyAllWindows()
    
