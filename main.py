#!/usr/bin/env python3

from paddleocr import PaddleOCR, draw_ocr
import cv2
import gpxpy
import gpxpy.gpx
from pydantic import BaseModel
from loguru import logger
from typing import Optional
import argparse
from pathlib import Path
from PIL import Image


class BBox(BaseModel):
    top: int
    bottom: int
    right: int
    left: int

class Gps(BaseModel):
    latitude: float
    longitude: float
    elevation: Optional[float] = 0.0

class FrameGpsDetector():
    def __init__(self, gps_bbox: BBox, save_wrong_frame=False):
        self._gps_bbox = gps_bbox
        self._save_wrong_frame = save_wrong_frame
        self._wrong_frame_cnt = 0

        ## OCR
        # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
        # You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
        # to switch the language model in order.

        self._ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False) # need to run only once to download and load model into memory
    
    def predict(self, frame) -> Gps:
        # crop frame bouning box [y:y+h, x:x+w]
        crop_frame = frame[
            self._gps_bbox.top:self._gps_bbox.bottom, 
            self._gps_bbox.left:self._gps_bbox.right
        ]
        result = self._ocr.ocr(crop_frame, cls=True)
        
        # use the top left x-axis of the bounding box after inference sorting
        #
        #   inference bbox: [top-left x, top-left y, bottom-right x, bottom-right y]
        #   s[0][0] is the top left x-axis of the bounding box
        # 
        sorted(result, key = lambda s: s[0][0])
        if not len(result):
            return None
        
        return GpsInfoProcessor(result).gps
    
    def save_frame(self, frame, result):
        wrong_img_path = Path('wrong_frame') / f'{self._wrong_frame_cnt}.jpg'
        wrong_img_path.parent.mkdir(parents=True, exist_ok=True)

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]

        # for txt, score, box in zip(txts, scores, boxes):
        #     logger.info(f"{txt}: {score} : {box}")

        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save(wrong_img_path)

        self._wrong_frame_cnt += 1

class GpsInfoProcessor(object):
    def __init__(self, result: list, threshold: float = 0.0):
        line = result[0]
        # txts = line[1][0]s
        txts = " ".join((line[1][0] for line in result)) 
        boxes = line[0]
        scores = line[1][1]
        self._gps = None

        if scores < threshold:
            raise Exception("score is too low")

        # split txt by space
        self._gpus_info = txts.split()

        try:
            latitude_name_idx = self._gpus_info.index("N")
            longitude_name_idx = self._gpus_info.index("E")

            if latitude_name_idx + 2 != longitude_name_idx:
                raise ValueError("index is not match")

            latitude = self._gpus_info[latitude_name_idx+1]
            longitude = self._gpus_info[longitude_name_idx+1]
        
            latitude, longitude = float(latitude), float(longitude)
            self._gps = Gps(latitude=latitude, longitude=longitude)
        except ValueError as e:
            logger.warning(f"failed to parser gps information[{txts}]: {e}")
            
    @property
    def gps(self) -> Gps:
        return self._gps

def parse_args():
    parser = argparse.ArgumentParser(prog="Video GPS information Detector",
                    description="Detect video frame that has GPS information, and save it into a .gpx file")

    parser.add_argument(
        "-i",
        "--input-video",
        help="video that want to detect gps information",
        type=str,
        metavar="VIDEO",
        default=["e3v.ts"],
        required=True,
    )
    return parser.parse_args()

def main():

    args = parse_args()
    input_video= Path(args.input_video)
    logger.info(f"Input video: {input_video}")
    
    ## opencv
    cap = cv2.VideoCapture(str(input_video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    logger.info(f'FPS: {fps}')
    
    ## GPX
    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    frame_cnt = 0

    # =================
    # GPS Frame Detctor
    # =================
    gps_detector:FrameGpsDetector = FrameGpsDetector(
        gps_bbox=BBox(top=1002, bottom=1062, right=1516, left=16),
        save_wrong_frame=True,
    )

    # scan all frame in video
    while (cap.isOpened()):
        try:
            ret, frame = cap.read()
            
            if not ret:
                print("failed to read frame")
                break
            
            # detect frames per second
            if frame_cnt % int(fps) != 0:
                continue
            
            gps = gps_detector.predict(frame)
            if gps is None:
                continue

            # Create GPS points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(gps.latitude, gps.longitude, elevation=0))

        finally:
            frame_cnt += 1

    cap.release()
    cv2.destroyAllWindows()

    with open(input_video.with_suffix('.gpx'), 'w') as f:
        f.write(gpx.to_xml())

if __name__ == '__main__':
    main()
