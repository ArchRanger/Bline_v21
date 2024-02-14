import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

matrisler = [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]

def siyah(alan, alan_no):
    start_time = time.time()

    gray = cv2.cvtColor(alan, cv2.COLOR_BGR2GRAY)

    lower_black = 0
    upper_black = 30

    mask = cv2.inRange(gray, lower_black, upper_black)
    black_pixels = cv2.bitwise_and(alan, alan, mask=mask)

    gray = cv2.cvtColor(black_pixels, cv2.COLOR_BGR2GRAY)  # Yoğunluk
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)  # B&W

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    section_width = alan.shape[1] // 5
    matris = [0, 0, 0, 0, 0]

    for contour in contours:
        # Konturun alanını hesapla
        area = cv2.contourArea(contour)
        # Alanı belirli bir eşik değerinden büyük olan konturları işle
        if area > 100:
            # Konturu çiz
            cv2.drawContours(alan, [contour], -1, (0, 255, 0), 2)
            # Konturun dış sınırlayıcı kutusunu hesapla
            x, y, w, h = cv2.boundingRect(contour)

            center_x = x + w // 2  # Sınırlayıcı kutunun merkezi
            center_y = y + h // 2

            section_index = center_x // section_width
            if section_index >= 5:
                section_index = 4

            matris[section_index] = 1

            print(f"Alan {alan_no} - Koordinatlar: {center_x}, {center_y} - Matris: {matris}")

            cv2.circle(alan, (center_x, center_y), 5, (0, 0, 255), -1)
            break

    matrisler[alan_no] = matris

    stop_time = time.time()
    print("Süre: ", stop_time - start_time)


while True:
    ret, photo = cap.read()
    if not ret:
        break

    photo = cv2.flip(photo, 1)  # Mirror
    kernel_size = (5, 5)
    photo = cv2.GaussianBlur(photo, kernel_size, 0)

    cv2.rectangle(photo, (90, 20), (230, 60), (0, 255, 0), 2)
    cv2.rectangle(photo, (90, 140), (230, 180), (0, 255, 0), 2)

    alan0 = photo[20:60, 90:230]
    alan1 = photo[140:180, 90:230]

    siyah(alan0, 0)
    siyah(alan1, 1)


    if len(matrisler) >= 2:
        matrisler_birlesik = [matrisler[0], matrisler[1]]
    else:
        matrisler_birlesik = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    print(matrisler_birlesik)

    cv2.imshow("Live", photo)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
