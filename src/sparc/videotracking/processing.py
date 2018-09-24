
import numpy as np
import cv2


class Processing:

    def __init__(self):
        self._image = None
        self._gray = None
        self._blur = None
        self._mask = None

    def get_gray_image(self):
        return self._gray

    def read_image(self, file_name):
        self._image = cv2.imread(file_name, 1)

    def filter_and_threshold(self):
        if self._image is None:
            raise Exception("No image selected! Please read the image first.")

        self._gray = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        self._blur = cv2.GaussianBlur(self._gray, (5, 5), 0)

        return self._gray, self._blur

    def mask_and_image(self, roi):
        r = roi
        self._mask = np.zeros(self._blur.shape[:2], dtype=np.uint8)
        cv2.rectangle(self._mask, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), 255, thickness=-1)

        return self._mask

    def feature_detect(self, h=2000, report_values=False):

        if report_values:
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(self._blur)
            print(minVal, maxVal, minLoc, maxLoc)

        surf = cv2.xfeatures2d.SURF_create(h)
        kp, dst = surf.detectAndCompute(self._blur, self._mask)

        filtered_kp = [x for x in kp if not self._blur[int(x.pt[0] + 0.5), int(x.pt[1] + 0.5)] > 80]

        # self.feature_image = cv2.drawKeypoints(self._image, filtered_kp, self._image)

        return filtered_kp, dst

    def grab_cut(self):
        mask = np.zeros(self.image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (300, 350, 600, 400)
        cv2.grabCut(self.image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = self.image * mask2[:, :, np.newaxis]

        return img

    def detect_ventricle(self, mask, show=False):
        if self.blur is None:
            raise Exception("Please create grayscale image using the 'filter_and_threshold' method.")

        m = mask
        masked_image = self.gray * m
        # filter = cv2.Laplacian(masked_image, cv2.CV_64F)
        ventricle = cv2.Canny(masked_image, 70, 120)
        # ventricle = cv2.Canny(self.gray, 70, 120)
        # masked_image = ventricle * m
        blend = cv2.addWeighted(self.gray, 0.5, ventricle, 0.5, 0)

        if show:
            cv2.imshow('Ventricle Edge', blend)
            cv2.waitKey(0)

