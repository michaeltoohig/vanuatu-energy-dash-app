from datetime import datetime
from pathlib import Path

import numpy as np
import cv2 as cv
import camelot
from PIL import Image
from pdf2image import convert_from_path


def convert_image_to_cv2(img: Image) -> np.ndarray:
    return cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)


def extract_source_figure(fp: Path):
    # assuming report doesn't change format, the energy source figure is on the first page
    image = convert_from_path(fp, fmt="jpg", single_file=True)[0]
    img = convert_image_to_cv2(image)

    # prepare img and crop roi
    top_y_crop = int(img.shape[0] * (7 / 100))
    bottom_y_crop = int(img.shape[0] * (45 / 100))
    roi = img[top_y_crop:bottom_y_crop, 0 : img.shape[1]]  # crop top 40% of page

    roi_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)  # convert roi into gray
    roi_blur = cv.GaussianBlur(roi_gray, (5, 5), 1)  # apply blur to roi
    roi_canny = cv.Canny(roi_blur, 10, 50)  # apply canny to roi

    # Find my contours
    contours, _ = cv.findContours(roi_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    cntrs = []
    for i in contours:
        epsilon = 0.05 * cv.arcLength(i, True)
        approx = cv.approxPolyDP(i, epsilon, True)
        if len(approx) == 4:
            cntrs.append(approx)
    largestCntr = max(cntrs, key=cv.contourArea)
    x, y, w, h = cv.boundingRect(largestCntr)
    figure = roi[y : y + h, x : x + w]
    # Save the figure
    figure_fp = fp.parent / f"{fp.stem}-source.jpg"
    cv.imwrite(str(figure_fp), figure)


def extract_source_table(fp: Path):
    tables = camelot.read_pdf(str(fp))
    for t in tables:
        if "total kwh produced" in str(t.df).lower():
            table_fp = fp.parent / f"{fp.stem}-source.csv"
            t.to_csv(str(table_fp))


def parse_source_table(df):
    date = datetime.strptime(df.columns[0], "%b-%y")
    locations = df.columns[1:]
    data = dict(date=date, locations={loc: {} for loc in locations})
    for row in df.values:
        label = row[0].lower()
        for loc, value in zip(locations, row[1:]):
            # catch empty/missing values in the table
            if value in ("-", "N/A"):
                value = "0"
            data["locations"][loc][label.lower()] = value
    return data